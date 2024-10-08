from flask import Blueprint

from routes import rent
from routes.rent.rent_book import rent_book

rent_BP = Blueprint('rent', __name__, url_prefix="/rent")


rent_BP.add_url_rule("/rent/<uuid:book_id>", "rent_new_book" , rent_book , methods=["POST"])