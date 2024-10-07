from netaddr.ip.iana import query

from core.database.database import Database
from models.book_model import Book

from flask import request


def get_books_by_page():
    data = request.get_json()
    page = data.get("page", 1)
    page = page - 1

    fetch_books_query = """ SELECT b.*, a.name AS author_name
              FROM books b
              JOIN authors a ON b.author_id = a.id
              OFFSET %s ROWS FETCH NEXT 5 ROWS ONLY;
          """
    if not isinstance(page, int):
        return {
            "message": "please enter valid page number"
        }, 400



    try:
        skip_num = page * 5
        with Database() as db:

            db.cursor.execute(fetch_books_query, (skip_num,))

            books = [Book.from_db_record(b).to_dict() for b in db.cursor.fetchall()]

            if books.__len__() == 0:
                return {
                    "message": "no more books"
                }, 404

            return {
                "message": "success",
                "data": books
            }

    except Exception as e:
        return {
            "message": 'error : '.format(e),

        }, 500
