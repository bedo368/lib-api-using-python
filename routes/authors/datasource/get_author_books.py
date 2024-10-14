from core.database.database import Database
from typing import  List

from models.book_model import Book
from routes import book


def get_author_books( db : Database,author_id , page) ->List:
    offset = page * 5
    q = """
    select * from books where books.author_id = %s 
    OFFSET %s ROWS FETCH NEXT 5 ROWS ONLY
    """
    try:
        res = db.cursor.execute(q, (author_id, offset),)


        res = db.cursor.fetchall()
        return [{
            "book_id": b["id"],
            "title":b["title"],
            "count":b["count"],
            "is_rentable":b["is_rentable"],
            "language":b["language"]
        } for b in res]

    except Exception as e:
        raise
