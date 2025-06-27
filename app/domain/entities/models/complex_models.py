from typing import List, Optional, Tuple

class ComplexAttribute:
    def __init__(self, name: str, content: str) -> None:
        self._name = name
        self._content = content

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = value

class ComplexElement:
    def __init__(self,
                 content: str,
                 name: Optional[str] = None,
                 comment: Optional[str] = None
    ) -> None:
        self._content = content
        self._name = name
        self._comment = comment
        self._attributes: List[ComplexAttribute] = []
        self._children: List['ComplexData'] = []  # noqa: F821

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = value

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value

    @property
    def comment(self) -> Optional[str]:
        return self._comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        self._comment = value

    def add_attribute(self, name: str, content: str) -> None:
        attr = ComplexAttribute(name, content)
        self._attributes.append(attr)

    def get_attribute(self, name: str) -> Optional[str]:
        for attr in self._attributes:
            if attr.name == name:
                return attr.content
        return None

    def remove_attribute(self, name: str) -> None:
        self._attributes = [a for a in self._attributes if a.name != name]

    def get_attributes(self) -> List[ComplexAttribute]:
        return list(self._attributes)

    def add_child(self, child: 'ComplexData') -> None:  # noqa: F821
        self._children.append(child)

    def get_children(self) -> List['ComplexData']:  # noqa: F821
        return list(self._children)

    def remove_child(self, child: 'ComplexData') -> None:  # noqa: F821
        self._children = [c for c in self._children if c is not child]

class ComplexData:
    def __init__(self,
                 chain: Optional[List[ComplexElement]] = None,
                 name: Optional[str] = None,
                 comment: Optional[str] = None
    ) -> None:
        self._chain: List[ComplexElement] = chain or []
        self._name = name
        self._comment = comment

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value

    @property
    def comment(self) -> Optional[str]:
        return self._comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        self._comment = value

    @property
    def chain(self) -> List[ComplexElement]:
        return list(self._chain)

    def add_element(self, element: ComplexElement) -> None:
        self._chain.append(element)

    def remove_element(self, element: ComplexElement) -> None:
        self._chain = [e for e in self._chain if e is not element]

    def move_element(self, from_index: int, to_index: int) -> None:
        elem = self._chain.pop(from_index)
        self._chain.insert(to_index, elem)

    def collect_attribute(self, name: str) -> List[Tuple[str, Optional[str]]]:
        return [(e.content, e.get_attribute(name)) for e in self._chain]