from app.application.dtos.complex_data import UpdateComplexDataDto
from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexDataModel


class UpdateComplexDataUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: UpdateComplexDataDto) -> None:
        complex_data = (
            self._session
                .query(ComplexDataModel)
                .filter_by(id=dto.id, owner_id=dto.owner_id)
                .first()
        )
        if complex_data is None:
            raise ValueError(f"Комплексные данные с id={dto.id} не найдены или нет доступа.")
        complex_data.name = dto.name
        complex_data.comment = dto.comment
        self._session.commit()