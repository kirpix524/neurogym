from sqlalchemy.orm import joinedload

from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexDataModel

class ComplexDataService:
    def __init__(self) -> None:
        self._session = db.session

    def get_complex_data(self, owner_id: int, data_id: int) -> ComplexDataModel:
        """
        Возвращает комплексные данные с загруженными элементами (elements).
        Бросит ValueError, если не найдено или нет доступа.
        """
        complex_data = (
            self._session
                .query(ComplexDataModel)
                .options(joinedload(ComplexDataModel.elements))
                .filter_by(id=data_id, owner_id=owner_id)
                .first()
        )
        if complex_data is None:
            raise ValueError(f"Комплексные данные с id={data_id} не найдены или нет доступа.")
        return complex_data