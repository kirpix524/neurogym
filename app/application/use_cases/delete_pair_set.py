from typing import Type

from app.extensions import db
from app.infrastructure.db.models.word_pairs import WordPairSetModel


class DeleteWordPairSetUseCase:
    def __init__(
        self,
        pair_set_model: Type[WordPairSetModel] = WordPairSetModel,
        db_session = db
    ) -> None:
        self._pair_set_model = pair_set_model
        self._db = db_session

    def execute(self, item_id: int, owner_id: int) -> None:
        """
        Удаляет набор пар слов, если он принадлежит пользователю.
        """
        pair_set = (
            self._pair_set_model.query
            .filter_by(id=item_id, owner_id=owner_id)
            .first()
        )
        if pair_set is None:
            raise ValueError("Набор пар не найден или доступ запрещён.")
        self._db.session.delete(pair_set)
        self._db.session.commit()