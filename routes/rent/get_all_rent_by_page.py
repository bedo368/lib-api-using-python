from flask import request

from routes.rent.data_source_opreation.get_rents_by_page_database import get_rents_by_page_database
from routes.rent.validate_request.rent_page_validate import RentPageValidate


def get_all_rent_by_page():

    try:
        data = request.get_json()
        RentPageValidate().load(data)

        res = get_rents_by_page_database(
            data={
                "page": data.get("page"),
            }
        )

        return {"message": "success", "data": res}, 200
    except Exception as e:
        return {"status": "fail", "message": "error happened ", "error": e.args}
