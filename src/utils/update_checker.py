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
import requests
import zipfile
from subprocess import Popen
from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class UpdateChecker:
    """
    A class responsible for checking for application updates, downloading them, and applying them.

    This class communicates with a specified update URL to determine if a newer version of the
    application is available. If an update is found, it can download the update package and
    apply it, typically by extracting files or running an installer script.

    Attributes:
        current_version (str): The current version of the application.
        update_url (str): The URL to check for available updates, which should return version metadata.
        download_path (str): The directory path where update packages will be downloaded.

    Methods:
        check_for_updates: Checks the remote server for available updates.
        download_update: Downloads the update package from a given URL.
        apply_update: Applies the downloaded update, such as by extracting files or running an update script.
    """
    def __init__(self, current_version, update_url, download_path):
        """
        Initializes the UpdateChecker with necessary information to check for and process updates.

        Args:
            current_version (str): The current version string of the application, used to compare
                                   with the version string retrieved from the update server to determine
                                   if an update is necessary.
            update_url (str): The URL to query for the latest version information. This URL should
                              return a response that includes at least the latest version string and,
                              if an update is available, a URL to download the update package.
            download_path (str): The filesystem path to a directory where update packages will be
                                 downloaded. This path should have write permissions for the application.
        """
        self.current_version = current_version
        self.update_url = update_url
        self.download_path = download_path

    def check_for_updates(self):
        """
        Checks for available updates by querying a remote server.

        Returns:
            A tuple (bool, str), where the first element indicates if an update is available,
            and the second element is the new version string or a message.
        """
        try:
            response = requests.get(self.update_url)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.

            latest_version = response.json().get('tag_name')
            if latest_version and latest_version != self.current_version:
                return True, latest_version, response.json().get('download_url')
            else:
                return False, "You're up-to-date.", None
        except requests.RequestException as e:
            logger.error(f"Failed to check for updates: {e}")
            return False, "Update check failed.", None

    def download_update(self, download_url):
        """
        Downloads the update file from the provided URL.

        Args:
            download_url (str): The URL from which to download the update.

        Returns:
            str: Path to the downloaded file, or None if the download failed.
        """
        try:
            local_filename = os.path.join(self.download_path, download_url.split('/')[-1])
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            return local_filename
        except requests.RequestException as e:
            logger.error(f"Failed to download update: {e}")
            return None

    def apply_update(self, update_file_path):
        """
        Applies the downloaded update. This example assumes a ZIP file and simply extracts it.

        Args:
            update_file_path (str): The path to the downloaded update file.
        """
        try:
            # Example: Unzipping an update package
            with zipfile.ZipFile(update_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.download_path)

            # Example: Running an installer or update script
            # Popen(['path/to/installer', 'installer-arguments'])

            logger.info("Update applied successfully.")

            # You might want to restart your application here.
        except Exception as e:
            logger.error(f"Failed to apply update: {e}")
