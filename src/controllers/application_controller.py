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
from tkinter import messagebox


from src.controllers.snippet_controller import SnippetController
from src.controllers.theme_management_controller import ThemeController
from src.controllers.configuration_management_controller import ConfigurationController

from src.models.snippet_model import SnippetModel
from src.models.theme_management_model import ThemeModel
from src.models.configuration_management_model import ConfigurationModel
from src.utils.constants import THEMES_DIR, CONFIG_DIR


from src.views.snippet_view import SnippetView
from src.views.theme_management_view import ThemeView
from src.views.configuration_management_view import ConfigurationView

from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class ApplicationController:
    """Controller class for the application.

    This class is responsible for controlling the application logic and handling user interactions.

    Attributes:
        model: Reference to the model object.
        view: Reference to the view object.

    Methods:
        __init__: Initializes the ApplicationController object.
        initialize: Initializes the controller and binds events.
        run_application: Runs the application.
        show_snippet_details: Displays details of a selected snippet.
        handle_new_snippet: Handles the event for creating a new snippet.
    """

    def __init__(self, model, db_connection):
        """ set """
        self.model = model
        self.view = None
        self.db_connection = db_connection
        self.callbacks = {
            # Button Related Callbacks
            'new_snippet': self.new_snippet,
            'edit_snippet': self.edit_snippet,
            'delete_snippet': self.delete_snippet,
            'import_snippet': self.import_snippet,
            'export_snippet': self.export_snippet,
            "manage_languages": self.manage_languages,
            "manage_categories": self.manage_categories,
            "manage_theme": self.manage_theme,
            "manage_configuration": self.manage_configuration,
            "open_user_guide": self.open_user_guide,
            "open_faqs": self.open_faqs,
            "report_issue": self.report_issue,
            "suggest_feature": self.suggest_feature,
            "open_about": self.open_about,
            # Misc Callbacks
            'close_db_connection': self.close_db_connection,
            'add_snippet_to_treeview': self.add_snippet_to_treeview,
            'update_snippet_in_treeview': self.edit_snippet_in_treeview,
            'delete_snippet_in_treeview': self.delete_snippet_in_treeview,
            'on_tree_select': self.on_tree_select,
            'get_language_specific_categories': self.get_language_specific_categories,
            'get_general_categories': self.get_general_categories,
            'apply_theme': self.apply_theme
        }
        self.initialize_application()

    def initialize_application(self):
        """Initializes the application UI with data."""
        self.update_snippet_display()

    def set_view(self, view):
        """ set """
        self.view = view

    def get_callbacks(self):
        """ set """
        return self.callbacks

    def run_application(self):
        """ summary """
        # Display initial state of the application
        if self.view:
            self.view.run()

    def prepare_treeview_data(self):
        """
        summary
        """
        # Fetch all languages as a dictionary: {language_id: language_name, ...}
        languages = self.model.get_all_languages()

        # Fetch general categories as a list of dictionaries: [{'id': x, 'name': y}, ...]
        general_categories = self.model.get_general_categories()

        structured_data = {}

        for language_id, language_name in languages.items():
            # Initialize each language in structured data with an empty categories dictionary
            structured_data[language_id] = {
                'name': language_name,
                'categories': {}
            }

            # Populate general categories for each language
            for category in general_categories:
                structured_data[language_id]['categories'][f"general-{category['id']}"] = {
                    'name': category['name'],
                    'snippets': []
                }

            # Fetch and populate language-specific categories
            self.language_specific_categories = self.model.get_language_specific_categories(language_id)
            for category in self.language_specific_categories:
                structured_data[language_id]['categories'][f"specific-{category['id']}"] = {
                    'name': category['name'],
                    'snippets': []
                }

        # Fetch all snippets and categorize them under their respective language and category
        snippets = self.model.get_all_snippets()
        for snippet in snippets:
            lang_id = snippet['language_id']
            cat_id = snippet['category_id']
            category_prefix = 'specific-' if cat_id in [cat['id'] for cat in
                                                        self.language_specific_categories] else 'general-'
            cat_key = f"{category_prefix}{cat_id}"

            # Ensure the snippet's language and category are present in structured_data before adding
            if lang_id in structured_data and cat_key in structured_data[lang_id]['categories']:
                structured_data[lang_id]['categories'][cat_key]['snippets'].append(snippet)

        # structured_data is now ready and can be passed to the view for treeview construction
        if self.view:
            self.view.refresh_treeview(structured_data)

    def show_snippet_details(self):
        """ summary """
        # Retrieve the selected snippet from the treeview
        selected_item = self.view.treeview.selection()[0]
        snippet = self.model.get_snippet(selected_item)  # Implement this method in your ApplicationModel class

        # Display the details of the selected snippet in the text area
        self.view.display_snippet_details(snippet)  # Implement this method in your ApplicationView class

    def edit_snippet(self):
        """Handle the event to edit a snippet."""
        selected_items = self.view.treeview.selection()

        # Check if any item is selected
        if not selected_items:
            messagebox.showerror("Selection Required", "Please select a snippet to edit.")
            return

        # Assuming the first selected item is what we want to edit
        self.selected_item = selected_items[0]

        # Check if the selected item is a snippet
        if not self.selected_item.startswith("snippet-"):
            messagebox.showerror("Invalid Selection", "Please select a valid snippet to edit.")
            return

        # Strip the "snippet-" prefix to get the numeric ID
        snippet_id = self.selected_item.replace("snippet-", "")
        # Alternatively, if the prefix length is constant, you can use slicing:
        # snippet_id = self.selected_item[len("snippet-"):]

        # Proceed with snippet editing logic using the numeric ID
        self.snippetModel = SnippetModel(self.db_connection)
        self.snippetController = SnippetController(self.snippetModel, self.callbacks, snippet_id)
        self.snippetView = SnippetView(self.view.root, self.snippetController.get_callbacks())
        self.snippetController.set_view(self.snippetView)
        self.snippetView.show()

    def generate_code(self):
        """ summary """
        pass

    def export_snippet(self):
        """ summary """
        pass

    def import_snippet(self):
        """ summary """
        pass

    def delete_snippet(self):
        """ summary """
        pass

    def apply_theme(self, theme_name):
        """ summary """
        pass

    def manage_configuration(self):
        """
        Summary
        """
        self.configurationModel = ConfigurationModel(CONFIG_DIR)
        self.configurationController = ConfigurationController(self.configurationModel, self.callbacks)
        self.configurationView = ConfigurationView(self.view.root, self.configurationController.get_callbacks())

        self.configurationController.set_view(self.configurationView)
        # self.configurationController.load_configurations()
        self.configurationView.show()

    def close_db_connection(self):
        """
        summary
        """
        if self.db_connection:
            self.db_connection.close_connection()
            print("Database connection closed.")
            logger.info("Database connection successfully closed.")

    def on_tree_select(self, selected_item):
        """
        Summary
        """
        parent_item = self.view.treeview.parent(selected_item)
        grandparent_item = self.view.treeview.parent(parent_item) if parent_item else None

        if not parent_item:
            print("Language selected:", self.view.treeview.item(selected_item, 'text'))
        elif not grandparent_item:
            print("Category selected:", self.view.treeview.item(selected_item, 'text'))
        else:
            snippet_id = self.view.treeview.item(selected_item, 'values')[0]
            snippet_details = self.model.get_snippet(snippet_id)
            self.view.display_snippet_code(snippet_details['code'])

    def update_snippet_display(self):
        """ Test """
        if self.view is not None:
            snippets = self.model.get_all_snippets()
            self.view.refresh_treeview(snippets)

    def get_language_specific_categories(self, language_id):
        """ summary """
        language_specific_categories = self.model.get_language_specific_categories(language_id)
        if self.view is not None:
            self.view.update_language_specific_categories({language_id: language_specific_categories})

    def get_general_categories(self):
        """ summary """
        general_categories = self.model.get_general_categories()
        print(general_categories)
        if self.view is not None:
            self.view.update_general_categories(general_categories)

    def add_snippet_to_treeview(self):
        """
        Summary
        """

    def edit_snippet_in_treeview(self):
        """
        Summary
        """

    def delete_snippet_in_treeview(self):
        """
        Summary
        """

    def manage_languages(self):
        # Logic to manage programming languages in the application
        pass

    def manage_categories(self):
        # Logic to manage snippet categories
        pass

    def new_snippet(self):
        """ summary """
        # Inside your method where you're handling snippet actions (e.g., opening the snippet form):
        self.snippetModel = SnippetModel(self.db_connection)
        self.snippetController = SnippetController(self.snippetModel,
                                                   self.callbacks)  # No snippet passed, defaults to 'add' mode
        self.snippetView = SnippetView(self.view.root, self.snippetController.get_callbacks())
        self.snippetController.set_view(self.snippetView)

        self.snippetView.show()

    def manage_theme(self):
        """ summary """
        self.themeModel = ThemeModel(THEMES_DIR)
        self.themeController = ThemeController(self.themeModel, self.callbacks)
        self.themeView = ThemeView(self.view.root, self.themeController.get_callbacks())
        self.themeController.set_view(self.themeView)
        self.themeController.load_themes()

        self.themeView.show()

    def open_user_guide(self):
        # Logic to display the user guide
        pass

    def open_faqs(self):
        # Logic to display FAQs
        pass

    def report_issue(self):
        # Logic to handle reporting an issue
        pass

    def suggest_feature(self):
        # Logic to handle suggesting a new feature
        pass

    def open_about(self):
        # Logic to display information about the application
        pass
