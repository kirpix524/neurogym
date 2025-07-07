from app.extensions import db
from app.application.dtos.complex_data import CreateComplexDataDto, ComplexDataDto
from app.infrastructure.db.models.complex_data import ComplexDataModel

class CreateComplexDataUseCase:
    def __init__(self) -> None:
        self._db = db

    def execute(self, dto: CreateComplexDataDto) -> ComplexDataDto:
        model = ComplexDataModel(
            name=dto.name,
            comment=dto.comment,
            owner_id=dto.owner_id,
            folder_id=dto.parent_folder_id
        )
        self._db.session.add(model)
        self._db.session.commit()
        return ComplexDataDto(
            id=model.id,
            name=model.name,
            comment=model.comment,
            parent_folder_id=model.folder_id,
            owner_id=model.owner_id,
            created_at=model.created_at
        )