from app.application.dtos.complex_data import CreateAttributeForAllDto
from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexDataModel, ComplexAttributeModel


class CreateAttributeForAllUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: CreateAttributeForAllDto) -> None:
        # 1) Проверяем доступ к данным
        data = (
            self._session
                .query(ComplexDataModel)
                .filter_by(id=dto.data_id, owner_id=dto.owner_id)
                .first()
        )
        if data is None:
            raise ValueError(f"Комплексные данные {dto.data_id} не найдены")

        # 2) Для каждого элемента создаём запись атрибута
        for elem in data.elements:
            attr = ComplexAttributeModel(
                parent_element_id=elem.id,
                name=dto.name,
                content=''
            )
            self._session.add(attr)

        self._session.commit()