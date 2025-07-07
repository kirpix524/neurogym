from app.application.dtos.complex_data import CreateComplexElementDto
from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexDataModel
from app.infrastructure.db.models.complex_data import ComplexElementModel

class CreateComplexElementUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: CreateComplexElementDto) -> None:
        # Валидация
        if not dto.name.strip():
            raise ValueError("Название элемента не может быть пустым")

        # Проверяем, что parent_data существует и принадлежит пользователю
        parent_data = (
            self._session
                .query(ComplexDataModel)
                .filter_by(id=dto.data_id, owner_id=dto.owner_id)
                .first()
        )
        if parent_data is None:
            raise ValueError(f"Комплексные данные с id={dto.data_id} не найдены или нет доступа")

        # Определяем следующую позицию в цепочке
        try:
            next_position = len(parent_data.elements) + 1
        except AttributeError:
            next_position = None

        # Создаём новый элемент
        element = ComplexElementModel(
            name=dto.name,
            content=dto.content,
            comment=dto.comment,
            parent_data_id=dto.data_id,
            position=next_position
        )
        self._session.add(element)
        self._session.commit()