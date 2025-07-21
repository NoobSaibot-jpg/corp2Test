from app.db import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    edrpou = db.Column(db.String)  # ЕДРПО
    # Новые поля:
    type = db.Column(db.String)
    email = db.Column(db.String)
    ipn = db.Column(db.String)
    bank_name = db.Column(db.String)
    bank_account = db.Column(db.String)
    mfo = db.Column(db.String)
    contact_person = db.Column(db.String)
    contact_phone = db.Column(db.String)
    contact_email = db.Column(db.String)
    discount = db.Column(db.Float)
    credit_limit = db.Column(db.Float)
    payment_terms = db.Column(db.String)
    notes = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    postal_code = db.Column(db.String)
    website = db.Column(db.String)
    tax_system = db.Column(db.String)
    vat_payer = db.Column(db.Boolean)
    vat_certificate = db.Column(db.String)  # Номер свидетельства плательщика НДС
    orders = db.relationship('Order', backref='customer', lazy=True)
    goods_issues = db.relationship('GoodsIssue', backref='customer', lazy=True)
    goods_receipts = db.relationship('GoodsReceipt', backref='supplier', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)  # 'product' или 'service'
    unit = db.Column(db.String)
    price = db.Column(db.Float)
    # Новые поля:
    description = db.Column(db.String)
    barcode = db.Column(db.String)
    weight = db.Column(db.Float)
    volume = db.Column(db.Float)
    manufacturer = db.Column(db.String)
    country = db.Column(db.String)
    group = db.Column(db.String)
    subgroup = db.Column(db.String)
    vat_rate = db.Column(db.Integer)
    min_stock = db.Column(db.Float)
    max_stock = db.Column(db.Float)
    supplier = db.Column(db.String)
    supplier_price = db.Column(db.Float)
    notes = db.Column(db.String)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    goods_receipt_items = db.relationship('GoodsReceiptItem', backref='product', lazy=True)
    goods_issue_items = db.relationship('GoodsIssueItem', backref='product', lazy=True)
    stock_batches = db.relationship('StockBatch', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    status = db.Column(db.String)
    items = db.relationship('OrderItem', backref='order', lazy=True)
    invoice = db.relationship('Invoice', backref='order', uselist=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float)

class GoodsReceipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.String)
    supplier_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    contract = db.Column(db.String)
    warehouse = db.Column(db.String)
    organization = db.Column(db.String)
    operation_type = db.Column(db.String)
    responsible = db.Column(db.String)
    comment = db.Column(db.String)
    pricing_note = db.Column(db.String)
    items = db.relationship('GoodsReceiptItem', backref='goods_receipt', lazy=True)

class GoodsReceiptItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_receipt_id = db.Column(db.Integer, db.ForeignKey('goods_receipt.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float)

class GoodsIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    contract = db.Column(db.String)
    warehouse = db.Column(db.String)
    organization = db.Column(db.String)
    operation_type = db.Column(db.String)
    responsible = db.Column(db.String)
    comment = db.Column(db.String)
    pricing_note = db.Column(db.String)
    items = db.relationship('GoodsIssueItem', backref='goods_issue', lazy=True)
    tax_invoice = db.relationship('TaxInvoice', backref='goods_issue', uselist=False)

class GoodsIssueItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_issue_id = db.Column(db.Integer, db.ForeignKey('goods_issue.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float)

class TaxInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_issue_id = db.Column(db.Integer, db.ForeignKey('goods_issue.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.String)

class StockBatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    received_date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Float, nullable=False) 