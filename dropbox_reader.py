import dropbox
import os
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Dropbox access token
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
print('...authenticated with Dropbox owned by ' + dbx.users_get_current_account().name.display_name)

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
        
        print(f"Files found in {folder_path}: {files} \n")  # Debugging statement
        print(f"Folders found in {folder_path}: {folders} \n")  # Debugging statement
        
        # Recursively list files and folders in subfolders
        for folder in folders:
            sub_files, sub_folders = list_dropbox_files_and_folders(folder)
            files.extend(sub_files)
            folders.extend(sub_folders)
        
        return files, folders
    except dropbox.exceptions.ApiError as err:
        raise Exception(f"Failed to list files and folders: {err}")

def download_dropbox_file(file_path):
    """Download a file from Dropbox."""
    try:
        metadata, res = dbx.files_download(file_path)
        return BytesIO(res.content)
    except dropbox.exceptions.ApiError as err:
        raise Exception(f"Failed to download file: {err}")