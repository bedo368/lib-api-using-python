

from  flask import  request

from core.database.database import Database
from routes.authors.datasource.get_author_books import get_author_books
from routes.authors.datasource.get_author_by_id import get_author_by_id


def get_all_autor_books( author_id ):


    page = request.args.get('page', 1, type=int)
    author_id = str(author_id)

    if not isinstance(page , int ) :
        return  {
            "message" : "page is not correct"
        }, 500


    try:


        with  Database() as db :

            author = get_author_by_id(db, author_id)
            books = get_author_books(db , author_id ,page)


            data = author.to_dict()
            data['books'] = books

        return  {
            "data":data
            ,"message":"success"
        },200



    except Exception as e :
        print(e.with_traceback())
        return  {
            "message":"something went wrong",
            "error":e.args
        },500






