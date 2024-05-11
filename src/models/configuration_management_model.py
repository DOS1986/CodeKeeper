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
import platform
import shutil
from pathlib import Path
from src.utils.custom_logger import CustomLogger
from src.utils.path_utils import get_file_path, check_write_permission

# Instantiate the logger
logger = CustomLogger(__name__).logger


class ConfigurationModel:
    def __init__(self, config_directory):
        self.default_config_path = config_directory

    def get_config_path(self, config_name, is_user_config=True):
        """
        Constructs the file path for the configuration file.
        If is_user_config is True, it looks for the file in the user's config directory,
        otherwise in the application's default config directory.
        """
        config_file_name = f"{config_name}_config.json"
        if is_user_config:
            return get_file_path(f"user_{config_file_name}", "config")
        else:
            return Path(self.default_config_path) / f"default_{config_file_name}"

    def read_config(self, config_name):
        """
        Attempts to read the user-specific configuration; falls back to the default configuration if not available.
        """
        # Try to load the user-specific configuration first
        user_config_path = self.get_config_path(config_name)
        if os.path.exists(user_config_path):
            with open(user_config_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            # Fall back to the default configuration
            default_config_path = self.get_config_path(config_name, is_user_config=False)
            if os.path.exists(default_config_path):
                with open(default_config_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
        return {}  # Return an empty dict if neither file exist

    def write_config(self, config_name, config_data):
        """
        Writes the configuration data to the user-specific configuration file.
        """
        user_config_path = self.get_config_path(config_name)
        if check_write_permission(os.path.dirname(user_config_path)):
            with open(user_config_path, 'w', encoding='utf-8') as file:
                json.dump(config_data, file, indent=4)
        else:
            # Handle the error, e.g., by notifying the user
            print("Error: Application does not have write permission for the configuration directory.")

    def backup_config(self, config_name):
        """
        Creates a backup of the user-specific configuration file.
        """
        user_config_path = self.get_config_path(config_name)
        backup_path = user_config_path.with_suffix(".bak")
        if user_config_path.exists():
            shutil.copy(user_config_path, backup_path)

    def restore_backup(self, config_name):
        """
        Restores the user-specific configuration from the backup file.
        """
        backup_path = self.get_config_path(config_name).with_suffix(".bak")
        # Check if the backup file exists
        if os.path.exists(backup_path):
            # Read the backup configuration
            with open(backup_path, 'r', encoding='utf-8') as file:
                backup_config = json.load(file)

            # Write the backup configuration to the main user-specific config file
            self.write_config(config_name, backup_config)

    def validate_config(self, config_data):
        # Example validation logic for demonstration
        errors = []

        # Check for required keys
        required_keys = ['theme', 'logging_level', 'auto_update']
        for key in required_keys:
            if key not in config_data:
                errors.append(f"Missing required configuration key: {key}")

        # Check for value constraints
        if 'logging_level' in config_data and config_data['logging_level'] not in ['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                                                                   'CRITICAL']:
            errors.append("Invalid logging level")

        # Return a tuple indicating if the config is valid, and any error messages
        is_valid = len(errors) == 0
        return is_valid, errors
