from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from sqlalchemy import DateTime
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

    name = Column('name', String, nullable=False)
    comment = Column('comment', String, nullable=True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column('created_at',DateTime,default=datetime.now,nullable=False)
    parent_folder_id = Column(Integer, ForeignKey('folders.id'), nullable=True)
    parent_folder = relationship(
        "FolderModel",
        remote_side="FolderModel.id",
        backref=backref('subfolders', cascade="all, delete-orphan")
    )
    complex_data_items = relationship(
        "ComplexDataModel",
        back_populates="folder",
        foreign_keys="ComplexDataModel.folder_id"
    )
    word_pair_set_items = relationship(
        "WordPairSetModel",
        back_populates="parent_folder",
        foreign_keys="WordPairSetModel.parent_folder_id",
        cascade="all, delete-orphan"
    )

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
        orm.owner_id = dom.owner_id if hasattr(dom, 'owner_id') else None
        for itm in dom.get_items():
            if isinstance(itm, DomainFolder):
                orm.subfolders.append(cls.from_domain(itm))
            elif isinstance(itm, DomainComplexData):
                orm.complex_data_items.append(ComplexDataModel.from_domain(itm))
            elif isinstance(itm, DomainWordPairSet):
                orm.word_pair_set_items.append(WordPairSetModel.from_domain(itm))
        return orm