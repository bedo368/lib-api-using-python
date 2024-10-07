from core.database.database import Database
from flask import request, jsonify
import uuid

from models.auther_model import Author
from models.category_model import Category


def add_book():
    # Get the request data
    data = request.get_json()
    title = data.get('title')
    count = data.get('count')
    language = data.get('language')
    category_name = data.get('category_name')
    author_name = data.get('author_name')
    is_rentable = data.get('is_rentable', True)  # Default to True if not provided

    # Check if all required fields are present
    if not title or not count or not category_name or not author_name:
        return jsonify({'message': 'Missing required fields'}), 400


    # SQL queries
    check_category_query = """
        SELECT id FROM categories WHERE name = %s
    """
    check_author_query = """
        SELECT id FROM authors WHERE name = %s
    """
    insert_book_query = """
        INSERT INTO books (id, title, count, author_id, is_rentable , language)
        VALUES (%s, %s, %s, %s, %s , %s)
    """

    try:
        with Database() as db:

            # Check if the category exists
            db.cursor.execute(check_category_query, (category_name,))
            category = db.cursor.fetchone()

            if category is None:
                db.cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
                db.cursor.execute("Select * from categories where name = %s", (category_name,))
                category = Category.from_db_record(db.cursor.fetchone())
                print(category.id)
                category_id = category.id
            else:
                category_id = category['id']

            # Get the category_id from the result
            # Check if the author exists
            db.cursor.execute(check_author_query, (author_name,))
            author = db.cursor.fetchone()

            if author is None:
                db.cursor.execute("INSERT INTO authors (name) VALUES (%s)", (author_name,))
                db.cursor.execute("Select * from authors where (name) = %s", (author_name,))

                author = Author.from_db_record(db.cursor.fetchone())
                author_id = author.id
            else:
                author_id = author['id']




            # Generate a UUID for the new book
            book_id = uuid.uuid4()

            # Insert the book into the database
            db.cursor.execute(insert_book_query, (str(book_id), title, count, author_id, is_rentable , language))
            db.cursor.execute("Insert into book_categories (book_id, category_id) VALUES (%s, %s)", (str(book_id), str(category_id)))
        # Success response
        return jsonify({
            'message': f'Book "{title}" added successfully with category "{category_name}" and author "{author_name}".',
            'data': str(book_id)
        }), 201

    except Exception as e:

        # Error handling
        return jsonify({'error': f'Failed to add book: {str(e)}'}), 500

