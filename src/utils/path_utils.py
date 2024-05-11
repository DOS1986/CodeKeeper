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
import sys


def get_file_path(file_name, folder_name, default_subdir=".appname"):
    """
    Get the appropriate file path based on the operating system and user preferences.

    Args:
        file_name (str): The name of the file.
        folder_name (str): The name of the folder to store the file in.
        default_subdir (str): The default subdirectory under the user's home directory.

    Returns:
        str: The full path to the file.
    """
    base_path = ""
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # Unix-like system (Linux, macOS)
        base_path = os.path.expanduser(f'~/{default_subdir}')
    elif sys.platform.startswith('win'):
        # Windows
        base_path = os.path.join(os.getenv('APPDATA', os.path.expanduser("~")), default_subdir)
    else:
        # Fallback to application directory
        base_path = os.path.join(os.getcwd(), default_subdir)

    full_path = os.path.join(base_path, folder_name, file_name)

    # Ensure that the directory for the file exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return full_path


def get_download_path(subdir="Downloads", default_subdir=".appname"):
    """
    Get the appropriate download path based on the operating system and user preferences.

    Args:
        subdir (str): The subdirectory under the main application directory where downloads should be saved.
        default_subdir (str): The default subdirectory under the user's home directory for the application.

    Returns:
        str: The full path to the downloads' directory.
    """
    base_path = ""
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # Unix-like system (Linux, macOS)
        base_path = os.path.expanduser(f'~/{default_subdir}')
    elif sys.platform.startswith('win'):
        # Windows
        base_path = os.path.join(os.getenv('APPDATA', os.path.expanduser("~")), default_subdir)
    else:
        # Fallback to application directory
        base_path = os.path.join(os.getcwd(), default_subdir)

    download_path = os.path.join(base_path, subdir)

    # Ensure that the directory for downloads exists
    os.makedirs(download_path, exist_ok=True)

    return download_path


def check_write_permission(path):
    """
    Check if the application has write permission to the specified path.

    Args:
        path (str): The path to check for write permissions.

    Returns:
        bool: True if write permission is granted, False otherwise.
    """
    try:
        test_file_path = os.path.join(path, 'temp_test_file')
        with open(test_file_path, 'w') as test_file:
            test_file.write('test')
        os.remove(test_file_path)
        return True
    except IOError as e:
        print(f"Write permission check failed: {e}")
        return False
