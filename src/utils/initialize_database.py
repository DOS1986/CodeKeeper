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
from src.db.connection import DatabaseConnection
from src.utils.custom_logger import CustomLogger
from src.db.db_schema import TABLES_SQL, INITIAL_DATA_SQL

# Instantiate the logger
logger = CustomLogger(__name__).logger


class DatabaseInitializer:
    """Facilitates the creation of database tables from SQL schema definitions."""

    def __init__(self, db_connection):
        """
        Initializes the CreateTable utility.

        Args:
            db_connection (DatabaseConnection): The database connection manager.
        """
        self.db_connection = db_connection.connection

    def create_table(self, conn, create_table_sql, table_name):
        """Creates a single table using the provided SQL statement.

        Args:
            conn (sqlite3.Connection): The database connection object.
            create_table_sql (str): SQL statement for creating the table.
            table_name (str): The name of the table to create.

        Returns:
            bool: True if the table was created successfully, False otherwise.
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            logger.info(f"Table '{table_name}' created successfully.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error creating table '{table_name}': {e}")
            return False

    def create_tables(self):
        """Creates all required database tables based on predefined SQL schema definitions.

        Returns:
            bool, list: True if all tables were created successfully, along with any errors encountered.
        """
        errors = []
        conn = self.db_connection  # Directly establish a new connection
        if conn is None:
            logger.error("Error: Unable to establish a database connection.")
            return False, ["Unable to establish a database connection."]

        for table_name, create_table_sql in TABLES_SQL.items():
            success = self.create_table(conn, create_table_sql, table_name)
            if not success:
                errors.append(f"Failed to create table {table_name}.")

        # Don't close the connection here; keep it open for further operations
        return len(errors) == 0, errors

    def load_initial_data(self):
        """Loads initial data into the database from predefined SQL commands.

        This version is optimized for batch insertion for improved performance.

        Returns:
            bool: True if the initial data was loaded successfully, False otherwise.
        """
        conn = self.db_connection  # Ensure to access the connection attribute of db_connection
        if conn is None:
            logger.error("Error: Unable to establish a database connection.")
            return False

        try:
            c = conn.cursor()
            # Begin a transaction explicitly, if desired. Not strictly necessary.
            c.execute("BEGIN")
            for data_sql_list in INITIAL_DATA_SQL.values():
                for data_sql in data_sql_list:
                    c.execute(data_sql)
            conn.commit()  # Commit the transaction after all commands
            logger.info("Initial data loaded successfully.")
            return True
        except sqlite3.Error as e:
            conn.rollback()  # Rollback in case of error
            logger.error(f"Error loading initial data: {e}")
            return False
