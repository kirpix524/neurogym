from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.entities.models.word_pair_set import WordPairSet as DomainWPS
from app.infrastructure.db import db


class WordPair(db.Model):
    __tablename__ = 'word_pairs'
    id = Column(Integer, primary_key=True)
    _key = Column('key', String, nullable=False)
    _value = Column('value', String, nullable=False)
    parent_id = Column(Integer, ForeignKey('word_pair_sets.id'))
    parent = relationship(
        "WordPairSetModel",
        back_populates="_pairs"
    )

class WordPairSetModel(db.Model):
    __tablename__ = 'word_pair_sets'
    id = Column(Integer, primary_key=True)
    _name = Column('name', String, nullable=True)
    _comment = Column('comment', String, nullable=True)

    _pairs = relationship(
        "WordPair",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    def to_domain(self) -> DomainWPS:
        dom = DomainWPS(name=str(self._name), comment=str(self._comment))
        for p in self._pairs:
            dom.add_pair(p.key, p.value)
        return dom

    @classmethod
    def from_domain(cls, dom: DomainWPS) -> "WordPairSetModel":
        orm = cls(_name=dom.name, _comment=dom.comment)
        for key, value in dom.pairs:
            wp = WordPair(_key=key, _value=value)
            orm._pairs.append(wp)
        return orm