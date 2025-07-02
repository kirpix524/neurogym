from typing import Type

from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexDataModel


class DeleteComplexDataUseCase:
    def __init__(self, complex_data_model: Type[ComplexDataModel] = ComplexDataModel, db_session = db) -> None:
        self._complex_data_model = complex_data_model
        self._db = db_session

    def execute(self, item_id: int, owner_id: int) -> None:
        complex_data = (
            self._complex_data_model.query
            .filter_by(id=item_id, owner_id=owner_id)
            .first()
        )
        if complex_data is None:
            raise ValueError("Данные не найдены или доступ запрещён.")
        self._db.session.delete(complex_data)
        self._db.session.commit()