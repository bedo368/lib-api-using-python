from flask import Blueprint

from routes.rent.get_all_rent_by_page import get_all_rent_by_page
from routes.rent.rent_book import rent_book
from routes.rent.return_book import return_book

rent_BP = Blueprint("rent", __name__, url_prefix="/rent")


rent_BP.add_url_rule("/rent/<uuid:book_id>", "rent_book", rent_book, methods=["POST"])
rent_BP.add_url_rule(
    "/rent/<uuid:rent_id>", "return_book", return_book, methods=["PATCH"]
)
rent_BP.add_url_rule("/rent", "ge_rents_by_page", get_all_rent_by_page, methods=["GET"])
