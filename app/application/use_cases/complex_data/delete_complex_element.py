from app.application.dtos.complex_data import DeleteComplexElementDto
from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexElementModel


class DeleteComplexElementUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: DeleteComplexElementDto) -> None:
        element = (
            self._session
                .query(ComplexElementModel)
                .filter_by(id=dto.id)
                .join(ComplexElementModel.parent_data)
                .filter_by(owner_id=dto.owner_id)
                .first()
        )
        if element is None:
            raise ValueError(f"Элемент с id={dto.id} не найден или нет доступа.")
        self._session.delete(element)
        self._session.commit()