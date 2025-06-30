from datetime import datetime

from app.infrastructure.db.models.folder import FolderModel
from typing import List, Optional, Type
from app.application.dtos.data_unit import DataUnitDTO

class DataService:
    def __init__(self, folder_model: Type[FolderModel] = FolderModel) -> None:
        self._folder_model: Type[FolderModel] = folder_model

    def get_data_units(
        self,
        owner_id: int,
        parent_folder_id: Optional[int] = None
    ) -> List[DataUnitDTO]:
        units: List[DataUnitDTO] = []
        folders = (
            self._folder_model.query
            .filter_by(owner_id=owner_id, parent_folder_id=parent_folder_id)
            .all()
        )
        for folder in folders:
            units.append(DataUnitDTO(
                id=folder.id,
                icon='folder-fill',
                name=folder.name,
                type='папка',
                updated_at=folder.created_at,
                last_training=None
            ))
        return units

    def get_folder_path(
        self,
        owner_id: int,
        parent_folder_id: Optional[int] = None
    ) -> List[FolderModel]:
        path: List[FolderModel] = []
        if parent_folder_id is None:
            return path
        folder = (
            self._folder_model.query
            .filter_by(id=parent_folder_id, owner_id=owner_id)
            .first()
        )
        while folder:
            path.append(folder)
            folder = folder.parent_folder
        return list(reversed(path))

