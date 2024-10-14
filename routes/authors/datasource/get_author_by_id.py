from core.database.database import Database
from models.auther_model import Author


def get_author_by_id(db :Database, author_id) -> Author:

    get_author_query = """select * from authors where authors.id = %s"""

    try:



        res =  db.execute_query(get_author_query, (author_id,) ,fetchone=True)

        author = Author(author_id=res['id'], name=res['name'] , bio=res['bio'])

        return  author




    except Exception as e:
        raise
