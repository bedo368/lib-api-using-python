from core.database.database import Database


def get_rents_by_page_database(data):
    get_rent_query = """
           SELECT 
        rent.id AS rent_id, 
        rent.rent_date , 
        rent.return_date,
        rent.due_date,
        rent.status,
        users.id AS user_id, 
        books.id AS book_id,
        rent.fine
    FROM rent
    JOIN users ON rent.user_id = users.id
    JOIN books ON rent.book_id = books.id
    OFFSET %s ROWS FETCH NEXT 5 ROWS ONLY
    ;

        """

    page = data["page"]

    try:

        with Database() as db:

            db.cursor.execute(get_rent_query, (page,))
            res = db.cursor.fetchall()

            return res

    except Exception as e:
        raise
