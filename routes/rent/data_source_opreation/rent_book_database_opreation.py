from datetime import datetime, timedelta
from typing import Any, Text

from marshmallow.fields import Float

from core.database.database import Database


def rent_book_database(data: dict[Text, Any]) -> dict[Text, Any]:
    book_id = data.get("book_id")
    user_id = data.get("user_id")
    time_by_days = data.get("time_by_days")
    rent_date = datetime.now()
    print(user_id)
    due_date = rent_date + timedelta(days=float(time_by_days))
    rent_query = """
    insert into rent ( user_id, book_id, rent_date, due_date, status) values (%s, %s, %s, %s, %s) 
    RETURNING id;
    
    
    """

    try:
        with Database() as db:

            db.cursor.execute(
                rent_query,
                [str(user_id), str(book_id), rent_date, due_date, "Rented"],
            )
            rent_id = db.cursor.fetchone()["id"]

        return {"id": rent_id}

    except Exception as e:
        raise
