from typing import List, Tuple

class WordPairSet:
    def __init__(self, name: str = None, comment: str = None):
        self._name = name
        self._comment = comment
        self._pairs: List[Tuple[str, str]] = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._comment = value

    def add_pair(self, key: str, value: str) -> None:
        # здесь может быть валидация: например, дубли и т.п.
        self._pairs.append((key, value))

    def remove_pair(self, key: str) -> None:
        self._pairs = [p for p in self._pairs if p[0] != key]

    @property
    def pairs(self) -> List[Tuple[str, str]]:
        return list(self._pairs)
