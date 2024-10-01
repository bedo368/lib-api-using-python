from flask import Blueprint

from routes.book.add_book import add_book

book_bp = Blueprint('books', __name__, url_prefix='/books')




book_bp.add_url_rule('/books', 'create_book', add_book, methods=['POST'])
