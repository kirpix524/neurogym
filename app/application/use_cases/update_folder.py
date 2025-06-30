# app/application/use_cases/update_folder.py

from typing import Type, Optional
from app.application.dtos.folder import UpdateFolderDto
from app.infrastructure.models import FolderModel, db

class UpdateFolderUseCase:
    def __init__(
        self,
        folder_model: Type[FolderModel] = FolderModel,
        db_session = db
    ) -> None:
        self._folder_model = folder_model
        self._db = db_session

    def execute(self, dto: UpdateFolderDto) -> None:
        """
        Обновляет имя и/или комментарий папки, если она принадлежит пользователю.
        """
        folder = (
            self._folder_model.query
            .filter_by(id=dto.id, owner_id=dto.owner_id)
            .first()
        )
        if folder is None:
            raise ValueError("Папка не найдена или доступ запрещён.")

        folder.name = dto.name
        folder.comment = dto.comment
        self._db.session.commit()
