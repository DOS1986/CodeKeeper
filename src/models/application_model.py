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


class ApplicationModel:
    """
    Represents the core application model in the MVC architectural pattern. This class is responsible for managing the data logic of the application, including interactions with the database for operations related to code snippets.

    The ApplicationModel provides an interface for retrieving, adding, updating, and deleting snippets from the database, abstracting the specifics of SQL queries and database access from the rest of the application.

    Attributes:
        db_connection: A database connection object that provides a connection to the application's database. This connection is used to execute SQL queries and interact with the database.

    Methods:
        get_all_snippets(): Retrieves all code snippets from the database, returning them in a structured format that can be easily used by the application's view for display.
    """

    def __init__(self, db_connection):
        """
        Initializes the ApplicationModel with a database connection.

        Args:
            db_connection: The database connection resource to be used by the application model.
        """
        self.db_connection = db_connection.connection

    def get_all_snippets(self):
        """
        Retrieves all snippets from the database.

        Returns:
            A list of dictionaries, each representing a snippet with its details.
        """
        snippets = []
        query = "SELECT snippets.id, snippets.title, snippets.code, snippets.language_id, languages.name AS language, snippets.category_id, categories.name AS category FROM snippets JOIN languages ON snippets.language_id = languages.id JOIN categories ON snippets.category_id = categories.id ORDER BY snippets.title ASC"

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                snippet = {
                    "id": row[0],
                    "title": row[1],
                    "code": row[2],
                    "language_id": row[3],
                    "language": row[4],
                    "category_id": row[5],
                    "category": row[6]
                }
                snippets.append(snippet)

        except Exception as e:
            print(f"Failed to fetch snippets: {e}")
            # Optionally, log this error or handle it as per your application's error management strategy

        return snippets

    def get_snippet(self, snippet_id):
        """
        Retrieves a single snippet from the database by its ID, including language name and category name.

        Parameters:
            snippet_id (int): The ID of the snippet to retrieve.

        Returns:
            A dictionary containing the snippet data or None if not found.
        """
        params = (snippet_id,)
        query = """SELECT snippets.id, snippets.title, snippets.code, snippets.language_id, languages.name AS language, snippets.category_id, categories.name AS category FROM snippets JOIN languages ON snippets.language_id = languages.id JOIN categories ON snippets.category_id = categories.id WHERE snippets.id = ?"""

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            snippet = cursor.fetchone()
            if snippet is not None:
                return {
                    "id": snippet[0],
                    "title": snippet[1],
                    "code": snippet[2],
                    "language_id": snippet[3],
                    "language": snippet[4],
                    "category_id": snippet[5],
                    "category": snippet[6]
                }
            return None
        except Exception as e:
            print(f"Error retrieving snippet: {e}")
            return None

    def get_language_specific_categories(self, language_id):
        """Retrieve shared categories from the database."""
        language_specific_categories = []
        params = (language_id,)
        query = """SELECT c.id, c.name FROM categories c JOIN languages_categories lc ON c.id = lc.category_id WHERE lc.language_id = ?;"""

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            for row in rows:
                language_specific_categories.append({'id': row[0], 'name': row[1]})
        except Exception as e:
            print(f"Error retrieving shared categories: {e}")
            # Handle error or log
        print(language_specific_categories)
        return language_specific_categories

    def get_general_categories(self):
        """Retrieve general categories from the database."""
        general_categories = []
        query = """SELECT c.id, c.name FROM categories c WHERE NOT EXISTS (SELECT 1 FROM languages_categories lc WHERE lc.category_id = c.id);"""

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                general_categories.append({'id': row[0], 'name': row[1]})
        except Exception as e:
            print(f"Error retrieving general categories: {e}")
            # Handle error or log
        print(general_categories)
        return general_categories

    def get_all_language_ids(self):
        """Retrieve all language IDs from the database."""
        query = "SELECT id FROM languages;"
        language_ids = []

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                language_ids.append(row[0])  # Assuming 'id' is the first column
        except Exception as e:
            print(f"Error retrieving language IDs: {e}")
            # Handle error or log as needed
        print(language_ids)
        return language_ids

    def get_all_languages(self):
        """Retrieve all languages with their IDs and names from the database."""
        query = "SELECT id, name FROM languages;"
        languages = {}

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                languages[row[0]] = row[1]  # Map ID to name
        except Exception as e:
            print(f"Error retrieving languages: {e}")
            # Handle error or log as needed
        print(languages)
        return languages
