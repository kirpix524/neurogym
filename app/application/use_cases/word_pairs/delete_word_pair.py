from app.extensions import db
from app.infrastructure.db.models.word_pairs import WordPairModel

class DeleteWordPairUseCase:
    def __init__(self) -> None:
        self._session = db.session

    def execute(self, pair_id: int, set_id: int) -> None:
        pair = (
            self._session
                .query(WordPairModel)
                .filter_by(id=pair_id, parent_id=set_id)
                .first()
        )
        if pair is None:
            raise ValueError(f"Пара слов с id={pair_id} не найдена или нет доступа.")
        self._session.delete(pair)
        self._session.commit()