from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from app.domain.entities.models.complex_models import (
    ComplexData as DomainComplexData,
    ComplexElement as DomainComplexElement,
    ComplexAttribute as DomainComplexAttribute
)
from app.infrastructure.db.models.base_data import BaseData


class ComplexAttributeModel(BaseData):
    __tablename__ = 'complex_attributes'

    name = Column('name', String, nullable=False)
    content = Column('content', String, nullable=True)
    parent_element_id = Column(Integer, ForeignKey('complex_elements.id'))

    parent_element = relationship(
        "ComplexElementModel",
        back_populates="attributes"
    )

    def to_domain(self) -> DomainComplexAttribute:
        return DomainComplexAttribute(name=str(self.name), content=str(self.content))

    @classmethod
    def from_domain(cls, dom: DomainComplexAttribute) -> "ComplexAttributeModel":
        return cls(name=dom.name, content=dom.content)

class ComplexDataModel(BaseData):
    __tablename__ = 'complex_data'

    name = Column('name', String, nullable=True)
    comment = Column('comment', String, nullable=True)
    created_at = Column('created_at', DateTime, default=datetime.now, nullable=False)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'), nullable=True)
    parent_element_id = Column(Integer, ForeignKey('complex_elements.id'), nullable=True)
    parent_id = Column(Integer, ForeignKey('complex_data.id'), nullable=True)
    folder_id = Column(Integer, ForeignKey('folders.id'), nullable=True)

    elements = relationship(
        "ComplexElementModel",
        back_populates="parent_data",
        order_by="ComplexElementModel.position",
        cascade="all, delete-orphan",
        foreign_keys="ComplexElementModel.parent_data_id"
    )
    parent_element = relationship(
        "ComplexElementModel",
        back_populates="children_data",
        foreign_keys=[parent_element_id]
    )
    parent = relationship(
        "ComplexDataModel",
        remote_side="ComplexDataModel.id",
        back_populates="children",
        foreign_keys=[parent_id]
    )
    children = relationship(
        "ComplexDataModel",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy='select',
        foreign_keys=[parent_id]
    )
    folder = relationship(
        "FolderModel",
        back_populates="complex_data_items",
        foreign_keys=[folder_id]
    )

    def to_domain(self) -> DomainComplexData:
        dom = DomainComplexData(
            chain=[],
            name=str(self._name),
            comment=str(self._comment)
        )
        for elem in self._elements:
            child_dom = elem.to_domain()
            dom.add_element(child_dom)
        return dom

    @classmethod
    def from_domain(cls, dom: DomainComplexData) -> "ComplexDataModel":
        orm = cls(
            name=dom.name,
            comment=dom.comment,
            owner_id=None
        )
        for idx, elem in enumerate(dom.chain):
            elem_model = ComplexElementModel.from_domain(elem)
            elem_model.position = idx
            orm.elements.append(elem_model)
        return orm

class ComplexElementModel(BaseData):
    __tablename__ = 'complex_elements'

    content = Column('content', String, nullable=False)
    name = Column('name', String, nullable=True)
    comment = Column('comment', String, nullable=True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'), nullable=True)
    position = Column(Integer, nullable=False)
    parent_data_id = Column(Integer, ForeignKey('complex_data.id'))

    parent_data = relationship(
        "ComplexDataModel",
        back_populates="elements",
        foreign_keys=[parent_data_id]
    )
    attributes = relationship(
        "ComplexAttributeModel",
        back_populates="parent_element",
        cascade="all, delete-orphan"
    )
    children_data = relationship(
        ComplexDataModel,
        back_populates="parent_element",
        cascade="all, delete-orphan",
        single_parent=True,
        lazy="select",
        foreign_keys=[ComplexDataModel.parent_element_id]
    )

    def to_domain(self) -> DomainComplexElement:
        dom_elem = DomainComplexElement(
            content=str(self.content),
            name=str(self.name),
            comment=str(self.comment)
        )
        for attr in self.attributes:
            dom_elem.add_attribute(attr.name, attr.content)
        for child in self.children_data:
            child_dom = child.to_domain()
            dom_elem.add_child(child_dom)
        return dom_elem

    @classmethod
    def from_domain(cls, dom: DomainComplexElement) -> "ComplexElementModel":
        orm = cls(
            content=dom.content,
            name=dom.name,
            comment=dom.comment,
            owner_id=None,
            position=0
        )
        for attr in dom.get_attributes():
            orm.attributes.append(ComplexAttributeModel.from_domain(attr))
        for child in dom.get_children():
            orm.children_data.append(ComplexDataModel.from_domain(child))
        return orm


