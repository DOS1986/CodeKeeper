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
import sys

from src.models.application_model import ApplicationModel
from src.views.application_view import ApplicationView, show_error_message
from src.controllers.application_controller import ApplicationController
from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class ApplicationShell:
    """
    The main entry point of the application which ties together models, views, and controllers.

    This class acts as the orchestrator for the application, setting up the MVC components,
    initializing them with the necessary dependencies, and starting the application's main loop.

    Attributes:
        controller (ApplicationController): The application's controller component.
        view (ApplicationView): The application's view component.
        model (ApplicationModel): The application's model component.
        db_connection: A database connection resource passed to the model for database operations.
    """
    def __init__(self, db_connection):
        """
        Initializes the ApplicationShell with a database connection.

        Args:
            db_connection: The database connection resource to be used by the application model.
        """
        self.controller = None
        self.view = None
        self.model = None
        self.db_connection = db_connection
        self.initialize()

    def initialize(self):
        """
        Initializes the MVC components of the application.

        Sets up the application model with the database connection, initializes the view,
        and creates the controller with references to both model and view. This setup ensures
        all components can properly interact following the MVC architectural pattern.
        """
        try:
            self.model = ApplicationModel(self.db_connection)
            self.controller = ApplicationController(self.model, self.db_connection)
            self.view = ApplicationView(self.controller.get_callbacks())
            self.controller.set_view(self.view)
            self.controller.prepare_treeview_data()

        except Exception as error:
            # Consider logging the error and presenting an error message to the user
            logger.error(f"Failed to initialize application components: {error}")
            # Display an error dialog or message box if the view is already initialized
            if self.view:
                show_error_message("Failed to initialize application components.")
            sys.exit(1)  # or handle more gracefully depending on application requirements

    def run(self):
        """
        Starts the main loop of the application.

        Calls the controller's method to begin application processing and interaction,
        effectively starting the application.
        """
        try:
            self.controller.run_application()
            self.view.root.mainloop()  # Assuming `root` is your Tk instance in `ApplicationView`
        except Exception as error:
            logger.error(f"An error occurred during application runtime: {error}")
