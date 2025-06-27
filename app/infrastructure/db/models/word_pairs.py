from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.entities.models.word_pair_set import WordPairSet as DomainWPS
from app.infrastructure.db.models.base_data import BaseData


class WordPair(BaseData):
    __tablename__ = 'word_pairs'
    id = Column(Integer, primary_key=True)
    _key = Column('key', String, nullable=False)
    _value = Column('value', String, nullable=False)
    parent_id = Column(Integer, ForeignKey('word_pair_sets.id'))
    parent = relationship(
        "WordPairSetModel",
        back_populates="_pairs"
    )

class WordPairSetModel(BaseData):
    __tablename__ = 'word_pair_sets'

    _name = Column('name', String, nullable=True)
    _comment = Column('comment', String, nullable=True)
    _owner_id = Column('owner_id', Integer, ForeignKey('users.id'), nullable=True)
    _pairs = relationship(
        "WordPair",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    parent_folder_id = Column(
        Integer,
        ForeignKey('folders.id'),
        nullable=True
    )

    parent_folder = relationship(
        "FolderModel",
        back_populates="word_pair_set_items",
        foreign_keys=[parent_folder_id]
    )

    @property
    def owner_id(self) -> Optional[int]:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: Optional[int]) -> None:
        self._owner_id = value

    def to_domain(self) -> DomainWPS:
        dom = DomainWPS(name=str(self._name), comment=str(self._comment))
        for p in self._pairs:
            dom.add_pair(p.key, p.value)
        return dom

    @classmethod
    def from_domain(cls, dom: DomainWPS) -> "WordPairSetModel":
        orm = cls(_name=dom.name, _comment=dom.comment)
        orm._owner_id = None
        for key, value in dom.pairs:
            wp = WordPair(_key=key, _value=value)
            orm._pairs.append(wp)
        return orm