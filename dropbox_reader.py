"""
This script provides functionality to interact with Dropbox using the Dropbox API.

It includes the following features:
1. Authenticates with Dropbox using an access token loaded from environment variables.
2. Lists all files and folders in a specified Dropbox folder recursively.
3. Downloads a specified file from Dropbox.

Uses the `dropbox` library to interact with the Dropbox API and `coloredlogs` for enhanced logging.

Functions:
- `list_dropbox_files_and_folders(folder_path)`: 
    Lists all files and folders in the specified Dropbox folder recursively.
- `download_dropbox_file(file_path)`: 
    Downloads a file from Dropbox.

Environment Variables:
- `DROPBOX_ACCESS_TOKEN`: The access token for authenticating with Dropbox.

Example usage:
    files, folders = list_dropbox_files_and_folders('/path/to/folder')
    file_content = download_dropbox_file('/path/to/file')
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

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
logger.info('Authenticated with Dropbox owned by %s',
            dbx.users_get_current_account().name.display_name)

def list_dropbox_files_and_folders(folder_path='/rag++ hack night - build log submissions'):
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

        files = [entry.path_lower for entry in entries if isinstance(entry, dropbox.files.FileMetadata)]
        folders = [entry.path_lower for entry in entries if isinstance(entry, dropbox.files.FolderMetadata)]

        logger.debug("Files found in %s: %s", folder_path, files)
        logger.debug("Folders found in %s: %s", folder_path, folders)

        # Recursively list files and folders in subfolders
        for folder in folders:
            sub_files, sub_folders = list_dropbox_files_and_folders(folder)
            files.extend(sub_files)
            folders.extend(sub_folders)

        return files, folders
    except dropbox.exceptions.ApiError as err:
        logger.error("Failed to list files and folders: %s", err)
        raise

def download_dropbox_file(file_path):
    """Download a file from Dropbox."""
    try:
        metadata, res = dbx.files_download(file_path)
        return BytesIO(res.content)
    except dropbox.exceptions.ApiError as err:
        logger.error("Failed to download file: %s", err)
        raise
