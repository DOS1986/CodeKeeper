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
import os
import threading
import tkinter as tk
from src.utils.initialize_database import DatabaseInitializer
from src.utils.update_checker import UpdateChecker
from src.db.connection import DatabaseConnection
from src.utils.custom_logger import CustomLogger
from src.application_shell import ApplicationShell
from src.utils.path_utils import get_file_path, check_write_permission, get_download_path
from src.utils.configuration_manager import ConfigurationManager
from src.utils.theme import theme_manager  # Adjust this import according to your project structure


# Instantiate the logger
logger = CustomLogger(__name__).logger


class LoadingScreen:
    """
    Manages the loading and initial setup screen for the application.

    This class controls the display of a loading screen, checks if the application is being run
    for the first time, and initializes the database if necessary.
    """

    def __init__(self):
        """Prepare the loading screen but don't display it immediately."""
        super().__init__()
        self.db_connection = None
        self.root = tk.Tk()
        self.root.title("Loading...")
        self.root.geometry("300x100")
        self.root.overrideredirect(True)
        self.user_application = ConfigurationManager("application_config")
        self.label = tk.Label(self.root, text="Initializing, please wait...")
        self.label.pack()
        self.center_window(self.root)

        # Initialize UpdateChecker with dynamic paths and version
        self.update_checker = UpdateChecker(
            current_version=self.user_application.get_configuration("application.version", "0.1"),
            update_url=self.user_application.get_configuration("updates.update_url", "https://api.github.com/DOS1986/codekeeper/releases/latest"),
            download_path=get_download_path(subdir="UpdateFiles", default_subdir="CodeKeeper")
        )

        # Start the initialization process in a separate thread
        threading.Thread(target=self.initialize_application, daemon=True).start()

    def center_window(self, window):
        """
        Summary
        """
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def update_message(self, message):
        """Updates the loading screen message."""
        self.label.config(text=message)

    def initialize_application(self):
        """Handles the initialization sequence for the application."""
        self.update_message("Initializing application...")
        self.root.after(1000, self.load_preferences)

    def load_preferences(self):
        """
        Loads and applies user preferences upon application startup.

        This method is responsible for applying the user-selected theme
        by utilizing the theme_manager. It ensures the visual theme of the
        application aligns with the user's preferences. After applying the theme,
        it updates the loading screen message to inform the user that preferences
        have been loaded and that the application is now checking for updates.
        """
        theme_manager.apply_theme()  # Apply the theme as per user preferences
        logger.info("Preferences loaded. Checking for updates...")
        self.update_message("Preferences loaded. Checking for updates...")
        self.root.after(1000, self.check_for_updates)

    def check_for_updates(self):
        """
        Check for new releases on GitHub or another update server.
        This method replaces the placeholder implementation.
        """
        try:
            available, latest_version = self.update_checker.check_for_updates()
            if available:
                logger.info(f"Update available: {latest_version}")
                self.update_message(f"Update available: {latest_version}")
                # Optional: Prompt user to download and apply the update
            else:
                logger.info("You're up-to-date.")
                self.update_message("You're up-to-date.")
        except Exception as e:
            logger.error(f"Failed to check for updates: {e}")
            self.update_message("Update check failed.")

        self.root.after(1000, self.check_initialization)

    def check_initialization(self):
        """
        Checks and performs initial application setup.

        This includes verifying if the application database exists and creating necessary
        database tables if it's determined to be the first run. It handles initialization
        failures by logging errors and updating the loading screen message.
        """
        db_path = get_file_path("codekeeper.db", "Database", "CodeKeeper")
        if not check_write_permission(os.path.dirname(db_path)):
            logger.error("No write permission for the database directory.")
            self.update_message("No write permission for the database directory. Check logs.")
            return

        first_run = not os.path.isfile(db_path)

        # Open database connection explicitly
        self.db_connection = DatabaseConnection(db_path)

        # Check if we've successfully established a connection
        if not self.db_connection or not self.db_connection.connection:
            logger.error("Failed to establish a database connection.")
            self.update_message("Database connection failed. Check logs.")
            return

        try:
            if first_run:
                logger.info("Setting up database...")
                self.update_message("Setting up database...")
                initializer = DatabaseInitializer(self.db_connection)
                success, errors = initializer.create_tables()
                if success:
                    # Load initial data only if table creation was successful
                    success_data, errors_data = initializer.load_initial_data()
                    if success_data:
                        logger.info("Database setup complete. Application is ready.")
                        self.update_message("Database setup complete. Application is ready.")
                    else:
                        logger.error(f"Failed to load initial data: {', '.join(errors_data)}")
                        self.update_message("Failed to load initial data. Check logs.")
                        return  # Abort further initialization if loading data failed
                else:
                    logger.error(f"Failed to create tables: {', '.join(errors)}")
                    self.update_message("Failed to create tables. Check logs.")
                    return  # Abort further initialization if table creation failed
        except Exception as e:
            logger.error(f"An unexpected error occurred during initialization: {e}")
            self.update_message("Unexpected error during initialization. Check logs.")
            self.db_connection.close_connection()

        # Delay the start of the main application to ensure all messages are shown
        self.root.after(1000, lambda: self.start_main_application())

    def start_main_application(self):
        """
        Launches the main application interface.

        Args:
            self.db_connection (DatabaseConnection): An active database connection for the application to use.
        """
        self.root.destroy()  # Close the loading screen
        app_shell = ApplicationShell(self.db_connection)
        app_shell.run()

    def start(self):
        """
        Starts the loading and initialization process of the application.
        """
        # This method should initiate the loading screen and any initialization logic.
        # Since you're starting the initialization process in a separate thread within the __init__ method,
        # and Tkinter's main loop is started with `tk.mainloop()`,
        # you just need to ensure the Tkinter main loop starts here if not already started in `__init__`.
        self.root.mainloop()
