"""
MIT License

Copyright (c) 2024 David Southwood

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sqlite3
from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class DatabaseConnection:
    """
    Manages database connections and queries for the application.

    This class provides methods to connect to and interact with the database,
    including executing queries and managing the connection lifecycle.

    Attributes:
        db_file (str): The file path to the SQLite database.
        connection (sqlite3.Connection): The SQLite connection object.
    """

    def __init__(self, db_file):
        """
        Initializes the database connection.

        Parameters:
            db_file (str): The file path to the SQLite database.
        """
        self.db_file = db_file
        self.connection = None
        self.open_connection()

    def open_connection(self):
        """Open the database connection if it isn't already open."""
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_file)
                logger.info(f"Connected to SQLite database: {self.db_file}")
            except sqlite3.Error as e:
                logger.error(f"Failed to connect to SQLite database: {e}")
                raise

    def close_connection(self):
        """Close the database connection if it's open."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("SQLite database connection closed")

    def __enter__(self):
        self.open_connection()  # Ensure connection is open
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def execute_query(self, query, params=None, is_select=False):
        """
        Executes a SQL query on the database.

        This method can execute both action (e.g., INSERT, UPDATE, DELETE) and
        selection (SELECT) queries. For selection queries, it returns all fetched rows;
        for action queries, it returns the number of rows affected.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to substitute into the query.
            is_select (bool): True if the query is a SELECT query, False otherwise.

        Returns:
            list | int: The fetched rows for SELECT queries, or the number of rows affected
            for action queries.

        Raises:
            RuntimeError: If the query execution fails.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                logger.info("Executing query with parameters...")
                cursor.execute(query, params)
            else:
                logger.info("Executing query...")
                cursor.execute(query)

            if is_select:
                logger.info(f"Query executed successfully: {query}")
                return cursor.fetchall()  # Return all rows for a SELECT query
            else:
                self.connection.commit()  # Commit changes for non-SELECT queries
                logger.info(f"Query executed successfully. Rows affected: {cursor.rowcount}")
                return cursor.rowcount  # Return the number of rows affected

        except sqlite3.Error as e:
            logger.error(f"Database error: {e}. Query: {query}")
            raise RuntimeError(f"Database operation failed: {e}")
