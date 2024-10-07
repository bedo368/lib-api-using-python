from core.database.database import Database

from models.book_model import Book
def get_book(book_id) :
    book_id = str(book_id)

    get_query = Book.get_book_query
    try:
        with Database() as db:
            db.cursor.execute(get_query  , (book_id,))

            res = db.cursor.fetchone()

            if res is None:
                return {
                    "message" : "Book not found",
                },404

            book = Book.from_db_record(res).to_dict()

            return  {
                "message": "success",
                "data": book
            }, 200
    except Exception as e:

        return {
            "message": "error : {}".format(e),

        }, 500
