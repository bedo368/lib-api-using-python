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
    category_name = data.get('category_name')
    author_name = data.get('author_name')
    is_rentable = data.get('is_rentable', True)  # Default to True if not provided

    # Check if all required fields are present
    if not title or not count or not category_name or not author_name:
        return jsonify({'error': 'Missing required fields'}), 400


    # SQL queries
    check_category_query = """
        SELECT id FROM categories WHERE name = %s
    """
    check_author_query = """
        SELECT id FROM authors WHERE name = %s
    """
    insert_book_query = """
        INSERT INTO books (id, title, count, author_id, is_rentable)
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        with Database() as db:


            #  if the book exist on data base
            seslct_book = """SELECT books.* 
                            FROM books 
                            JOIN authors ON books.author_id = authors.id 
                            WHERE books.title = %s 
                            AND authors.name = %s; """
            db.cursor.execute(seslct_book, (title, author_name))


            book = db.cursor.fetchone()
            if book:
                print(book , "fffdafdsfasdfds")
                db.cursor.execute(""" UPDATE books SET count = count + %s WHERE id = %s """ , [count, book.get('id')])

                return {
                    "message": "Book was  already exist and increment it's count ",
                },200
            else :
                # Check if the category exists
                db.cursor.execute(check_category_query, (category_name,))
                category = db.cursor.fetchone()

                if category is None:
                    db.cursor.execute("INSERT INTO categories (title) VALUES (%s)", (category_name,))
                    print("fffff")
                    db.cursor.execute("Select * from categories where title = %s", (category_name,))
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
                db.cursor.execute(insert_book_query, (str(book_id), title, count, author_id, is_rentable))
                db.execute_query("Insert into book_categories (book_id, category_id) VALUES (%s, %s)", (str(book_id), str(category_id)))

            # Success response
            return jsonify({
                'message': f'Book "{title}" added successfully with category "{category_name}" and author "{author_name}".',
                'book_id': str(book_id)
            }), 201

    except Exception as e:

        print(e.with_traceback())
        # Error handling
        return jsonify({'error': f'Failed to add book: {str(e)}'}), 500

