from app.application.dtos.word_pair import UpdateWordPairDto
from app.extensions import db
from app.infrastructure.db.models.word_pairs import WordPairModel

class UpdateWordPairUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: UpdateWordPairDto) -> None:
        pair = (
            self._session
                .query(WordPairModel)
                .filter_by(id=dto.id, parent_id=dto.set_id)
                .first()
        )
        if pair is None:
            raise ValueError(f"Пара слов с id={dto.id} не найдена.")

        pair.key = dto.key
        pair.value = dto.value
        self._session.commit()