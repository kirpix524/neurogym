from typing import List, Optional, Union
from app.domain.entities.models.complex_models import ComplexData
from app.domain.entities.models.word_pair_set import WordPairSet


class Folder:
    def __init__(
        self,
        name: str,
        comment: Optional[str] = None,
        items: Optional[List[Union['Folder', ComplexData, WordPairSet]]] = None
    ) -> None:
        self._name = name
        self._comment = comment
        self._items: List[Union[Folder, ComplexData, WordPairSet]] = items or []  # noqa: F821

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def comment(self) -> Optional[str]:
        return self._comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        self._comment = value

    def add_item(self, item: Union['Folder', ComplexData, WordPairSet]) -> None:
        self._items.append(item)

    def remove_item(self, item: Union['Folder', ComplexData, WordPairSet]) -> None:
        self._items = [i for i in self._items if i is not item]

    def get_items(self) -> List[Union['Folder', ComplexData, WordPairSet]]:
        return list(self._items)