from flask import Blueprint, request, jsonify, abort
from app.models.models import Customer
from app.db import db
import traceback

customer_api = Blueprint('customer_api', __name__, url_prefix='/api/customers')

# Получить список всех клиентов
@customer_api.route('/', methods=['GET'])
def get_customers():
    try:
        customers = Customer.query.all()
        return jsonify([
            {
                'id': c.id,
                'name': c.name,
                'type': c.type,
                'address': c.address,
                'phone': c.phone,
                'email': c.email,
                'edrpou': c.edrpou,
                'ipn': c.ipn,
                'bank_name': c.bank_name,
                'bank_account': c.bank_account,
                'mfo': c.mfo,
                'contact_person': c.contact_person,
                'contact_phone': c.contact_phone,
                'contact_email': c.contact_email,
                'discount': c.discount,
                'credit_limit': c.credit_limit,
                'payment_terms': c.payment_terms,
                'notes': c.notes,
                'country': c.country,
                'city': c.city,
                'postal_code': c.postal_code,
                'website': c.website,
                'tax_system': c.tax_system,
                'vat_payer': c.vat_payer,
                'vat_certificate': c.vat_certificate
            } for c in customers
        ])
    except Exception as e:
        print(f"[ERROR] get_customers: {e}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

# Получить клиента по id
@customer_api.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'type': customer.type,
        'address': customer.address,
        'phone': customer.phone,
        'email': customer.email,
        'edrpou': customer.edrpou,
        'ipn': customer.ipn,
        'bank_name': customer.bank_name,
        'bank_account': customer.bank_account,
        'mfo': customer.mfo,
        'contact_person': customer.contact_person,
        'contact_phone': customer.contact_phone,
        'contact_email': customer.contact_email,
        'discount': customer.discount,
        'credit_limit': customer.credit_limit,
        'payment_terms': customer.payment_terms,
        'notes': customer.notes,
        'country': customer.country,
        'city': customer.city,
        'postal_code': customer.postal_code,
        'website': customer.website,
        'tax_system': customer.tax_system,
        'vat_payer': customer.vat_payer,
        'vat_certificate': customer.vat_certificate
    })

# Создать нового клиента
@customer_api.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data or not data.get('name'):
        abort(400, 'Missing required field: name')
    customer = Customer(
        name=data['name'],
        type=data.get('type'),
        address=data.get('address'),
        phone=data.get('phone'),
        email=data.get('email'),
        edrpou=data.get('edrpou'),
        ipn=data.get('ipn'),
        bank_name=data.get('bank_name'),
        bank_account=data.get('bank_account'),
        mfo=data.get('mfo'),
        contact_person=data.get('contact_person'),
        contact_phone=data.get('contact_phone'),
        contact_email=data.get('contact_email'),
        discount=data.get('discount'),
        credit_limit=data.get('credit_limit'),
        payment_terms=data.get('payment_terms'),
        notes=data.get('notes'),
        country=data.get('country'),
        city=data.get('city'),
        postal_code=data.get('postal_code'),
        website=data.get('website'),
        tax_system=data.get('tax_system'),
        vat_payer=data.get('vat_payer'),
        vat_certificate=data.get('vat_certificate')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id}), 201

# Обновить клиента
@customer_api.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    if not data:
        abort(400, 'No input data')
    customer.name = data.get('name', customer.name)
    customer.type = data.get('type', customer.type)
    customer.address = data.get('address', customer.address)
    customer.phone = data.get('phone', customer.phone)
    customer.email = data.get('email', customer.email)
    customer.edrpou = data.get('edrpou', customer.edrpou)
    customer.ipn = data.get('ipn', customer.ipn)
    customer.bank_name = data.get('bank_name', customer.bank_name)
    customer.bank_account = data.get('bank_account', customer.bank_account)
    customer.mfo = data.get('mfo', customer.mfo)
    customer.contact_person = data.get('contact_person', customer.contact_person)
    customer.contact_phone = data.get('contact_phone', customer.contact_phone)
    customer.contact_email = data.get('contact_email', customer.contact_email)
    customer.discount = data.get('discount', customer.discount)
    customer.credit_limit = data.get('credit_limit', customer.credit_limit)
    customer.payment_terms = data.get('payment_terms', customer.payment_terms)
    customer.notes = data.get('notes', customer.notes)
    customer.country = data.get('country', customer.country)
    customer.city = data.get('city', customer.city)
    customer.postal_code = data.get('postal_code', customer.postal_code)
    customer.website = data.get('website', customer.website)
    customer.tax_system = data.get('tax_system', customer.tax_system)
    customer.vat_payer = data.get('vat_payer', customer.vat_payer)
    customer.vat_certificate = data.get('vat_certificate', customer.vat_certificate)
    db.session.commit()
    return jsonify({'result': 'success'})

# Удалить клиента
@customer_api.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'result': 'deleted'}) 