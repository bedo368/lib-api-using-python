from datetime import datetime

from flask import request

from routes.rent.data_source_opreation.return_book_database import return_book_database
from routes.rent.validate_request.return_validate import ReturnBookValidateSchema


def return_book(rent_id):

    try:
        print(datetime.now())
        rent_id = str(rent_id)
        data = request.get_json()
        ReturnBookValidateSchema().load(data)

        res = return_book_database(
            {
                "rent_id": rent_id,
                "fine": data.get("fine"),
                "return_date": data.get("return_date"),
            }
        )

        return {"message": "success", "data": res}, 200

        return {}, 200

    except Exception as e:
        return {"message": "error happened ", "error": e.args}, 500
