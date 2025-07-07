from typing import List

from app.extensions import db
from app.infrastructure.db.models.word_pairs import WordPairSetModel, WordPairModel


class WordPairDataService:
    def __init__(self) -> None:
        self._session = db.session

    def get_word_pair_set(self, owner_id: int, set_id: int) -> WordPairSetModel:
        """
        Возвращает набор пар слов по его ID и владельцу.
        Бросает ValueError, если набор не найден или не принадлежит пользователю.
        """
        word_set = (
            self._session
                .query(WordPairSetModel)
                .filter_by(id=set_id, owner_id=owner_id)
                .first()
        )
        if word_set is None:
            raise ValueError(f"Набор пар слов с id={set_id} не найден.")
        return word_set

    def get_word_pairs(self, owner_id: int, set_id: int) -> List[WordPairModel]:
        """
        Возвращает список пар слов внутри указанного набора.
        Предварительно проверяет, что набор принадлежит пользователю.
        """
        # Проверяем доступ к самому набору
        self.get_word_pair_set(owner_id=owner_id, set_id=set_id)

        pairs = (
            self._session
                .query(WordPairModel)
                .filter_by(parent_id=set_id)
                .order_by(WordPairModel.id)
                .all()
        )
        return pairs