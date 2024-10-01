from venv import logger

from  flask import  request , jsonify

from core.database.database import Database
from models.user_model import User


def get_all_users():

    query = "SELECT * from users"

    try:
        with Database() as db:
            print("start")
            db.cursor.execute(query)
            users = db.cursor.fetchall()
            print(users)
            return {
                "status": "success",
                "data": [ User.from_db_record(user).to_dict() for user in users ]
            },200
    except Exception as e:
        logger.error(e.args)
        return {
            "message": "Something went wrong",
        },500
