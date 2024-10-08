from flask import Blueprint

from routes import rent
from routes.rent.rent_book import rent_book
from routes.rent.return_book import return_book

rent_BP = Blueprint('rent', __name__, url_prefix="/rent")


rent_BP.add_url_rule("/rent/<uuid:book_id>", "rent_book" , rent_book , methods=["POST"])
rent_BP.add_url_rule("/rent/<uuid:rent_id>", "return_book" , return_book , methods=["PATCH"])
