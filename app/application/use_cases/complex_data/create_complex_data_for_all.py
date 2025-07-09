from app.application.dtos.complex_data import CreateChainForAllDto
from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexDataModel


class CreateComplexDataForAllUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: CreateChainForAllDto) -> None:
        # проверяем доступ и загружаем исходные данные
        data = (
            self._session
                .query(ComplexDataModel)
                .options()
                .filter_by(id=dto.data_id, owner_id=dto.owner_id)
                .first()
        )
        if data is None:
            raise ValueError(f"Комплексные данные с id={dto.data_id} не найдены или нет доступа.")

        # создаём новую ComplexDataModel для каждого элемента
        for elem in data.elements:
            subchain = ComplexDataModel(
                name=dto.name,
                comment=dto.comment,
                owner_id=dto.owner_id,
                parent_element_id=elem.id
            )
            self._session.add(subchain)

        self._session.commit()