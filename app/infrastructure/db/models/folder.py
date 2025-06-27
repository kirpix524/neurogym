from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, backref
from app.domain.entities.models.complex_models import (
    ComplexData as DomainComplexData
)
from app.domain.entities.models.folder import Folder as DomainFolder

from app.domain.entities.models.word_pair_set import WordPairSet as DomainWordPairSet
from app.infrastructure.db.models.base_data import BaseData
from app.infrastructure.db.models.word_pairs import WordPairSetModel
from app.infrastructure.db.models.complex_data import ComplexDataModel

class FolderModel(BaseData):
    __tablename__ = 'folders'

    _name = Column('name', String, nullable=False)
    _comment = Column('comment', String, nullable=True)
    parent_folder_id = Column(Integer, ForeignKey('folders.id'), nullable=True)

    parent_folder = relationship(
        "FolderModel",
        remote_side=[BaseData.id],
        backref=backref('subfolders', cascade="all, delete-orphan")
    )
    complex_data_items = relationship(
        "ComplexDataModel",
        backref=backref('folder', cascade="all")
    )
    word_pair_set_items = relationship(
        "WordPairSetModel",
        backref=backref('folder', cascade="all")
    )

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

    def to_domain(self) -> DomainFolder:
        dom = DomainFolder(name=self._name, comment=self._comment)
        for sub in self.subfolders:
            dom.add_item(sub.to_domain())
        for item in self.complex_data_items:
            dom.add_item(item.to_domain())
        for wp in self.word_pair_set_items:
            dom.add_item(wp.to_domain())
        return dom

    @classmethod
    def from_domain(cls, dom: DomainFolder) -> "FolderModel":
        orm = cls(_name=dom.name, _comment=dom.comment)
        for itm in dom.get_items():
            if isinstance(itm, DomainFolder):
                orm.subfolders.append(cls.from_domain(itm))
            elif isinstance(itm, DomainComplexData):
                orm.complex_data_items.append(ComplexDataModel.from_domain(itm))
            elif isinstance(itm, DomainWordPairSet):
                orm.word_pair_set_items.append(WordPairSetModel.from_domain(itm))
        return orm