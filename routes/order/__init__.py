from flask import Blueprint

from routes.order.create_new_order import create_new_order
from routes.order.get_orders_by_page import get_orders_by_page

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


orders_bp.add_url_rule('/orders', 'create_order', create_new_order, methods=['POST'])
orders_bp.add_url_rule('/orders', 'get_orders_by_page', get_orders_by_page, methods=['GET'])

