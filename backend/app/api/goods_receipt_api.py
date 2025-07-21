from flask import Blueprint, request, jsonify, abort, render_template_string
from app.models.models import GoodsReceipt, GoodsReceiptItem, Product, Customer
from app.services.fifo_service import FIFOService
from app.db import db
from datetime import datetime
from app.utils.number_to_words import number_to_words_ua
import traceback

goods_receipt_api = Blueprint('goods_receipt_api', __name__, url_prefix='/api/goods_receipts')

# Получить список всех приходных накладных
@goods_receipt_api.route('/', methods=['GET'])
def get_goods_receipts():
    try:
        receipts = GoodsReceipt.query.all()
        return jsonify([
            {
                'id': r.id,
                'date': r.date.isoformat(),
                'number': r.number,
                'supplier_id': r.supplier_id,
                'supplier_name': r.supplier.name if r.supplier else None,
                'contract': r.contract,
                'warehouse': r.warehouse,
                'organization': r.organization,
                'operation_type': r.operation_type,
                'responsible': r.responsible,
                'comment': r.comment,
                'pricing_note': r.pricing_note,
                'items': [
                    {
                        'id': item.id,
                        'product_id': item.product_id,
                        'product_name': item.product.name if item.product else None,
                        'quantity': item.quantity,
                        'price': item.price
                    } for item in r.items
                ]
            } for r in receipts
        ])
    except Exception as e:
        print(f"[ERROR] get_goods_receipts: {e}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

# Получить приходную накладную по id
@goods_receipt_api.route('/<int:receipt_id>', methods=['GET'])
def get_goods_receipt(receipt_id):
    r = GoodsReceipt.query.get_or_404(receipt_id)
    return jsonify({
        'id': r.id,
        'date': r.date.isoformat(),
        'number': r.number,
        'supplier_id': r.supplier_id,
        'supplier_name': r.supplier.name if r.supplier else None,
        'contract': r.contract,
        'warehouse': r.warehouse,
        'organization': r.organization,
        'operation_type': r.operation_type,
        'responsible': r.responsible,
        'comment': r.comment,
        'pricing_note': r.pricing_note,
        'items': [
            {
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name if item.product else None,
                'quantity': item.quantity,
                'price': item.price
            } for item in r.items
        ]
    })

# Создать новую приходную накладную с позициями
@goods_receipt_api.route('/', methods=['POST'])
def create_goods_receipt():
    data = request.get_json()
    if not data or not data.get('date') or not data.get('items'):
        abort(400, 'Missing required fields: date, items')
    try:
        receipt_date = datetime.fromisoformat(data['date'])
    except Exception:
        abort(400, 'Invalid date format')
    receipt = GoodsReceipt(
        date=receipt_date,
        number=data.get('number'),
        supplier_id=data.get('supplier_id'),
        contract=data.get('contract'),
        warehouse=data.get('warehouse'),
        organization=data.get('organization'),
        operation_type=data.get('operation_type'),
        responsible=data.get('responsible'),
        comment=data.get('comment'),
        pricing_note=data.get('pricing_note')
    )
    db.session.add(receipt)
    db.session.flush()  # Получить id накладной
    for item in data['items']:
        if not item.get('product_id') or not item.get('quantity'):
            abort(400, 'Each item must have product_id and quantity')
        receipt_item = GoodsReceiptItem(
            goods_receipt_id=receipt.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item.get('price')
        )
        db.session.add(receipt_item)
    db.session.commit()
    FIFOService.create_batches_from_receipt(receipt.id)
    return jsonify({'id': receipt.id}), 201

# Обновить приходную накладную и её позиции
@goods_receipt_api.route('/<int:receipt_id>', methods=['PUT'])
def update_goods_receipt(receipt_id):
    r = GoodsReceipt.query.get_or_404(receipt_id)
    data = request.get_json()
    if not data:
        abort(400, 'No input data')
    if 'date' in data:
        try:
            r.date = datetime.fromisoformat(data['date'])
        except Exception:
            abort(400, 'Invalid date format')
    if 'number' in data:
        r.number = data['number']
    if 'supplier_id' in data:
        r.supplier_id = data['supplier_id']
    if 'contract' in data:
        r.contract = data['contract']
    if 'warehouse' in data:
        r.warehouse = data['warehouse']
    if 'organization' in data:
        r.organization = data['organization']
    if 'operation_type' in data:
        r.operation_type = data['operation_type']
    if 'responsible' in data:
        r.responsible = data['responsible']
    if 'comment' in data:
        r.comment = data['comment']
    if 'pricing_note' in data:
        r.pricing_note = data['pricing_note']
    # Обновление позиций (перезапись)
    if 'items' in data:
        GoodsReceiptItem.query.filter_by(goods_receipt_id=r.id).delete()
        for item in data['items']:
            if not item.get('product_id') or not item.get('quantity'):
                abort(400, 'Each item must have product_id and quantity')
            receipt_item = GoodsReceiptItem(
                goods_receipt_id=r.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item.get('price')
            )
            db.session.add(receipt_item)
    db.session.commit()
    return jsonify({'result': 'success'})

# Удалить приходную накладную и её позиции
@goods_receipt_api.route('/<int:receipt_id>', methods=['DELETE'])
def delete_goods_receipt(receipt_id):
    r = GoodsReceipt.query.get_or_404(receipt_id)
    GoodsReceiptItem.query.filter_by(goods_receipt_id=r.id).delete()
    db.session.delete(r)
    db.session.commit()
    return jsonify({'result': 'deleted'}) 

PRINT_TEMPLATE_UA = """
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>Прибуткова накладна №{{ receipt.number }}</title>
  <style>
    body { font-family: Arial, sans-serif; }
    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
    th, td { border: 1px solid #333; padding: 6px 10px; text-align: left; }
    th { background: #eee; }
    .header { margin-bottom: 20px; }
    .footer { margin-top: 30px; }
    .supplier-info { margin-bottom: 15px; }
    .total-words { margin-top: 15px; font-weight: bold; }
  </style>
</head>
<body>
  <div class=\"header\">
    <h2>Прибуткова накладна №{{ receipt.number }} від {{ receipt.date.strftime('%d.%m.%Y') }}</h2>
    <div class=\"supplier-info\">
      <div><strong>Постачальник:</strong> {{ receipt.supplier.name if receipt.supplier else '' }}</div>
      {% if receipt.supplier and receipt.supplier.edrpou %}
      <div><strong>ЕДРПО:</strong> {{ receipt.supplier.edrpou }}</div>
      {% endif %}
      {% if receipt.supplier and receipt.supplier.address %}
      <div><strong>Адреса:</strong> {{ receipt.supplier.address }}</div>
      {% endif %}
      {% if receipt.supplier and receipt.supplier.phone %}
      <div><strong>Телефон:</strong> {{ receipt.supplier.phone }}</div>
      {% endif %}
      {% if receipt.supplier and receipt.supplier.bank_name %}
      <div><strong>Банк:</strong> {{ receipt.supplier.bank_name }}</div>
      {% endif %}
      {% if receipt.supplier and receipt.supplier.bank_account %}
      <div><strong>Рахунок:</strong> {{ receipt.supplier.bank_account }}</div>
      {% endif %}
      {% if receipt.supplier and receipt.supplier.mfo %}
      <div><strong>МФО:</strong> {{ receipt.supplier.mfo }}</div>
      {% endif %}
      {% if receipt.supplier and receipt.supplier.ipn %}
      <div><strong>ІПН:</strong> {{ receipt.supplier.ipn }}</div>
      {% endif %}
      {% if receipt.supplier and receipt.supplier.vat_certificate %}
      <div><strong>Свідоцтво ПДВ:</strong> {{ receipt.supplier.vat_certificate }}</div>
      {% endif %}
    </div>
    <div><strong>Покупець:</strong> {{ receipt.organization or 'Наша компанія' }}</div>
    {% if receipt.contract %}<div><strong>Договір:</strong> {{ receipt.contract }}</div>{% endif %}
    {% if receipt.warehouse %}<div><strong>Склад:</strong> {{ receipt.warehouse }}</div>{% endif %}
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
      {% for item in receipt.items %}
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
    <div>Всього найменувань: {{ receipt.items|length }}, на суму {{ '%.2f' % total }} грн.</div>
    <div>Відвантажив(ла): ____________________</div>
    <div>Отримав(ла): ____________________</div>
    <div>Відповідальний: {{ receipt.responsible or '____________________' }}</div>
    <div>Підпис: ____________________</div>
  </div>
</body>
</html>
"""

@goods_receipt_api.route('/<int:receipt_id>/print', methods=['GET'])
def print_goods_receipt(receipt_id):
    r = GoodsReceipt.query.get_or_404(receipt_id)
    # Считаем total
    total = sum((item.price or 0) * (item.quantity or 0) for item in r.items)
    vat_rate = 0.2
    total_vat = total * vat_rate / (1 + vat_rate)
    total_wo_vat = total - total_vat
    total_words = number_to_words_ua(total)
    html = render_template_string(
        PRINT_TEMPLATE_UA,
        receipt=r,
        number_to_words_ua=number_to_words_ua,
        total=total,
        total_vat=total_vat,
        total_wo_vat=total_wo_vat,
        total_words=total_words
    )
    return html

# В шаблоне:
# - Всього: {{ '%.2f' % total }}
# - У тому числі ПДВ: {{ '%.2f' % total_vat }}
# - Сума прописом: {{ total_words }} 

XML_TEMPLATE_RECEIPT_UA = """<?xml version="1.0" encoding="utf-8"?>
<ЕлектроннийДокумент>
   <Заголовок>
      <НомерДокументу>{{ receipt.number or receipt.id }}</НомерДокументу>
      <ТипДокументу>Прибуткова накладна</ТипДокументу>
      <КодТипуДокументу>007</КодТипуДокументу>
      <ДатаДокументу>{{ receipt.date.strftime('%Y-%m-%d') }}</ДатаДокументу>
      <НомерЗамовлення>{{ receipt.number or '' }}</НомерЗамовлення>
      <ДатаЗамовлення>{{ receipt.date.strftime('%Y-%m-%d') }}</ДатаЗамовлення>
      <МісцеСкладання>{{ receipt.supplier.address if receipt.supplier and receipt.supplier.address else 'Не вказано' }}</МісцеСкладання>
   </Заголовок>
   <Сторони>
      <Контрагент>
         <СтатусКонтрагента>Відправник</СтатусКонтрагента>
         <ВидОсоби>Юридична</ВидОсоби>
         <НазваКонтрагента>{{ receipt.supplier.name if receipt.supplier else 'Не вказано' }}</НазваКонтрагента>
         <КодКонтрагента>{{ receipt.supplier.edrpou if receipt.supplier and receipt.supplier.edrpou else '00000000' }}</КодКонтрагента>
         <ІПН>{{ receipt.supplier.edrpou if receipt.supplier and receipt.supplier.edrpou else '000000000000' }}</ІПН>
         <СвідоцтвоПДВ>{{ receipt.supplier.edrpou if receipt.supplier and receipt.supplier.edrpou else '' }}</СвідоцтвоПДВ>
         <GLN>{{ receipt.supplier.edrpou if receipt.supplier and receipt.supplier.edrpou else '0000000000000' }}</GLN>
      </Контрагент>
      <Контрагент>
         <СтатусКонтрагента>Отримувач</СтатусКонтрагента>
         <ВидОсоби>Юридична</ВидОсоби>
         <НазваКонтрагента>Наша компанія</НазваКонтрагента>
         <КодКонтрагента>12345678</КодКонтрагента>
         <ІПН>123456789012</ІПН>
         <СвідоцтвоПДВ>1234567890</СвідоцтвоПДВ>
         <GLN>1234567890123</GLN>
      </Контрагент>
   </Сторони>
   <Параметри>
      <Параметр ІД="1" назва="Адреса постачальника">{{ receipt.supplier.address if receipt.supplier and receipt.supplier.address else 'Не вказано' }}</Параметр>
      <Параметр ІД="2" назва="Телефон постачальника">{{ receipt.supplier.phone if receipt.supplier and receipt.supplier.phone else 'Не вказано' }}</Параметр>
   </Параметри>
   <Таблиця>
      {% for item in receipt.items %}
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

@goods_receipt_api.route('/<int:receipt_id>/xml', methods=['GET'])
def xml_goods_receipt(receipt_id):
    r = GoodsReceipt.query.get_or_404(receipt_id)
    # Считаем total
    total = sum((item.price or 0) * (item.quantity or 0) for item in r.items)
    vat_rate = 0.2
    total_vat = total * vat_rate / (1 + vat_rate)
    total_wo_vat = total - total_vat
    
    xml_content = render_template_string(
        XML_TEMPLATE_RECEIPT_UA,
        receipt=r,
        total=total,
        total_vat=total_vat,
        total_wo_vat=total_wo_vat
    )
    
    from flask import Response
    return Response(xml_content, mimetype='application/xml') 