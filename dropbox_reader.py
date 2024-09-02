"""
This script interacts with the Dropbox API to authenticate a user, 
list files and folders in a specified Dropbox folder, 
and download files from Dropbox.

Modules:
    - os: Provides a way of using operating system dependent functionality.
    - logging: Provides logging capabilities.
    - io: Provides the BytesIO class for handling binary data.
    - dropbox: Provides the Dropbox API client.
    - coloredlogs: Provides colored logging output.
    - dotenv: Loads environment variables from a .env file.

Environment Variables:
    - DROPBOX_ACCESS_TOKEN: The access token for authenticating with Dropbox.
    - DROPBOX_FOLDER_PATH: The path to the Dropbox folder to list files and folders from.

Global Variables:
    - DROPBOX_AUTHENTICATED: A flag indicating whether Dropbox authentication was successful.

Functions:
    - list_dropbox_files_and_folders(folder_path=DROPBOX_FOLDER_PATH):
        Lists all files and folders in the specified Dropbox folder recursively.
        Args:
            folder_path (str): The path to the Dropbox folder to list files and folders from.
        Returns:
            tuple: A dictionary mapping file names to their full paths and a list of folder paths.
        Raises:
            dropbox.exceptions.ApiError: If there is an error listing files and folders.

    - download_dropbox_file(file_path):
        Downloads a file from Dropbox.
        Args:
            file_path (str): The path to the file in Dropbox to download.
        Returns:
            BytesIO: A BytesIO object containing the file's content.
        Raises:
            dropbox.exceptions.ApiError: If there is an error downloading the file.

Usage:
    Ensure that the environment variables are set in a .env file.
    Call the list_dropbox_files_and_folders function to list all files and 
    folders in the specified Dropbox folder.
    Call the download_dropbox_file function to download a file from Dropbox.
"""
import os
import logging
from io import BytesIO
import dropbox
import coloredlogs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

# Dropbox access token
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
DROPBOX_FOLDER_PATH = os.getenv("DROPBOX_FOLDER_PATH")

# Flag to indicate if Dropbox is authenticated
DROPBOX_AUTHENTICATED = True

try:
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    logger.info('Authenticated with Dropbox owned by %s',
                dbx.users_get_current_account().name.display_name)
except dropbox.exceptions.AuthError as err:
    logger.error("Authentication error: %s", err)
    if err.error.is_expired_access_token():
        logger.error("The access token has expired. Please refresh the access token.")
    DROPBOX_AUTHENTICATED = False

def list_dropbox_files_and_folders(folder_path=DROPBOX_FOLDER_PATH):
    """List all files and folders in the specified Dropbox folder recursively."""
    try:
        # Ensure the folder path starts with a slash, except for the root folder
        if folder_path and not folder_path.startswith('/'):
            folder_path = '/' + folder_path

        result = dbx.files_list_folder(folder_path)
        entries = result.entries

        while result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
            entries.extend(result.entries)

        files = [entry.path_lower for entry in entries 
                 if isinstance(entry, dropbox.files.FileMetadata)]
        folders = [entry.path_lower for entry in entries 
                   if isinstance(entry, dropbox.files.FolderMetadata)]

        logger.debug("Files found in %s: %s", folder_path, files)
        logger.debug("Folders found in %s: %s", folder_path, folders)

        # Recursively list files and folders in subfolders
        for folder in folders:
            sub_files, sub_folders = list_dropbox_files_and_folders(folder)
            files.extend(sub_files)
            folders.extend(sub_folders)

        # Create a dictionary mapping file names to their full paths
        file_map = {os.path.basename(file): file for file in files}

        return file_map, folders
    except dropbox.exceptions.ApiError as api_err:
        logger.error("Failed to list files and folders: %s", api_err)
        raise

def download_dropbox_file(file_path):
    """Download a file from Dropbox."""
    try:
        _, res = dbx.files_download(file_path)
        return BytesIO(res.content)
    except dropbox.exceptions.ApiError as api_err:
        logger.error("Failed to download file: %s", api_err)
        raise
