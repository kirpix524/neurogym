from typing import Optional
from app.extensions import db
from app.application.dtos.folder import CreateFolderDto, FolderDto
from app.infrastructure.db.models.folder import FolderModel

class CreateFolderUseCase:
    def __init__(self) -> None:
        self._db = db

    def execute(self, dto: CreateFolderDto) -> FolderDto:
        folder = FolderModel(
            name=dto.name,
            comment=dto.comment,
            owner_id=dto.owner_id,
            parent_folder_id = dto.parent_id
        )
        self._db.session.add(folder)
        self._db.session.commit()

        return FolderDto(
            id=folder.id,
            name=folder.name,
            comment=folder.comment,
            owner_id=folder.owner_id,
            created_at=folder.created_at
        )
