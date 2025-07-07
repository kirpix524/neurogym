from typing import Type

from app.extensions import db
from app.infrastructure.db.models.folder import FolderModel

class DeleteFolderUseCase:
    def __init__(
        self,
        folder_model: Type[FolderModel] = FolderModel,
        db_session = db
    ) -> None:
        self._folder_model = folder_model
        self._db = db_session

    def execute(self, folder_id: int, owner_id: int) -> None:
        """
        Удаляет папку вместе с её содержимым, если она принадлежит пользователю.
        """
        folder = (
            self._folder_model.query
            .filter_by(id=folder_id, owner_id=owner_id)
            .first()
        )
        if folder is None:
            raise ValueError("Папка не найдена или доступ запрещён.")
        self._db.session.delete(folder)
        self._db.session.commit()
