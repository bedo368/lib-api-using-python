from routes.rent.data_source_opreation.rent_book_database_opreation import rent_book_database
from routes.rent.validate_request.rent_book_request import RentBookRequestSchema

from  flask import  request
def rent_book( book_id ):


    book_id = str(book_id)

    try:
        data = request.get_json()
        RentBookRequestSchema().load(data)

        res =  rent_book_database({
            "book_id": book_id,
            "user_id": data.get("user_id"),
            "time_by_days": data.get("time_by_days"),
        })

        print(res)
        return {
            'message' : 'success',
            'data' : res
        }
    except Exception as err :
        print(e.with_traceback())

        return  {
            "message" :f" error happened : {err} ",
            "error": err.args
        }, 500
