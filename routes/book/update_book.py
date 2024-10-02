from flask import request

from core.database.database import Database
from models.book_model import Book


def update_book(book_id):

    data = request.get_json()
    if not data:
        return {
            "status": "fail",
            "message": "No data provided"

        },400
    count   = data.get("count")
    is_rentable  =  data.get('is_rentable')

    update_query : str = "UPDATE books SET"
    params:list = []

    if not isinstance(is_rentable, bool) and not isinstance(count , int) :
        return {
            "status": "fail",
            "message": "nothing to update !!!"
        } , 400

    if is_rentable is not None and isinstance(is_rentable, bool):
        update_query += " is_rentable = %s ,"
        params.append(is_rentable)

    if count is not None and isinstance(count, int):
        update_query += " count = %s ,"
        params.append(count)

    # Remove the last comma and add the WHERE clause
    update_query = update_query.rstrip(',') + " WHERE id = %s"
    params.append(str(book_id))
    try:

        with Database() as db:
            db.cursor.execute(update_query, params)
            if db.cursor.rowcount == 0:
                return  {
                    "status": "fail",
                    "message": "no book with this id " ,

                }, 404

            db.cursor.execute(Book.get_book_query, (str(book_id),))
            # print(db.cursor.fetchone())
            return {
                "status": "ok",
                "message": "book updated successfully",
                "book" : Book.from_db_record(db.cursor.fetchone()).to_dict()

            },200


    except Exception as e :

        return {
            "status": "fail",
            "message": 'error : '.format(e)

        }, 500

