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