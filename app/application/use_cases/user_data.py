from datetime import datetime

from app.infrastructure.db.models.complex_data import ComplexDataModel
from app.infrastructure.db.models.folder import FolderModel
from typing import List, Optional, Type
from app.application.dtos.data_unit import DataUnitDTO
from app.infrastructure.db.models.word_pairs import WordPairSetModel


class DataService:
    def __init__(self, folder_model: Type[FolderModel] = FolderModel) -> None:
        self._folder_model: Type[FolderModel] = folder_model

    def get_data_units(
            self,
            owner_id: int,
            parent_folder_id: Optional[int] = None
    ) -> List[DataUnitDTO]:
        units: List[DataUnitDTO] = []

        # существующие папки
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
                comment=folder.comment,
                updated_at=folder.created_at,
                last_training=None
            ))

        # наборы пар слов
        word_sets = (
            WordPairSetModel.query
            .filter_by(owner_id=owner_id, parent_folder_id=parent_folder_id)
            .all()
        )
        for wp in word_sets:
            units.append(DataUnitDTO(
                id=wp.id,
                icon='file-earmark-text-fill',
                name=wp.name,
                type='пары слов',
                comment=wp.comment,
                updated_at=wp.created_at,
                last_training=wp.last_training if hasattr(wp, 'last_training') else None
            ))

        # комплексные данные
        complex_items = (
            ComplexDataModel.query
            .filter_by(owner_id=owner_id, folder_id=parent_folder_id, parent_element_id=None)
            .all()
        )
        for cd in complex_items:
            units.append(DataUnitDTO(
                id=cd.id,
                icon='file-earmark-code-fill',
                name=cd.name,
                type='комплексные данные',
                comment=cd.comment,
                updated_at=cd.created_at,
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

