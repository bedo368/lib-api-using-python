from core.database.database import Database

from models.book_model import Book
def get_book(book_id) :
    book_id = str(book_id)

    get_query = """
        SELECT b.*, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
         WHERE b.id = %s;
    """
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
                "book": book
            }, 200
    except Exception as e:
        print(e.with_traceback())

        return {
            "message": "error : {}".format(e),

        }, 500
