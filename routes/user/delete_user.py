from core.database.database import Database


def delete_user(user_id):

    """
    in real time data base this is not working this is just for test
    no one should be able to delete user data we will keep it and lie about delete it  hahahahahaha
    """
    query = "DELETE FROM users WHERE id = %s "

    try:
        params = ( str(user_id),)
        with Database() as db:
            db.cursor.execute(query, params )


        if db.cursor.rowcount == 0:

            return {
                "message": f"User with id {user_id} does not exist."
            }, 404  # Return 404 Not Found status


        return {
            "message": f"User with id {user_id} deleted successfully",

        },200


    except Exception as e:
        return  {
            "message":e.args,

        }, 500

