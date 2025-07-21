from flask import Blueprint, request, jsonify, abort
from app.models.models import Order, OrderItem, Customer, Product
from app.db import db
from datetime import datetime

order_api = Blueprint('order_api', __name__, url_prefix='/api/orders')

# Получить список всех заказов
@order_api.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {
            'id': o.id,
            'date': o.date.isoformat(),
            'customer_id': o.customer_id,
            'customer_name': o.customer.name if o.customer else None,
            'status': o.status,
            'items': [
                {
                    'id': item.id,
                    'product_id': item.product_id,
                    'product_name': item.product.name if item.product else None,
                    'quantity': item.quantity,
                    'price': item.price
                } for item in o.items
            ]
        } for o in orders
    ])

# Получить заказ по id
@order_api.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'date': order.date.isoformat(),
        'customer_id': order.customer_id,
        'customer_name': order.customer.name if order.customer else None,
        'status': order.status,
        'items': [
            {
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name if item.product else None,
                'quantity': item.quantity,
                'price': item.price
            } for item in order.items
        ]
    })

# Создать новый заказ с позициями
@order_api.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or not data.get('customer_id') or not data.get('items'):
        abort(400, 'Missing required fields: customer_id, items')
    try:
        order_date = datetime.fromisoformat(data.get('date')) if data.get('date') else datetime.utcnow()
    except Exception:
        abort(400, 'Invalid date format')
    order = Order(
        date=order_date,
        customer_id=data['customer_id'],
        status=data.get('status')
    )
    db.session.add(order)
    db.session.flush()  # Получить id заказа
    for item in data['items']:
        if not item.get('product_id') or not item.get('quantity'):
            abort(400, 'Each item must have product_id and quantity')
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item.get('price')
        )
        db.session.add(order_item)
    db.session.commit()
    return jsonify({'id': order.id}), 201

# Обновить заказ и его позиции
@order_api.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    if not data:
        abort(400, 'No input data')
    if 'date' in data:
        try:
            order.date = datetime.fromisoformat(data['date'])
        except Exception:
            abort(400, 'Invalid date format')
    if 'customer_id' in data:
        order.customer_id = data['customer_id']
    if 'status' in data:
        order.status = data['status']
    # Обновление позиций заказа (перезапись)
    if 'items' in data:
        # Удаляем старые позиции
        OrderItem.query.filter_by(order_id=order.id).delete()
        for item in data['items']:
            if not item.get('product_id') or not item.get('quantity'):
                abort(400, 'Each item must have product_id and quantity')
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item.get('price')
            )
            db.session.add(order_item)
    db.session.commit()
    return jsonify({'result': 'success'})

# Удалить заказ и его позиции
@order_api.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    OrderItem.query.filter_by(order_id=order.id).delete()
    db.session.delete(order)
    db.session.commit()
    return jsonify({'result': 'deleted'}) 