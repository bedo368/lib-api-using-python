from core.database.database import Database
from routes.authors.datasource.get_author_by_id import get_author_by_id


def get_author(author_id):


    try:
        with Database() as db:
            res =  get_author_by_id(db=db,author_id= str( author_id))

        return {
            "message": "success",
            "data": res.to_dict()
        },200



    except Exception as e :
        return  {
            "message":"error happened while trying to get author",
            "error": e.args

        }, 500
