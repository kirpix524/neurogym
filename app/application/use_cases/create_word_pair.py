from app.application.dtos.word_pair import CreateWordPairDto
from app.infrastructure.db.models.word_pairs import WordPairModel
from app.extensions import db

class CreateWordPairUseCase:
    def __init__(self) -> None:
        # Здесь можно инжектировать репозиторий для тестируемости
        self._session = db.session

    def execute(self, dto: CreateWordPairDto) -> None:
        # Валидация
        if not dto.key.strip() or not dto.value.strip():
            raise ValueError("Оба слова должны быть непустыми")

        # Создаем модель и сохраняем в БД
        pair = WordPairModel(
            key=dto.key,
            value=dto.value,
            parent_id=dto.set_id
        )
        self._session.add(pair)
        self._session.commit()