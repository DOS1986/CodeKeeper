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

from src.utils.constants import CONFIG_DIR
from src.utils.path_utils import get_file_path
from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class ConfigurationManager:
    """
    Manages user preferences for the application, including loading, saving,
    and accessing individual preferences.
    """

    def __init__(self, config_name):
        """
        Initializes the ConfigurationManager object by loading the stored configurations
        from either a user-specific or default configuration file.

        Args:
            config_name (str): Base name of the configuration file (without "user_" or "default_" prefix).
        """
        self.config_file = get_file_path(f"user_{config_name}.json", "config", "CodeKeeper")
        self.default_config_file = os.path.join(CONFIG_DIR, f"default_{config_name}.json")
        self.configurations = self.load_configurations()

    def load_configurations(self):
        """
        Attempts to load the user-specific configuration if available,
        otherwise falls back to the default configuration.

        Returns:
            dict: The loaded configurations.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading user configuration: {e}")
        # Attempt to load default configurations if user-specific configurations fail to load
        try:
            with open(self.default_config_file, "r") as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error loading default configuration: {e}")
        return {}  # Return an empty dict if neither file could be loaded

    def get_configuration(self, key, default=None):
        """
        Retrieves a configuration value by key.

        Args:
            key (str): The configuration key.
            default: The default value to return if the key is not found.

        Returns:
            The value of the configuration or the default value if the key is not found.
        """
        return self.configurations.get(key, default)

    def set_configuration(self, key, value):
        """
        Sets a configuration key to a given value.

        Args:
            key (str): The configuration key.
            value: The value to set for the key.
        """
        self.configurations[key] = value
        self.save_configurations()

    def save_configurations(self):
        """
        Saves the current configurations to the user-specific configuration file.
        """
        try:
            with open(self.config_file, "w") as file:
                json.dump(self.configurations, file, indent=4)
        except Exception as e:
            logger.error(f"Error saving configurations: {e}")
