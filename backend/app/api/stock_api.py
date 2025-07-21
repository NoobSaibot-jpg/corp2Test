from flask import Blueprint, request, jsonify, render_template_string
from app.models.models import StockBatch, Product
from app.services.fifo_service import FIFOService
from datetime import datetime

stock_api = Blueprint('stock_api', __name__, url_prefix='/api/stock')

# Получить остатки всех товаров
@stock_api.route('/', methods=['GET'])
def get_stock():
    products = Product.query.filter_by(type='product').all()
    stock_data = []
    
    for product in products:
        available_quantity, batches = FIFOService.get_available_stock(product.id)
        stock_data.append({
            'product_id': product.id,
            'product_name': product.name,
            'available_quantity': available_quantity,
            'unit': product.unit
        })
    
    return jsonify(stock_data)

# Получить остатки конкретного товара
@stock_api.route('/<int:product_id>', methods=['GET'])
def get_product_stock(product_id):
    available_quantity, batches = FIFOService.get_available_stock(product_id)
    product = Product.query.get_or_404(product_id)
    
    return jsonify({
        'product_id': product_id,
        'product_name': product.name,
        'available_quantity': available_quantity,
        'unit': product.unit,
        'batches': [
            {
                'id': batch.id,
                'quantity': batch.quantity,
                'received_date': batch.received_date.isoformat(),
                'cost': batch.cost
            } for batch in batches
        ]
    })

# Получить все партии товара
@stock_api.route('/batches', methods=['GET'])
def get_all_batches():
    batches = StockBatch.query.join(Product).all()
    return jsonify([
        {
            'id': batch.id,
            'product_id': batch.product_id,
            'product_name': batch.product.name,
            'quantity': batch.quantity,
            'received_date': batch.received_date.isoformat(),
            'cost': batch.cost
        } for batch in batches
    ]) 

# Отчёт по остаткам на складе на дату (FIFO)
@stock_api.route('/report', methods=['GET'])
def stock_report():
    date_str = request.args.get('date')
    print(f"[DEBUG] /api/stock/report?date={date_str}")
    if not date_str:
        print("[DEBUG] Нет даты!")
        return jsonify({'error': 'Необхідно вказати дату (параметр date)'}), 400
    try:
        report_date = datetime.fromisoformat(date_str)
    except Exception:
        print("[DEBUG] Невірний формат дати!")
        return jsonify({'error': 'Невірний формат дати'}), 400
    products = Product.query.filter_by(type='product').all()
    print(f"[DEBUG] Найдено товаров: {len(products)}")
    report = []
    for product in products:
        available_quantity, batches = FIFOService.get_available_stock_on_date(product.id, report_date)
        print(f"[DEBUG] {product.name}: {available_quantity}")
        report.append({
            'product_id': product.id,
            'product_name': product.name,
            'available_quantity': available_quantity,
            'unit': product.unit
        })
    print(f"[DEBUG] Итоговый отчет: {report}")
    return jsonify(report) 

PRINT_TEMPLATE_STOCK_REPORT_UA = """
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>Звіт по залишках на складі</title>
  <style>
    body { font-family: Arial, sans-serif; }
    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
    th, td { border: 1px solid #333; padding: 6px 10px; text-align: left; }
    th { background: #eee; }
    .header { margin-bottom: 20px; }
    .footer { margin-top: 30px; }
  </style>
</head>
<body>
  <div class=\"header\">
    <h2>Звіт по залишках на складі станом на {{ date }}</h2>
  </div>
  <table>
    <thead>
      <tr>
        <th>№</th>
        <th>Товар</th>
        <th>Залишок</th>
        <th>Од. вим.</th>
      </tr>
    </thead>
    <tbody>
      {% for row in report %}
      <tr>
        <td>{{ loop.index }}</td>
        <td>{{ row.product_name }}</td>
        <td>{{ row.available_quantity }}</td>
        <td>{{ row.unit }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <div class=\"footer\">
    <div>Відповідальний: ____________________</div>
    <div>Підпис: ____________________</div>
  </div>
</body>
</html>
"""

@stock_api.route('/report/print', methods=['GET'])
def print_stock_report():
    date_str = request.args.get('date')
    print(f"[DEBUG] /api/stock/report/print?date={date_str}")
    if not date_str:
        print("[DEBUG] Нет даты!")
        return 'Необхідно вказати дату (параметр date)', 400
    try:
        report_date = datetime.fromisoformat(date_str)
    except Exception:
        print("[DEBUG] Невірний формат дати!")
        return 'Невірний формат дати', 400
    products = Product.query.filter_by(type='product').all()
    print(f"[DEBUG] Найдено товаров: {len(products)}")
    report = []
    for product in products:
        available_quantity, _ = FIFOService.get_available_stock_on_date(product.id, report_date)
        print(f"[DEBUG] {product.name}: {available_quantity}")
        report.append({
            'product_name': product.name,
            'available_quantity': available_quantity,
            'unit': product.unit
        })
    print(f"[DEBUG] Итоговый отчет: {report}")
    html = render_template_string(PRINT_TEMPLATE_STOCK_REPORT_UA, report=report, date=report_date.strftime('%d.%m.%Y'))
    return html 