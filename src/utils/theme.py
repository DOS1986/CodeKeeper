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
import json
import shutil
from src.utils.path_utils import get_file_path
from src.utils.configuration_manager import ConfigurationManager
from src.utils.custom_logger import CustomLogger
from src.utils.constants import THEMES_DIR

# Instantiate the logger
logger = CustomLogger(__name__).logger


def load_theme(theme_name):
    """
    Loads a theme by name. First attempts to load from the user-specific theme directory. If the theme is
    not found, it copies the default theme from the application's internal directory to the user-specific
    directory and then loads it.

    Args:
        theme_name (str): The name of the theme to load.

    Returns:
        dict: The theme properties or an empty dictionary if the theme cannot be loaded.
    """
    # First, attempt to get the user-specific theme path
    theme_path = get_file_path(f"{theme_name}.json", "themes", "CodeKeeper")

    # Check if the theme exists at the user-specific path; if not, try copying from the default directory
    if not os.path.exists(theme_path):
        default_theme_path = os.path.join(THEMES_DIR, f"{theme_name}.json")
        if os.path.exists(default_theme_path):
            try:
                os.makedirs(os.path.dirname(theme_path), exist_ok=True)
                shutil.copy(default_theme_path, theme_path)
                logger.info(f"Copied default theme '{theme_name}' to user directory.")
            except Exception as e:
                logger.error(f"Failed to copy default theme '{theme_name}': {e}")
                return {}  # Return an empty theme if copy fails

    # Try to load the theme from the now potentially copied user-specific path
    try:
        with open(theme_path, "r") as theme_file:
            # Directly return the loaded JSON object without accessing ["ui"]
            return json.load(theme_file)
    except Exception as e:
        logger.error(f"Error loading theme '{theme_name}': {e}")
        return {}  # Return an empty theme in case of error


class ThemeManager:
    """Manages application themes, including loading and applying themes."""

    def __init__(self):
        """Initializes the ThemeManager with the current theme."""
        self.current_theme = {}
        self.apply_theme()

    def apply_theme(self):
        """
        Applies the user's selected theme or the default theme if none is selected.
        """
        user_preferences = ConfigurationManager("preferences_config")

        user_theme = user_preferences.get_configuration("theme", "light_theme")
        self.current_theme = load_theme(user_theme)

    def get_current_theme(self):
        """
        Returns the currently applied theme.

        Returns:
            dict: The current theme properties.
        """
        return self.current_theme


# Creating a singleton instance of ThemeManager to be used across the application.
theme_manager = ThemeManager()
