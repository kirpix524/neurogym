from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.domain.entities.models.word_pair_set import WordPairSet as DomainWPS
from app.infrastructure.db.models.base_data import BaseData


class WordPair(BaseData):
    __tablename__ = 'word_pairs'
    id = Column(Integer, primary_key=True)
    key = Column('key', String, nullable=False)
    value = Column('value', String, nullable=False)
    parent_id = Column(Integer, ForeignKey('word_pair_sets.id'))
    parent = relationship(
        "WordPairSetModel",
        back_populates="pairs"
    )

class WordPairSetModel(BaseData):
    __tablename__ = 'word_pair_sets'

    name = Column('name', String, nullable=True)
    comment = Column('comment', String, nullable=True)
    created_at = Column('created_at', DateTime, default=datetime.now, nullable=False)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'), nullable=True)
    parent_folder_id = Column('parent_folder_id',Integer,ForeignKey('folders.id'),nullable=True)
    pairs = relationship(
        "WordPair",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    parent_folder = relationship(
        "FolderModel",
        back_populates="word_pair_set_items",
        foreign_keys=[parent_folder_id]
    )

    def to_domain(self) -> DomainWPS:
        dom = DomainWPS(name=str(self.name), comment=str(self.comment))
        for p in self.pairs:
            dom.add_pair(p.key, p.value)
        return dom

    @classmethod
    def from_domain(cls, dom: DomainWPS) -> "WordPairSetModel":
        orm = cls(name=dom.name, comment=dom.comment)
        orm.owner_id = None
        for key, value in dom.pairs:
            wp = WordPair(key=key, value=value)
            orm.pairs.append(wp)
        return orm