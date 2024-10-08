from core.database.database import Database


def return_book_database ( data : dict ) -> dict:


    return_query = """
    update rent 
    set return_date = %s ,
    status = 'Returned',
    fine = %s
    where id = %s
    returning * 
     """

    try:

        with Database() as db :

            res =  db.execute_query(return_query, (data['return_date'], data['fine'], data['rent_id']) , fetchone=True)

            print(res)
            return  {
                "rent_id": res
            }






    except:
        raise