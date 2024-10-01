from flask import Blueprint

from routes.user.delete_user import delete_user
from routes.user.get_all_users import get_all_users
from routes.user.add_user import create_user
from routes.user.get_user import get_user
user_bp = Blueprint('user', __name__, url_prefix='/users')




user_bp.add_url_rule('/users', 'create_user', create_user, methods=['POST'])
user_bp.add_url_rule('/users/<uuid:user_id>', 'get_user', get_user, methods=['GET'])
user_bp.add_url_rule('/users/<uuid:user_id>', 'delete_user', delete_user, methods=['DELETE'])
user_bp.add_url_rule('/users', 'get_all_users', get_all_users, methods=['GET'])
