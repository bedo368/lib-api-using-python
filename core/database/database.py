# database.py

import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DATABASE_HOST', 'localhost')
        self.port = os.getenv('DATABASE_PORT', 5432)
        self.dbname = os.getenv('DATABASE_NAME')
        self.user = os.getenv('DATABASE_USER')
        self.password = os.getenv('DATABASE_PASSWORD')
        self.conn = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            # Use RealDictCursor to get results as dictionaries
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            return self
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is not None:
                # An exception occurred, rollback
                self.conn.rollback()
            else:
                # No exception, commit the transaction
                self.conn.commit()
            self.conn.close()

    def execute_query(self, query, params=None, fetch=False, fetchone=False):
        """
        Execute a SQL query.
        :param query: SQL query to execute.
        :param params: Tuple of parameters to pass to the query.
        :param fetch: Boolean indicating whether to fetch all results.
        :param fetchone: Boolean indicating whether to fetch one result.
        :return: Fetched data if fetch is True, else None.
        """
        try:
            self.cursor.execute(query, params)
            if fetch:
                return self.cursor.fetchall()
            if fetchone:
                return self.cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Database query error: {e}")
            self.conn.rollback()
            raise e

    def execute_many(self, query, params_list):
        """
        Execute a SQL query with multiple sets of parameters.
        :param query: SQL query to execute.
        :param params_list: List of parameter tuples.
        """
        try:
            self.cursor.executemany(query, params_list)
        except psycopg2.Error as e:
            print(f"Database query error: {e}")
            self.conn.rollback()
            raise e
