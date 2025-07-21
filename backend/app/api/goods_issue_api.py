from flask import Blueprint, request, jsonify, abort, render_template_string
from app.models.models import GoodsIssue, GoodsIssueItem, Product, Customer
from app.services.fifo_service import FIFOService
from app.db import db
from datetime import datetime
from app.utils.number_to_words import number_to_words_ua

goods_issue_api = Blueprint('goods_issue_api', __name__, url_prefix='/api/goods_issues')

# Получить список всех расходных накладных
@goods_issue_api.route('/', methods=['GET'])
def get_goods_issues():
    issues = GoodsIssue.query.all()
    return jsonify([
        {
            'id': i.id,
            'date': i.date.isoformat(),
            'number': i.number,
            'customer_id': i.customer_id,
            'customer_name': i.customer.name if i.customer else None,
            'contract': i.contract,
            'warehouse': i.warehouse,
            'organization': i.organization,
            'operation_type': i.operation_type,
            'responsible': i.responsible,
            'comment': i.comment,
            'pricing_note': i.pricing_note,
            'items': [
                {
                    'id': item.id,
                    'product_id': item.product_id,
                    'product_name': item.product.name if item.product else None,
                    'quantity': item.quantity,
                    'price': item.price
                } for item in i.items
            ]
        } for i in issues
    ])

# Получить расходную накладную по id
@goods_issue_api.route('/<int:issue_id>', methods=['GET'])
def get_goods_issue(issue_id):
    i = GoodsIssue.query.get_or_404(issue_id)
    return jsonify({
        'id': i.id,
        'date': i.date.isoformat(),
        'number': i.number,
        'customer_id': i.customer_id,
        'customer_name': i.customer.name if i.customer else None,
        'contract': i.contract,
        'warehouse': i.warehouse,
        'organization': i.organization,
        'operation_type': i.operation_type,
        'responsible': i.responsible,
        'comment': i.comment,
        'pricing_note': i.pricing_note,
        'items': [
            {
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name if item.product else None,
                'quantity': item.quantity,
                'price': item.price
            } for item in i.items
        ]
    })

# Создать новую расходную накладную с позициями
@goods_issue_api.route('/', methods=['POST'])
def create_goods_issue():
    data = request.get_json()
    if not data or not data.get('date') or not data.get('items'):
        abort(400, 'Missing required fields: date, items')
    stock_errors = FIFOService.validate_stock_for_issue(data['items'])
    if stock_errors:
        return jsonify({
            'error': 'Insufficient stock',
            'details': stock_errors
        }), 400
    try:
        issue_date = datetime.fromisoformat(data['date'])
    except Exception:
        abort(400, 'Invalid date format')
    issue = GoodsIssue(
        date=issue_date,
        number=data.get('number'),
        customer_id=data.get('customer_id'),
        contract=data.get('contract'),
        warehouse=data.get('warehouse'),
        organization=data.get('organization'),
        operation_type=data.get('operation_type'),
        responsible=data.get('responsible'),
        comment=data.get('comment'),
        pricing_note=data.get('pricing_note')
    )
    db.session.add(issue)
    db.session.flush()  # Получить id накладной
    for item in data['items']:
        if not item.get('product_id') or not item.get('quantity'):
            abort(400, 'Each item must have product_id and quantity')
        issue_item = GoodsIssueItem(
            goods_issue_id=issue.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item.get('price')
        )
        db.session.add(issue_item)
    db.session.commit()
    for item in data['items']:
        FIFOService.consume_stock(item['product_id'], item['quantity'])
    return jsonify({'id': issue.id}), 201

# Обновить расходную накладную и её позиции
@goods_issue_api.route('/<int:issue_id>', methods=['PUT'])
def update_goods_issue(issue_id):
    i = GoodsIssue.query.get_or_404(issue_id)
    data = request.get_json()
    if not data:
        abort(400, 'No input data')
    if 'date' in data:
        try:
            i.date = datetime.fromisoformat(data['date'])
        except Exception:
            abort(400, 'Invalid date format')
    if 'number' in data:
        i.number = data['number']
    if 'customer_id' in data:
        i.customer_id = data['customer_id']
    if 'contract' in data:
        i.contract = data['contract']
    if 'warehouse' in data:
        i.warehouse = data['warehouse']
    if 'organization' in data:
        i.organization = data['organization']
    if 'operation_type' in data:
        i.operation_type = data['operation_type']
    if 'responsible' in data:
        i.responsible = data['responsible']
    if 'comment' in data:
        i.comment = data['comment']
    if 'pricing_note' in data:
        i.pricing_note = data['pricing_note']
    if 'items' in data:
        GoodsIssueItem.query.filter_by(goods_issue_id=i.id).delete()
        for item in data['items']:
            if not item.get('product_id') or not item.get('quantity'):
                abort(400, 'Each item must have product_id and quantity')
            issue_item = GoodsIssueItem(
                goods_issue_id=i.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item.get('price')
            )
            db.session.add(issue_item)
    db.session.commit()
    return jsonify({'result': 'success'})

# Удалить расходную накладную и её позиции
@goods_issue_api.route('/<int:issue_id>', methods=['DELETE'])
def delete_goods_issue(issue_id):
    i = GoodsIssue.query.get_or_404(issue_id)
    GoodsIssueItem.query.filter_by(goods_issue_id=i.id).delete()
    db.session.delete(i)
    db.session.commit()
    return jsonify({'result': 'deleted'}) 

PRINT_TEMPLATE_ISSUE_UA = """
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>Видаткова накладна №{{ issue.number }}</title>
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
    <h2>Видаткова накладна №{{ issue.number }} від {{ issue.date.strftime('%d.%m.%Y') }}</h2>
    <div class=\"customer-info\">
      <div><strong>Покупець:</strong> {{ issue.customer.name if issue.customer else '' }}</div>
      {% if issue.customer and issue.customer.edrpou %}
      <div><strong>ЕДРПО:</strong> {{ issue.customer.edrpou }}</div>
      {% endif %}
      {% if issue.customer and issue.customer.address %}
      <div><strong>Адреса:</strong> {{ issue.customer.address }}</div>
      {% endif %}
      {% if issue.customer and issue.customer.phone %}
      <div><strong>Телефон:</strong> {{ issue.customer.phone }}</div>
      {% endif %}
      {% if issue.customer and issue.customer.bank_name %}
      <div><strong>Банк:</strong> {{ issue.customer.bank_name }}</div>
      {% endif %}
      {% if issue.customer and issue.customer.bank_account %}
      <div><strong>Рахунок:</strong> {{ issue.customer.bank_account }}</div>
      {% endif %}
      {% if issue.customer and issue.customer.mfo %}
      <div><strong>МФО:</strong> {{ issue.customer.mfo }}</div>
      {% endif %}
      {% if issue.customer and issue.customer.ipn %}
      <div><strong>ІПН:</strong> {{ issue.customer.ipn }}</div>
      {% endif %}
      {% if issue.customer and issue.customer.vat_certificate %}
      <div><strong>Свідоцтво ПДВ:</strong> {{ issue.customer.vat_certificate }}</div>
      {% endif %}
    </div>
    <div><strong>Постачальник:</strong> {{ issue.organization or 'Наша компанія' }}</div>
    {% if issue.contract %}<div><strong>Договір:</strong> {{ issue.contract }}</div>{% endif %}
    {% if issue.warehouse %}<div><strong>Склад:</strong> {{ issue.warehouse }}</div>{% endif %}
  </div>
  <table>
    <thead>
      <tr>
        <th>№</th>
        <th>Товар/послуга</th>
        <th>Кількість</th>
        <th>Од. вим.</th>
        <th>Ціна з ПДВ</th>
        <th>Сума з ПДВ</th>
      </tr>
    </thead>
    <tbody>
      {% for item in issue.items %}
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
    <div>Всього найменувань: {{ issue.items|length }}, на суму {{ '%.2f' % total }} грн.</div>
    <div>Відвантажив(ла): ____________________</div>
    <div>Отримав(ла): ____________________</div>
    <div>Відповідальний: {{ issue.responsible or '____________________' }}</div>
    <div>Підпис: ____________________</div>
  </div>
</body>
</html>
"""

@goods_issue_api.route('/<int:issue_id>/print', methods=['GET'])
def print_goods_issue(issue_id):
    i = GoodsIssue.query.get_or_404(issue_id)
    # Считаем total
    total = sum((item.price or 0) * (item.quantity or 0) for item in i.items)
    vat_rate = 0.2
    total_vat = total * vat_rate / (1 + vat_rate)
    total_wo_vat = total - total_vat
    total_words = number_to_words_ua(total)
    html = render_template_string(
        PRINT_TEMPLATE_ISSUE_UA,
        issue=i,
        number_to_words_ua=number_to_words_ua,
        total=total,
        total_vat=total_vat,
        total_wo_vat=total_wo_vat,
        total_words=total_words
    )
    return html 

XML_TEMPLATE_ISSUE_UA = """<?xml version="1.0" encoding="utf-8"?>
<ЕлектроннийДокумент>
   <Заголовок>
      <НомерДокументу>{{ issue.number or issue.id }}</НомерДокументу>
      <ТипДокументу>Видаткова накладна</ТипДокументу>
      <КодТипуДокументу>006</КодТипуДокументу>
      <ДатаДокументу>{{ issue.date.strftime('%Y-%m-%d') }}</ДатаДокументу>
      <НомерЗамовлення>{{ issue.number or '' }}</НомерЗамовлення>
      <ДатаЗамовлення>{{ issue.date.strftime('%Y-%m-%d') }}</ДатаЗамовлення>
      <МісцеСкладання>{{ issue.customer.address if issue.customer and issue.customer.address else 'Не вказано' }}</МісцеСкладання>
   </Заголовок>
   <Сторони>
      <Контрагент>
         <СтатусКонтрагента>Відправник</СтатусКонтрагента>
         <ВидОсоби>Юридична</ВидОсоби>
         <НазваКонтрагента>Наша компанія</НазваКонтрагента>
         <КодКонтрагента>12345678</КодКонтрагента>
         <ІПН>123456789012</ІПН>
         <СвідоцтвоПДВ>1234567890</СвідоцтвоПДВ>
         <GLN>1234567890123</GLN>
      </Контрагент>
      <Контрагент>
         <СтатусКонтрагента>Отримувач</СтатусКонтрагента>
         <ВидОсоби>Юридична</ВидОсоби>
         <НазваКонтрагента>{{ issue.customer.name if issue.customer else 'Не вказано' }}</НазваКонтрагента>
         <КодКонтрагента>{{ issue.customer.edrpou if issue.customer and issue.customer.edrpou else '00000000' }}</КодКонтрагента>
         <ІПН>{{ issue.customer.edrpou if issue.customer and issue.customer.edrpou else '000000000000' }}</ІПН>
         <СвідоцтвоПДВ>{{ issue.customer.edrpou if issue.customer and issue.customer.edrpou else '' }}</СвідоцтвоПДВ>
         <GLN>{{ issue.customer.edrpou if issue.customer and issue.customer.edrpou else '0000000000000' }}</GLN>
      </Контрагент>
   </Сторони>
   <Параметри>
      <Параметр ІД="1" назва="Адреса покупця">{{ issue.customer.address if issue.customer and issue.customer.address else 'Не вказано' }}</Параметр>
      <Параметр ІД="2" назва="Телефон покупця">{{ issue.customer.phone if issue.customer and issue.customer.phone else 'Не вказано' }}</Параметр>
   </Параметри>
   <Таблиця>
      {% for item in issue.items %}
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

@goods_issue_api.route('/<int:issue_id>/xml', methods=['GET'])
def xml_goods_issue(issue_id):
    i = GoodsIssue.query.get_or_404(issue_id)
    # Считаем total
    total = sum((item.price or 0) * (item.quantity or 0) for item in i.items)
    vat_rate = 0.2
    total_vat = total * vat_rate / (1 + vat_rate)
    total_wo_vat = total - total_vat
    
    xml_content = render_template_string(
        XML_TEMPLATE_ISSUE_UA,
        issue=i,
        total=total,
        total_vat=total_vat,
        total_wo_vat=total_wo_vat
    )
    
    from flask import Response
    return Response(xml_content, mimetype='application/xml') 