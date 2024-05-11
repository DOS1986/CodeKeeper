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
import logging
from logging.config import dictConfig
import json
import os
from src.utils.path_utils import get_file_path  # Assuming this is your utility function for paths


class CustomLogger:
    """
    A custom logger class that implements singleton pattern to create a unique logger for each logger name.
    
    This logger supports writing logs to both console and file, with separate handling for error logs.
    It uses rotating file handlers to limit log file sizes and maintain a fixed number of backup logs.
    """

    _loggers = {}

    def __new__(cls, name, level=logging.INFO):
        """
        Ensures that only one instance of logger is created for each unique logger name.

        Args:
            name (str): The name of the logger to create or retrieve.
            level (int): The logging level; defaults to logging.INFO.

        Returns:
            CustomLogger: A singleton instance of the custom logger.
        """
        if name not in cls._loggers:
            cls._loggers[name] = super(CustomLogger, cls).__new__(cls)
            cls._loggers[name]._init_logger(name, level)
        return cls._loggers[name]

    def _init_logger(self, name, level):
        self._load_logging_config(name)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def _load_logging_config(self, name):
        """Loads logging configuration from a JSON file, adjusting file paths dynamically."""
        # First, try loading the configuration from a user-specific location
        user_config_path = get_file_path("user_logging_config.json", "config", default_subdir="CodeKeeper")
        # Fallback to the default configuration within the source directory
        default_config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'default_logging_config.json')

        # Determine which configuration file exists
        if os.path.exists(user_config_path):
            config_path = user_config_path
        else:
            config_path = default_config_path

        # Load the configuration
        with open(config_path, 'r') as config_file:
            logging_config = json.load(config_file)

        # Adjust file paths in the logging configuration
        logs_base_path = get_file_path("", "logs", "CodeKeeper")
        for handler in logging_config['handlers'].values():
            if 'filename' in handler:
                # Set up a dedicated error log file
                if handler.get('level') == 'ERROR':
                    handler['filename'] = os.path.join(logs_base_path, 'error.log')
                # Set up specific log files for each logger based on the logger's name
                else:
                    handler['filename'] = os.path.join(logs_base_path, f"{name}.log")

        # Apply the logging configuration
        logging.config.dictConfig(logging_config)
