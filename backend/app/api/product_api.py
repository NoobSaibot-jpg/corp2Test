from flask import Blueprint, request, jsonify, abort
from app.models.models import Product
from app.db import db

product_api = Blueprint('product_api', __name__, url_prefix='/api/products')

# Получить список всех товаров/услуг
@product_api.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'type': p.type,
            'unit': p.unit,
            'price': p.price,
            'description': p.description,
            'barcode': p.barcode,
            'weight': p.weight,
            'volume': p.volume,
            'manufacturer': p.manufacturer,
            'country': p.country,
            'group': p.group,
            'subgroup': p.subgroup,
            'vat_rate': p.vat_rate,
            'min_stock': p.min_stock,
            'max_stock': p.max_stock,
            'supplier': p.supplier,
            'supplier_price': p.supplier_price,
            'notes': p.notes
        } for p in products
    ])

# Получить товар/услугу по id
@product_api.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'type': product.type,
        'unit': product.unit,
        'price': product.price,
        'description': product.description,
        'barcode': product.barcode,
        'weight': product.weight,
        'volume': product.volume,
        'manufacturer': product.manufacturer,
        'country': product.country,
        'group': product.group,
        'subgroup': product.subgroup,
        'vat_rate': product.vat_rate,
        'min_stock': product.min_stock,
        'max_stock': product.max_stock,
        'supplier': product.supplier,
        'supplier_price': product.supplier_price,
        'notes': product.notes
    })

# Создать новый товар/услугу
@product_api.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'type')):
        abort(400, 'Missing required fields')
    product = Product(
        name=data['name'],
        type=data['type'],
        unit=data.get('unit'),
        price=data.get('price'),
        description=data.get('description'),
        barcode=data.get('barcode'),
        weight=data.get('weight'),
        volume=data.get('volume'),
        manufacturer=data.get('manufacturer'),
        country=data.get('country'),
        group=data.get('group'),
        subgroup=data.get('subgroup'),
        vat_rate=data.get('vat_rate'),
        min_stock=data.get('min_stock'),
        max_stock=data.get('max_stock'),
        supplier=data.get('supplier'),
        supplier_price=data.get('supplier_price'),
        notes=data.get('notes')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id}), 201

# Обновить товар/услугу
@product_api.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    if not data:
        abort(400, 'No input data')
    product.name = data.get('name', product.name)
    product.type = data.get('type', product.type)
    product.unit = data.get('unit', product.unit)
    product.price = data.get('price', product.price)
    product.description = data.get('description', product.description)
    product.barcode = data.get('barcode', product.barcode)
    product.weight = data.get('weight', product.weight)
    product.volume = data.get('volume', product.volume)
    product.manufacturer = data.get('manufacturer', product.manufacturer)
    product.country = data.get('country', product.country)
    product.group = data.get('group', product.group)
    product.subgroup = data.get('subgroup', product.subgroup)
    product.vat_rate = data.get('vat_rate', product.vat_rate)
    product.min_stock = data.get('min_stock', product.min_stock)
    product.max_stock = data.get('max_stock', product.max_stock)
    product.supplier = data.get('supplier', product.supplier)
    product.supplier_price = data.get('supplier_price', product.supplier_price)
    product.notes = data.get('notes', product.notes)
    db.session.commit()
    return jsonify({'result': 'success'})

# Удалить товар/услугу
@product_api.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'result': 'deleted'}) 