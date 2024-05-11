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
from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class ThemeController:
    """ set """

    def __init__(self, model, application_callbacks):
        """ set """
        self.model = model
        self.view = None
        self.current_theme = None
        self.callbacks = {
            'theme_selected': self.theme_selected,
            'save_theme': self.save_theme,
        }
        self.application_callbacks = application_callbacks

    def apply_theme(self, theme_name):
        """ set """
        try:
            # Assuming a method in the application to apply themes
            self.application_callbacks['apply_theme'](theme_name)
            logger.info(f"Theme applied: {theme_name}")
        except Exception as e:
            logger.error(f"Failed to apply theme: {e}")
            self.view.show_message(f"Failed to apply theme: {e}", success=False)

    def set_view(self, view):
        """ set """
        self.view = view

    def get_callbacks(self):
        """ set """
        return self.callbacks

    def load_themes(self):
        """ set """
        try:
            themes = self.model.get_themes()
            self.view.list_themes(themes)
        except Exception as e:
            print(f"Failed to load themes: {e}")  # Logging the error
            # message = f"Failed to load themes: {e}"
            # self.view.show_message("Error", message)

    def run_application(self):
        """ summary """
        # Display initial state of the application
        if self.view:
            self.view.run()

    def theme_selected(self, theme_name):
        """ set """
        try:
            self.current_theme = theme_name
            theme_data = self.model.get_theme_data(theme_name)
            self.view.display_theme_data(theme_data)
        except Exception as e:
            self.view.show_message(f"Failed to load theme data: {e}")

    def save_theme(self, theme_data):
        """ set """
        if self.current_theme:
            try:
                self.model.save_theme_data(self.current_theme, theme_data)
                self.view.show_message("Theme saved successfully.")
            except Exception as e:
                self.view.show_message(f"Failed to save theme: {e}")
        else:
            self.view.show_message("No theme selected.")
