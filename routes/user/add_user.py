
from flask import request, jsonify
from core.database.database import Database
from models.user_model import User
import logging


def create_user():
    print("fuck u")
    """
        Add a new user.
        Expected JSON payload:
        {
            "name": "John Doe",
            "phone_number": "1234567890",
            "email": "john.doe@example.com",
            "address": "123 Main St",
            "membership_type_id": uuid
        }
        """
    data = request.get_json()
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    address = data.get('address')
    membership_type_id = data.get('membership_type_id')

    if not name or not phone_number:
        return jsonify({'error': 'Name and phone number are required.'}), 400

    insert_query = """
            INSERT INTO users (name, phone_number, email, address  )
            VALUES (%s, %s, %s, %s ) RETURNING id, date_joined;
        """
    params = (name, phone_number, email, address )

    try:
        with Database() as db:
            result = db.execute_query(insert_query, params, fetchone=True)
            user_id = result['id']
            date_joined = result['date_joined']
            logging.info(f"User created with ID: {user_id}")

            # Create a User instance using from_db_record
            user = User(
                user_id=user_id,
                name=name,
                phone_number=phone_number,
                email=email,
                address=address,
                date_joined=date_joined
            )

            return jsonify({'message': f'User {user.name} added with ID {user.id}.', 'data': user.to_dict()}), 201
    except Exception as e:
        logging.error(f"Error in add_user: {e}")
        return jsonify({'error': e.args}), 500