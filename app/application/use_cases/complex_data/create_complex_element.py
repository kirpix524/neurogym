from sqlalchemy.orm import joinedload

from app.application.dtos.complex_data import CreateComplexElementDto
from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexDataModel, ComplexAttributeModel
from app.infrastructure.db.models.complex_data import ComplexElementModel

class CreateComplexElementUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: CreateComplexElementDto) -> None:
        """
        Создает новый элемент цепочки в заданных комплексных данных (data_id),
        наследуя атрибуты и подчиненные цепочки от первого существующего элемента.
        """
        if not dto.name.strip():
            raise ValueError("Название элемента не может быть пустым")

        # Загружаем parent_data вместе с элементами и их дочерними цепочками
        parent_data = (
            self._session
                .query(ComplexDataModel)
                .options(
                    joinedload(ComplexDataModel.elements)
                      .joinedload(ComplexElementModel.children_data)
                )
                .filter_by(id=dto.data_id, owner_id=dto.owner_id)
                .first()
        )
        if parent_data is None:
            raise ValueError(f"Комплексные данные с id={dto.data_id} не найдены или нет доступа.")

        # Определяем позицию нового элемента
        next_position = len(parent_data.elements)

        # Создаем новый элемент
        element = ComplexElementModel(
            name=dto.name,
            content=dto.content or "",
            comment=dto.comment or "",
            parent_data_id=dto.data_id,
            position=next_position,
            owner_id=dto.owner_id
        )
        self._session.add(element)
        self._session.flush()

        # Наследуем атрибуты и дочерние цепочки от первого сиблинга, если он есть
        if parent_data.elements:
            sibling = parent_data.elements[0]
            for attr in sibling.attributes:
                new_attr = ComplexAttributeModel(
                    parent_element_id=element.id,
                    name=attr.name,
                    content=''
                )
                self._session.add(new_attr)
            for child_chain in sibling.children_data:
                new_chain = ComplexDataModel(
                    name=child_chain.name,
                    comment=child_chain.comment,
                    owner_id=dto.owner_id,
                    parent_element_id=element.id
                )
                self._session.add(new_chain)

        self._session.commit()