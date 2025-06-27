from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.domain.entities.models.complex_models import (
    ComplexData as DomainComplexData,
    ComplexElement as DomainComplexElement,
    ComplexAttribute as DomainComplexAttribute
)
from app.infrastructure.db.models.base_data import BaseData

class ComplexAttributeModel(BaseData):
    __tablename__ = 'complex_attributes'

    _name = Column('name', String, nullable=False)
    _content = Column('content', String, nullable=False)
    parent_element_id = Column(Integer, ForeignKey('complex_elements.id'))

    parent_element = relationship(
        "ComplexElementModel",
        back_populates="_attributes"
    )

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

    def to_domain(self) -> DomainComplexAttribute:
        return DomainComplexAttribute(name=self._name, content=self._content)

    @classmethod
    def from_domain(cls, dom: DomainComplexAttribute) -> "ComplexAttributeModel":
        return cls(_name=dom.name, _content=dom.content)

class ComplexElementModel(BaseData):
    __tablename__ = 'complex_elements'

    _content = Column('content', String, nullable=False)
    _name = Column('name', String, nullable=True)
    _comment = Column('comment', String, nullable=True)
    position = Column(Integer, nullable=False)
    parent_data_id = Column(Integer, ForeignKey('complex_data.id'))

    parent_data = relationship(
        "ComplexDataModel",
        back_populates="_elements"
    )
    _attributes = relationship(
        "ComplexAttributeModel",
        back_populates="parent_element",
        cascade="all, delete-orphan"
    )
    children_data = relationship(
        "ComplexDataModel",
        backref=backref('parent_element', remote_side=[BaseData.id]),
        cascade="all, delete-orphan",
        lazy='dynamic'
    )

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

    def to_domain(self) -> DomainComplexElement:
        dom_elem = DomainComplexElement(
            content=self._content,
            name=self._name,
            comment=self._comment
        )
        for attr in self._attributes:
            dom_elem.add_attribute(attr.name, attr.content)
        for child in self.children_data:
            dom_elem.add_child(child.to_domain())
        return dom_elem

    @classmethod
    def from_domain(cls, dom: DomainComplexElement) -> "ComplexElementModel":
        orm = cls(
            _content=dom.content,
            _name=dom.name,
            _comment=dom.comment,
            position=0
        )
        for attr in dom.get_attributes():
            orm._attributes.append(ComplexAttributeModel.from_domain(attr))
        for child in dom.get_children():
            orm.children_data.append(ComplexDataModel.from_domain(child))
        return orm

class ComplexDataModel(BaseData):
    __tablename__ = 'complex_data'

    _name = Column('name', String, nullable=True)
    _comment = Column('comment', String, nullable=True)
    _elements = relationship(
        "ComplexElementModel",
        back_populates="parent_data",
        order_by="ComplexElementModel.position",
        cascade="all, delete-orphan"
    )
    parent_id = Column(Integer, ForeignKey('complex_data.id'), nullable=True)
    _children = relationship(
        "ComplexDataModel",
        backref=backref('parent', remote_side=[BaseData.id]),
        cascade="all, delete-orphan",
        lazy='dynamic'
    )

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

    def to_domain(self) -> DomainComplexData:
        dom = DomainComplexData(
            chain=[],
            name=self._name,
            comment=self._comment
        )
        for elem in self._elements:
            dom.add_element(elem.to_domain())
        return dom

    @classmethod
    def from_domain(cls, dom: DomainComplexData) -> "ComplexDataModel":
        orm = cls(
            _name=dom.name,
            _comment=dom.comment
        )
        for idx, elem in enumerate(dom.chain):
            elem_model = ComplexElementModel.from_domain(elem)
            elem_model.position = idx
            orm._elements.append(elem_model)
        return orm
