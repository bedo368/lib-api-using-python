from flask import Blueprint

from routes.book.add_book import add_book
from routes.book.get_book_by_page import get_books_by_page
from routes.book.get_book import get_book
from routes.book.update_book import update_book

book_bp = Blueprint('books', __name__, url_prefix='/books')




book_bp.add_url_rule('/books', 'create_book', add_book, methods=['POST'])
book_bp.add_url_rule('/books', 'get_books_by_page', get_books_by_page, methods=['GET'])
book_bp.add_url_rule('/books/<uuid:book_id>' , 'get_book', get_book, methods=['GET'])
book_bp.add_url_rule('/books/<uuid:book_id>' , 'update_book', update_book, methods=['PATCH'])
