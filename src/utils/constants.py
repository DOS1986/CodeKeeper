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

# Application Metadata
APPLICATION_NAME = "CodeKeeper"
APPLICATION_VERSION = "0.1"
APPLICATION_AUTHOR = "David Southwood"

# Configuration Defaults
DEFAULT_SUBDIR = "CodeKeeper"
DEFAULT_DATABASE_NAME = "codekeeper.db"
CONFIG_DIR_NAME = "config"
LOGS_DIR_NAME = "logs"

# URLs and Endpoints
UPDATE_CHECK_URL = "https://api.github.com/repos/DOS1986/codekeeper/releases/latest"

# General UI Constants
UI_PADDING = 10
UI_FONT_SIZE_SMALL = 10
UI_FONT_SIZE_MEDIUM = 12
UI_FONT_SIZE_LARGE = 14
UI_FONT_FAMILY = "Helvetica"

# Colors (consider using a consistent and accessible color scheme)
COLOR_PRIMARY = "#005f73"
COLOR_SECONDARY = "#0a9396"
COLOR_ACCENT = "#94d2bd"
COLOR_BACKGROUND = "#e9d8a6"
COLOR_TEXT = "#292929"
COLOR_ERROR = "#e63946"
COLOR_SUCCESS = "#2a9d8f"

# Define specific font styles
UI_FONT_NORMAL = (UI_FONT_FAMILY, UI_FONT_SIZE_MEDIUM)
UI_FONT_BOLD = (UI_FONT_FAMILY, UI_FONT_SIZE_MEDIUM, "bold")
UI_FONT_ITALIC = (UI_FONT_FAMILY, UI_FONT_SIZE_MEDIUM, "italic")

# Sizes and dimensions
MAIN_WINDOW_SIZE = "800x600"
BUTTON_HEIGHT = 2
BUTTON_WIDTH = 15

# Miscellaneous
TOOLTIP_BACKGROUND = "#ffffe0"
TOOLTIP_FOREGROUND = "#000000"

# Path Constants
# Base directory of the application's source code
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Config directory
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
# Utility directory
UTILS_DIR = os.path.join(BASE_DIR, 'utils')
# Database directory
DB_DIR = os.path.join(BASE_DIR, 'db')
# Themes directory within the config folder
THEMES_DIR = os.path.join(CONFIG_DIR, 'themes')
# Assets directory
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
# Images directory
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')

# Error Messages and User Prompts
ERROR_PERMISSION_DENIED = "You do not have permission to perform this action."
PROMPT_SAVE_BEFORE_EXIT = "Do you want to save changes before exiting?"

# Keys and Tokens
# Be cautious with sensitive information; it's often better to use environment variables or secure storage methods

