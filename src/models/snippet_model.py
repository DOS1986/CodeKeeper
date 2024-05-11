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


class SnippetModel:
    """
    The SnippetModel class handles all data operations related to code snippets,
    including CRUD (Create, Read, Update, Delete) operations.
    """

    def __init__(self, db_connection):
        """
        Initialize the SnippetModel with a database connection.

        Parameters:
            db_connection: An active database connection.
        """
        self.db_connection = db_connection.connection

    def add_snippet(self, snippet_data):
        """
        Adds a new snippet to the database using data from a dictionary.

        Parameters:
            snippet_data (dict): A dictionary containing the snippet data.

        Returns:
            The ID of the newly created snippet or None if the operation failed.
        """
        query = "INSERT INTO snippets (title, language, code, category_id) VALUES (?, ?, ?, ?)"
        params = (snippet_data['title'], snippet_data['language'], snippet_data['code'], snippet_data.get('category_id'))

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            self.db_connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding snippet: {e}")
            return None

    def update_snippet(self, snippet_id, snippet_data):
        """
        Updates an existing snippet in the database using data from a dictionary.

        Parameters:
            snippet_id (int): The ID of the snippet to update.
            snippet_data (dict): A dictionary containing the updated snippet data.

        Returns:
            True if the snippet was successfully updated, False otherwise.
        """
        query = "UPDATE snippets SET title = ?, language = ?, code = ?, category_id = ? WHERE id = ?"
        params = (snippet_data['title'], snippet_data['language'], snippet_data['code'], snippet_data.get('category_id'), snippet_id)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            self.db_connection.commit()
            return True if cursor.rowcount > 0 else False
        except Exception as e:
            print(f"Error updating snippet: {e}")
            return False

    def delete_snippet(self, snippet_id):
        """
        Deletes a snippet from the database.

        Parameters:
            snippet_id (int): The ID of the snippet to delete.

        Returns:
            True if the snippet was successfully deleted, False otherwise.
        """
        query = """DELETE FROM snippets WHERE id = ?"""
        params = (snippet_id,)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            self.db_connection.commit()
            return True if cursor.rowcount > 0 else False
        except Exception as e:
            print(f"Error deleting snippet: {e}")
            return False

    def get_snippet(self, snippet_id):
        """
        Retrieves a single snippet from the database by its ID, including language name and category name.

        Parameters:
            snippet_id (int): The ID of the snippet to retrieve.

        Returns:
            A dictionary containing the snippet data or None if not found.
        """
        params = (snippet_id,)
        query = """SELECT snippets.id, snippets.title, snippets.code, languages.name AS language, categories.name AS category FROM snippets JOIN languages ON snippets.language_id = languages.id JOIN categories ON snippets.category_id = categories.id WHERE snippets.id = ?"""

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            snippet = cursor.fetchone()
            if snippet is not None:
                return {
                    "id": snippet[0],
                    "title": snippet[1],
                    "code": snippet[2],
                    "language": snippet[3],
                    "category": snippet[4]
                }
            return None
        except Exception as e:
            print(f"Error retrieving snippet: {e}")
            return None

    def get_all_snippets(self):
        """
        Retrieves all snippets from the database, including language names and category names.

        Returns:
            A list of dictionaries, where each dictionary contains the data of one snippet.
        """
        query = """SELECT snippets.id, snippets.title, snippets.code, languages.name AS language, categories.name AS category FROM snippets JOIN languages ON snippets.language_id = languages.id JOIN categories ON snippets.category_id = categories.id ORDER BY s.title"""

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query)
            snippets = cursor.fetchall()
            return [
                {"id": row[0], "title": row[1], "code": row[2], "language": row[3], "category": row[4]}
                for row in snippets
            ]
        except Exception as e:
            print(f"Error retrieving all snippets: {e}")
            return []

    def get_snippets_by_category(self, category_id):
        """
        Retrieves all snippets that belong to a specific category.

        Parameters:
            category_id (int): The ID of the category.

        Returns:
            A list of dictionaries, where each dictionary contains the data of one snippet.
        """
        query = """SELECT id, title, language, code FROM snippets WHERE category_id = ? ORDER BY title"""
        params = (category_id,)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            snippets = cursor.fetchall()
            return [
                {"id": row[0], "title": row[1], "language": row[2], "code": row[3]}
                for row in snippets
            ]
        except Exception as e:
            print(f"Error retrieving snippets by category: {e}")
            return []
