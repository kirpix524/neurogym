from typing import List

from app.infrastructure.db.models.complex_data import ComplexDataModel, ComplexElementModel
from app.infrastructure.db.models.folder import FolderModel

def get_folder_path(folder: 'FolderModel') -> List['FolderModel']:
    folders_path = []
    while folder:
        folders_path.insert(0, folder)
        folder = folder.parent_folder

    return folders_path

def find_root_data(data_id: int) -> ComplexDataModel:
    """
    Если дали ComplexElementModel — переходим к его parent_data,
    иначе оставляем ComplexDataModel как есть.
    Затем по циклу поднимаемся по parent_element → parent_data до корня.
    """

    # Всегда возвращаемся к корневой цепочке, найденной от data_id
    root = ComplexDataModel.query.get(data_id)
    if not root:
        root = ComplexElementModel.query.get(data_id)
    if not root:
        raise ValueError(f'ComplexDataModel or ComplexElementModel with id={data_id} not found')
    while root.parent_element is not None:
        root = root.parent_element.parent_data

    return root