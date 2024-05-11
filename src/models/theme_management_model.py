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
import json
import os
import shutil

from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class ThemeModel:
    def __init__(self, themes_directory):
        self.themes_directory = themes_directory

    def get_themes(self):
        """Returns a list of available theme names, excluding 'template_theme.json'."""
        themes = []
        for filename in os.listdir(self.themes_directory):
            if filename.endswith('.json') and filename != 'template_theme.json':
                themes.append(os.path.splitext(filename)[0])
        return themes

    def get_theme_data(self, theme_name):
        """Returns the data of a specified theme."""
        with open(os.path.join(self.themes_directory, f"{theme_name}.json"), 'r') as file:
            return json.load(file)

    def save_theme_data(self, theme_name, theme_data):
        """Saves the modified theme data back to the JSON file."""
        with open(os.path.join(self.themes_directory, f"{theme_name}.json"), 'w') as file:
            json.dump(theme_data, file, indent=4)

    def validate_theme_data(self, theme_data):
        """Validates the modified theme data against required structure and value types."""
        required_keys = ['theme_info', 'colors', 'fonts', 'ttkStyles']
        theme_info_keys = ['name', 'author', 'version', 'last_modified', 'description']
        color_and_font_keys = ['default', 'button', 'treeview', 'tabs', 'menu']

        # Validate presence of top-level keys
        for key in required_keys:
            if key not in theme_data:
                raise ValueError(f"Theme data missing required key: {key}")

        # Validate 'theme_info' structure
        for key in theme_info_keys:
            if key not in theme_data['theme_info']:
                raise ValueError(f"'theme_info' missing required key: {key}")

        # Validate 'colors' structure
        if not isinstance(theme_data['colors'], dict):
            raise ValueError("'colors' must be a dictionary.")
        for key, value in theme_data['colors'].items():
            if not isinstance(value, (str, dict)):  # Assuming color can be a hex string or a dict of colors
                raise ValueError(f"Color '{key}' has an invalid format. Expected a hex string or a dictionary.")

        # Validate 'fonts' structure
        if not isinstance(theme_data['fonts'], dict):
            raise ValueError("'fonts' must be a dictionary.")
        for key, value in theme_data['fonts'].items():
            if not isinstance(value, list) or not all(isinstance(item, (str, int)) for item in value):
                raise ValueError(f"Font '{key}' has an invalid format. Expected a list of strings and/or integers.")

        # Validate 'ttkStyles' structure and presence of configure or map
        if not isinstance(theme_data['ttkStyles'], dict):
            raise ValueError("'ttkStyles' must be a dictionary.")
        for style, details in theme_data['ttkStyles'].items():
            if 'configure' not in details and 'map' not in details:
                raise ValueError(f"'{style}' in 'ttkStyles' must have either 'configure' or 'map' keys.")

        # Additional complex validations can be added here as necessary

        # Log successful validation
        logger.info("Theme data validation passed.")

    def backup_theme_data(self, theme_name):
        """Backups the modified theme data"""
        backup_file_path = os.path.join(self.themes_directory, f"{theme_name}_backup.json")
        original_file_path = os.path.join(self.themes_directory, f"{theme_name}.json")
        if os.path.exists(original_file_path):
            shutil.copyfile(original_file_path, backup_file_path)
            logger.info(f"Backup created for theme: {theme_name}")

    def restore_theme_data_from_backup(self, theme_name):
        """Restores the modified theme data"""
        backup_file_path = os.path.join(self.themes_directory, f"{theme_name}_backup.json")
        if os.path.exists(backup_file_path):
            shutil.copyfile(backup_file_path, os.path.join(self.themes_directory, f"{theme_name}.json"))
            logger.info(f"Theme restored from backup: {theme_name}")