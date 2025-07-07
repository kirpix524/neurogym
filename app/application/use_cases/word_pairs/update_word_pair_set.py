from app.application.dtos.word_pair_set import UpdateWordPairSetDto
from app.extensions import db
from app.infrastructure.db.models.word_pairs import WordPairSetModel

class UpdateWordPairSetUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, dto: UpdateWordPairSetDto) -> None:
        word_set = (
            self._session
                .query(WordPairSetModel)
                .filter_by(id=dto.id, owner_id=dto.owner_id)
                .first()
        )
        if word_set is None:
            raise ValueError(f"Набор пар слов с id={dto.id} не найден или нет доступа.")

        word_set.name = dto.name
        word_set.comment = dto.comment
        self._session.commit()
