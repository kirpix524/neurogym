from app.application.dtos.complex_data import UpdateElementAttributeDto
from app.extensions import db
from app.infrastructure.db.models.complex_data import ComplexAttributeModel


class UpdateElementAttributeUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: UpdateElementAttributeDto) -> None:
        """
        Обновляет поле content для конкретного атрибута элемента,
        проверяя, что атрибут существует и принадлежит текущему пользователю.
        """
        # 1. Находим атрибут по его ID
        attribute = (
            self._session
                .query(ComplexAttributeModel)
                .filter_by(id=dto.id)
                .first()
        )
        if attribute is None:
            raise ValueError(f"Атрибут с id={dto.id} не найден.")

        # 2. Проверяем права доступа через связь к ComplexDataModel
        #    Предполагается, что ComplexElementAttributeModel.element → ComplexElementModel
        #    и ComplexElementModel.parent_data → ComplexDataModel
        if attribute.parent_element.owner_id != dto.owner_id:
            raise ValueError("Нет прав на изменение этого атрибута.")

        # 3. Обновляем содержимое и сохраняем
        attribute.content = dto.content
        self._session.commit()