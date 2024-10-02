from flask import Blueprint

from routes.order.create_new_order import create_new_order

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


orders_bp.add_url_rule('/orders', 'create_order', create_new_order, methods=['POST'])

