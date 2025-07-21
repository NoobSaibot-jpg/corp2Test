from flask import Blueprint, request, jsonify, abort, render_template_string
from app.models.models import Invoice, Order
from app.db import db
from datetime import datetime
from app.utils.number_to_words import number_to_words_ua

invoice_api = Blueprint('invoice_api', __name__, url_prefix='/api/invoices')

# Получить список всех счетов-фактур
@invoice_api.route('/', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([
        {
            'id': inv.id,
            'order_id': inv.order_id,
            'order_status': inv.order.status if inv.order else None,
            'date': inv.date.isoformat(),
            'total': inv.total
        } for inv in invoices
    ])

# Получить счет-фактуру по id
@invoice_api.route('/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    return jsonify({
        'id': inv.id,
        'order_id': inv.order_id,
        'order_status': inv.order.status if inv.order else None,
        'date': inv.date.isoformat(),
        'total': inv.total
    })

# Создать новый счет-фактуру
@invoice_api.route('/', methods=['POST'])
def create_invoice():
    data = request.get_json()
    if not data or not data.get('order_id'):
        abort(400, 'Missing required field: order_id')
    try:
        invoice_date = datetime.fromisoformat(data.get('date')) if data.get('date') else datetime.utcnow()
    except Exception:
        abort(400, 'Invalid date format')
    invoice = Invoice(
        order_id=data['order_id'],
        date=invoice_date,
        total=data.get('total')
    )
    db.session.add(invoice)
    db.session.commit()
    return jsonify({'id': invoice.id}), 201

# Обновить счет-фактуру
@invoice_api.route('/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    data = request.get_json()
    if not data:
        abort(400, 'No input data')
    if 'order_id' in data:
        inv.order_id = data['order_id']
    if 'date' in data:
        try:
            inv.date = datetime.fromisoformat(data['date'])
        except Exception:
            abort(400, 'Invalid date format')
    if 'total' in data:
        inv.total = data['total']
    db.session.commit()
    return jsonify({'result': 'success'})

# Удалить счет-фактуру
@invoice_api.route('/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    db.session.delete(inv)
    db.session.commit()
    return jsonify({'result': 'deleted'})

PRINT_TEMPLATE_INVOICE_UA = """
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>Рахунок-фактура №{{ invoice.id }}</title>
  <style>
    body { font-family: Arial, sans-serif; }
    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
    th, td { border: 1px solid #333; padding: 6px 10px; text-align: left; }
    th { background: #eee; }
    .header { margin-bottom: 20px; }
    .footer { margin-top: 30px; }
    .customer-info { margin-bottom: 15px; }
    .total-words { margin-top: 15px; font-weight: bold; }
  </style>
</head>
<body>
  <div class=\"header\">
    <h2>Рахунок-фактура №{{ invoice.id }} від {{ invoice.date.strftime('%d.%m.%Y') }}</h2>
    <div class=\"customer-info\">
      <div><strong>Покупець:</strong> {{ invoice.order.customer.name if invoice.order and invoice.order.customer else '' }}</div>
      {% if invoice.order and invoice.order.customer and invoice.order.customer.edrpou %}
      <div><strong>ЕДРПО:</strong> {{ invoice.order.customer.edrpou }}</div>
      {% endif %}
      {% if invoice.order and invoice.order.customer and invoice.order.customer.address %}
      <div><strong>Адреса:</strong> {{ invoice.order.customer.address }}</div>
      {% endif %}
      {% if invoice.order and invoice.order.customer and invoice.order.customer.phone %}
      <div><strong>Телефон:</strong> {{ invoice.order.customer.phone }}</div>
      {% endif %}
    </div>
  </div>
  <table>
    <thead>
      <tr>
        <th>№</th>
        <th>Товар/послуга</th>
        <th>Кількість</th>
        <th>Од. вим.</th>
        <th>Ціна</th>
        <th>Сума</th>
      </tr>
    </thead>
    <tbody>
      {% for item in invoice.order.items %}
      <tr>
        <td>{{ loop.index }}</td>
        <td>{{ item.product.name if item.product else '' }}</td>
        <td>{{ item.quantity }}</td>
        <td>{{ item.product.unit if item.product else '' }}</td>
        <td>{{ item.price }}</td>
        <td>{{ '%.2f' % (item.price * item.quantity) }}</td>
      </tr>
      {% endfor %}
    </tbody>
    <tfoot>
      <tr>
        <th colspan=\"5\" style=\"text-align:right;\">Всього:</th>
        <th>{{ '%.2f' % total }}</th>
      </tr>
      <tr>
        <th colspan=\"5\" style=\"text-align:right;\">У тому числі ПДВ (20%):</th>
        <th>{{ '%.2f' % total_vat }}</th>
      </tr>
    </tfoot>
  </table>
  <div class=\"total-words\">
    <strong>Сума прописом:</strong> {{ total_words }}
  </div>
  <div class=\"footer\">
    <div>Відповідальний: ____________________</div>
    <div>Підпис: ____________________</div>
  </div>
</body>
</html>
"""

@invoice_api.route('/<int:invoice_id>/print', methods=['GET'])
def print_invoice(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    # Считаем total
    total = sum((item.price or 0) * (item.quantity or 0) for item in inv.order.items)
    vat_rate = 0.2
    total_vat = total * vat_rate / (1 + vat_rate)
    total_wo_vat = total - total_vat
    total_words = number_to_words_ua(total)
    html = render_template_string(
        PRINT_TEMPLATE_INVOICE_UA,
        invoice=inv,
        number_to_words_ua=number_to_words_ua,
        total=total,
        total_vat=total_vat,
        total_wo_vat=total_wo_vat,
        total_words=total_words
    )
    return html 

XML_TEMPLATE_INVOICE_UA = """<?xml version="1.0" encoding="utf-8"?>
<ЕлектроннийДокумент>
   <Заголовок>
      <НомерДокументу>{{ invoice.id }}</НомерДокументу>
      <ТипДокументу>Рахунок-фактура</ТипДокументу>
      <КодТипуДокументу>001</КодТипуДокументу>
      <ДатаДокументу>{{ invoice.date.strftime('%Y-%m-%d') }}</ДатаДокументу>
      <НомерЗамовлення>{{ invoice.order.id if invoice.order else '' }}</НомерЗамовлення>
      <ДатаЗамовлення>{{ invoice.order.date.strftime('%Y-%m-%d') if invoice.order else '' }}</ДатаЗамовлення>
      <МісцеСкладання>{{ invoice.order.customer.address if invoice.order and invoice.order.customer and invoice.order.customer.address else 'Не вказано' }}</МісцеСкладання>
   </Заголовок>
   <Сторони>
      <Контрагент>
         <СтатусКонтрагента>Продавець</СтатусКонтрагента>
         <ВидОсоби>Юридична</ВидОсоби>
         <НазваКонтрагента>Наша компанія</НазваКонтрагента>
         <КодКонтрагента>12345678</КодКонтрагента>
         <ІПН>123456789012</ІПН>
         <СвідоцтвоПДВ>1234567890</СвідоцтвоПДВ>
         <GLN>1234567890123</GLN>
      </Контрагент>
      <Контрагент>
         <СтатусКонтрагента>Покупець</СтатусКонтрагента>
         <ВидОсоби>Юридична</ВидОсоби>
         <НазваКонтрагента>{{ invoice.order.customer.name if invoice.order and invoice.order.customer else 'Не вказано' }}</НазваКонтрагента>
         <КодКонтрагента>{{ invoice.order.customer.edrpou if invoice.order and invoice.order.customer and invoice.order.customer.edrpou else '00000000' }}</КодКонтрагента>
         <ІПН>{{ invoice.order.customer.edrpou if invoice.order and invoice.order.customer and invoice.order.customer.edrpou else '000000000000' }}</ІПН>
         <СвідоцтвоПДВ>{{ invoice.order.customer.edrpou if invoice.order and invoice.order.customer and invoice.order.customer.edrpou else '' }}</СвідоцтвоПДВ>
         <GLN>{{ invoice.order.customer.edrpou if invoice.order and invoice.order.customer and invoice.order.customer.edrpou else '0000000000000' }}</GLN>
      </Контрагент>
   </Сторони>
   <Параметри>
      <Параметр ІД="1" назва="Адреса покупця">{{ invoice.order.customer.address if invoice.order and invoice.order.customer and invoice.order.customer.address else 'Не вказано' }}</Параметр>
      <Параметр ІД="2" назва="Телефон покупця">{{ invoice.order.customer.phone if invoice.order and invoice.order.customer and invoice.order.customer.phone else 'Не вказано' }}</Параметр>
   </Параметри>
   <Таблиця>
      {% for item in invoice.order.items %}
      <Рядок ІД="{{ loop.index }}">
         <НомПоз>{{ loop.index }}</НомПоз>
         <Штрихкод ІД="{{ loop.index }}">{{ item.product.id }}</Штрихкод>
         <АртикулПокупця>{{ item.product.id }}</АртикулПокупця>
         <Найменування>{{ item.product.name if item.product else 'Не вказано' }}</Найменування>
         <ПрийнятаКількість>{{ "%.3f"|format(item.quantity) }}</ПрийнятаКількість>
         <ОдиницяВиміру>{{ item.product.unit if item.product and item.product.unit else 'шт.' }}</ОдиницяВиміру>
         <БазоваЦіна>{{ "%.2f"|format((item.price or 0) - (item.price or 0) * 0.2 / 1.2) }}</БазоваЦіна>
         <ПДВ>{{ "%.2f"|format((item.price or 0) * 0.2 / 1.2) }}</ПДВ>
         <Ціна>{{ "%.2f"|format(item.price or 0) }}</Ціна>
         <СтавкаПДВ>20</СтавкаПДВ>
         <ВсьогоПоРядку>
            <СумаБезПДВ>{{ "%.2f"|format((item.price or 0) * item.quantity - (item.price or 0) * item.quantity * 0.2 / 1.2) }}</СумаБезПДВ>
            <СумаПДВ>{{ "%.2f"|format((item.price or 0) * item.quantity * 0.2 / 1.2) }}</СумаПДВ>
            <Сума>{{ "%.2f"|format((item.price or 0) * item.quantity) }}</Сума>
         </ВсьогоПоРядку>
      </Рядок>
      {% endfor %}
   </Таблиця>
   <ВсьогоПоДокументу>
      <СумаБезПДВ>{{ "%.2f"|format(total_wo_vat) }}</СумаБезПДВ>
      <ПДВ>{{ "%.2f"|format(total_vat) }}</ПДВ>
      <Сума>{{ "%.2f"|format(total) }}</Сума>
   </ВсьогоПоДокументу>
</ЕлектроннийДокумент>
"""

@invoice_api.route('/<int:invoice_id>/xml', methods=['GET'])
def xml_invoice(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    # Считаем total
    total = sum((item.price or 0) * (item.quantity or 0) for item in inv.order.items)
    vat_rate = 0.2
    total_vat = total * vat_rate / (1 + vat_rate)
    total_wo_vat = total - total_vat
    
    xml_content = render_template_string(
        XML_TEMPLATE_INVOICE_UA,
        invoice=inv,
        total=total,
        total_vat=total_vat,
        total_wo_vat=total_wo_vat
    )
    
    from flask import Response
    return Response(xml_content, mimetype='application/xml') 