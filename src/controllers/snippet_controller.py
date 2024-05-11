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
import threading


def validate_snippet_data(data):
    """
    Validates the snippet data.

    Args:
        data: A dictionary containing the snippet data to validate.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    # Implement validation logic, e.g., checking for empty fields
    required_fields = ['title', 'language', 'code']
    return all(data.get(field) for field in required_fields)


class SnippetController:
    """
    summary
    """

    def __init__(self, model, application_callbacks, selected_item=None):
        """
        Initializes the SnippetController.

        Args:
            model: The model that handles the snippet data.

        """
        self.model = model
        self.view = None
        self.selected_item = selected_item
        self.snippet = self.model.get_snippet(self.selected_item)
        print(self.snippet)
        self.mode = 'edit' if selected_item else 'add'
        self.callbacks = {
            'submit_snippet': self.submit_snippet,
        }
        self.application_callbacks = application_callbacks

    def get_callbacks(self):
        """ set """
        return self.callbacks

    def set_view(self, view):
        """
        summary
        """
        self.view = view
        # self.view.set_submit_callback(self.submit_snippet)
        if self.mode == 'edit':
            self.view.populate_form(self.snippet)

    def submit_snippet_async(self, snippet_data):
        """Submits the snippet in a new thread to keep UI responsive."""
        threading.Thread(target=self.submit_snippet, args=(snippet_data,), daemon=True).start()

    def submit_snippet(self, snippet_data):
        """
        Attempts to add a new snippet or update an existing one based on the controller's mode.
        This method runs in a separate thread to keep the UI responsive.
        """
        if not self.validate_snippet_data(snippet_data):
            self.invoke_in_main_thread(self.view.show_message, "Validation failed. Please check your input.", False)
            return

        if self.mode == 'add':
            self.success = self.model.add_snippet(snippet_data)
        elif self.mode == 'edit':
            self.success = self.model.update_snippet(self.selected_item, snippet_data)

        message = "Snippet saved successfully." if self.success else "Failed to save snippet."
        self.invoke_in_main_thread(self.post_submission_cleanup, message, self.success)

        # Execute UI operations in the main thread
        self.view.master.after(0, self.view.show_message, message, self.success)

    @staticmethod
    def validate_snippet_data(data):
        """
        Validates the provided snippet data.
        """
        required_fields = ['title', 'language', 'code']
        return all(data.get(field) for field in required_fields)

    def invoke_in_main_thread(self, func, *args, **kwargs):
        """
        Utility method to run a function in the main thread, especially useful for updating the UI from a background thread.
        """
        self.view.master.after(0, func, *args, **kwargs)

    def post_submission_cleanup(self, message, success, snippet_data=None):
        """
        Handles the cleanup after submitting a snippet, including form clearing, message showing,
        and updating the main display based on the operation's success.

        Args:
            message (str): The message to show to the user indicating the operation's outcome.
            success (bool): Indicates whether the snippet submission was successful.
            snippet_data (dict, optional): The data of the snippet that was submitted. This is used to update the main display.
        """
        if success:
            # Clear the form fields if the submission was successful.
            self.view.clear_form()

            # Show a success message to the user.
            self.view.show_message("Success", message)

            # Assuming the application_callbacks dict has a callback to refresh or update the main display.
            # If a snippet was added or edited, update the treeview or relevant display accordingly.
            if snippet_data:
                # Check if the operation was an add or edit based on snippet_data content.
                if 'id' in snippet_data and snippet_data['id']:
                    # Handle updating an existing snippet in the treeview.
                    self.application_callbacks['update_snippet_in_treeview'](snippet_data)
                else:
                    # Handle adding a new snippet to the treeview.
                    self.application_callbacks['add_snippet_to_treeview'](snippet_data)
            else:
                # General refresh of the display if no specific snippet data is provided.
                self.application_callbacks['refresh_display']()

            # Close the snippet form window.
            self.view.close()
        else:
            # Show an error message if the submission was not successful.
            self.view.show_message("Error", message)

    def create_snippet(self, data):
        """
        Creates a new snippet.

        Args:
            data: A dictionary containing the new snippet data.

        Returns:
            bool: True if the snippet was created successfully, False otherwise.
        """
        # Call the model's method to create a new snippet
        try:
            self.model.add_snippet(data)
            self.callbacks['add-snippet-treeview'](data)
            return True
        except Exception as e:
            print(f"Error creating snippet: {e}")  # Logging the error
            return False

    def update_snippet(self, data):
        """
        Updates an existing snippet.

        Args:
            data: A dictionary containing the updated snippet data.

        Returns:
            bool: True if the snippet was updated successfully, False otherwise.
        """
        # Call the model's method to update the snippet
        try:
            self.model.update_snippet(self.selected_item, data)
            return True
        except Exception as e:
            print(f"Error updating snippet: {e}")  # Logging the error
            return False
