from .product_api import product_api
from .customer_api import customer_api
from .order_api import order_api
from .invoice_api import invoice_api
from .goods_receipt_api import goods_receipt_api
from .goods_issue_api import goods_issue_api
from .stock_api import stock_api

def register_blueprints(app):
    app.register_blueprint(product_api)
    app.register_blueprint(customer_api)
    app.register_blueprint(order_api)
    app.register_blueprint(invoice_api)
    app.register_blueprint(goods_receipt_api)
    app.register_blueprint(goods_issue_api)
    app.register_blueprint(stock_api) 