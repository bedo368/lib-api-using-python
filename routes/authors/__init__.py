from flask import Blueprint

from routes import authors
from routes.authors.get_all_autor_books import get_all_autor_books
from routes.authors.get_author import get_author

author_bp = Blueprint('authors', __name__ ,url_prefix='/authors')



author_bp.add_url_rule('/authors/<uuid:author_id>', view_func=get_author , methods=['GET'])
author_bp.add_url_rule('/authors/<uuid:author_id>/books', view_func=get_all_autor_books, methods=['GET'])
