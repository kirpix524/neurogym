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
        """
        Возвращает список единиц данных текущего пользователя,
        ограниченных по вложенности (parent_id=None — корневые папки)
        """
        units: List[DataUnitDTO] = []
        print(f"owner_id={owner_id}, parent_folder_id={parent_folder_id}")
        folders = (
            self._folder_model.query
            .filter_by(owner_id=owner_id, parent_folder_id=parent_folder_id)
            .all()
        )
        units.append(DataUnitDTO(
            icon='folder-fill',
            name="test folder",
            type='папка',
            updated_at=datetime.now(),
            last_training=None
        ))
        for folder in folders:
            units.append(DataUnitDTO(
                icon='folder-fill',
                name=folder.name,
                type='папка',
                updated_at=folder.created_at,
                last_training=None
            ))
        #добавить обработку файловых единиц данных
        return units

