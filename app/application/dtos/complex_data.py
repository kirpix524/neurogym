from typing import Optional
from datetime import datetime

class CreateComplexDataDto:
    def __init__(
        self,
        name: str,
        comment: Optional[str],
        parent_folder_id: Optional[int],
        owner_id: int
    ) -> None:
        self.name: str = name
        self.comment: Optional[str] = comment
        self.parent_folder_id: Optional[int] = parent_folder_id
        self.owner_id: int = owner_id

class ComplexDataDto:
    def __init__(
        self,
        id: int,
        name: str,
        comment: Optional[str],
        parent_folder_id: Optional[int],
        owner_id: int,
        created_at: datetime
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.comment: Optional[str] = comment
        self.parent_folder_id: Optional[int] = parent_folder_id
        self.owner_id: int = owner_id
        self.created_at: datetime = created_at

class UpdateComplexDataDto:
    def __init__(
        self,
        id: int,
        name: str,
        comment: Optional[str],
        owner_id: int
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.comment: Optional[str] = comment
        self.owner_id: int = owner_id

class CreateComplexElementDto:
    def __init__(
            self,
            name: str,
            content: str,
            comment: Optional[str],
            data_id: int,
            owner_id: int
    ) -> None:
        self.name: str = name
        self.content: str = content
        self.comment: Optional[str] = comment
        self.data_id: int = data_id
        self.owner_id: int = owner_id

class UpdateComplexElementDto:
    def __init__(
        self,
        id: int,
        name: str,
        content: str,
        comment: Optional[str],
        data_id: int,
        owner_id: int
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.content: str = content
        self.comment: Optional[str] = comment
        self.data_id: int = data_id
        self.owner_id: int = owner_id

class DeleteComplexElementDto:
    def __init__(
        self,
        id: int,
        data_id: int,
        owner_id: int
    ) -> None:
        self.id: int = id
        self.data_id: int = data_id
        self.owner_id: int = owner_id

class CreateAttributeForAllDto:
    def __init__(self, data_id: int, name: str, owner_id: int) -> None:
        self.data_id: int = data_id
        self.name: str = name
        self.owner_id: int = owner_id

class UpdateElementAttributeDto:
    def __init__(
        self,
        id: int,
        content: str,
        data_id: int,
        owner_id: int
    ) -> None:
        self.id: int = id
        self.content: str = content
        self.data_id: int = data_id
        self.owner_id: int = owner_id

class CreateChainForAllDto:
    def __init__(
        self,
        data_id: int,
        name: str,
        comment: Optional[str],
        owner_id: int
    ) -> None:
        self.data_id: int = data_id
        self.name: str = name
        self.comment: Optional[str] = comment
        self.owner_id: int = owner_id