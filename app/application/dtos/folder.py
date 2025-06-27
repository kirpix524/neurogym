from typing import Optional
from datetime import datetime

class CreateFolderDto:
    def __init__(
        self,
        name: str,
        comment: Optional[str],
        owner_id: int
    ) -> None:
        self.name: str = name
        self.comment: Optional[str] = comment
        self.owner_id: int = owner_id

class FolderDto:
    def __init__(
        self,
        id: int,
        name: str,
        comment: Optional[str],
        owner_id: int,
        created_at: datetime
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.comment: Optional[str] = comment
        self.owner_id: int = owner_id
        self.created_at: datetime = created_at
