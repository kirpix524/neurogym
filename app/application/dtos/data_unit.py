from datetime import datetime
from typing import Optional

class DataUnitDTO:
    def __init__(
        self,
        id: int,
        icon: str,
        name: str,
        type: str,
        comment: Optional[str],
        updated_at: datetime,
        last_training: Optional[datetime]
    ) -> None:
        self.id = id
        self.icon = icon
        self.name = name
        self.type = type
        self.comment = comment
        self.updated_at = updated_at
        self.last_training = last_training
