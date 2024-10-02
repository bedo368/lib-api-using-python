

from  flask import  request
from marshmallow import ValidationError

from core.database.database import Database
from routes.order.validate_reqests.vlidate_get_orders_by_page import ValidatePageSchema


def get_orders_by_page():
    query = """
        SELECT o.*, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        OFFSET %s ROWS FETCH NEXT 5 ROWS ONLY;
    """

    try:

        data = request.get_json()
        ValidatePageSchema().load(data)

        with Database() as db:
            pass

    except ValidationError as err:
        return  {"errors":err.messages , "message":"error on validation check errors key for more detail"}, 400
    except Exception as err:
        return  {
            "message": str(err)

        }, 500
