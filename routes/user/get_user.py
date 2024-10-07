from models.user_model import User
import logging

from flask import request, jsonify
from core.database.database import Database  # Your database connection class

def get_user(user_id):

    query = """
           select * from users WHERE id = %s
       """
    params = (str(user_id),)

    try:
        with Database() as db:
            db.cursor.execute(query, params)


            user = User.from_db_record(db.cursor.fetchone())

            return jsonify({'message': f'User {user.name} added with ID {user.id}.', 'data': user.to_dict()}), 201
    except Exception as e:
        logging.error(f"Error in get user: {e}")
        return jsonify({'error': 'Failed to add user.'}), 500