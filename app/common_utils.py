from typing import List
from app.infrastructure.db.models.folder import FolderModel

def get_folder_path(folder: 'FolderModel') -> List['FolderModel']:
    folders_path = []
    while folder:
        folders_path.insert(0, folder)
        folder = folder.parent_folder

    return folders_path