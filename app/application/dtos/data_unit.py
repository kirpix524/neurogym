from datetime import datetime
from typing import Optional

class DataUnitDTO:
    def __init__(
        self,
        icon: str,
        name: str,
        type: str,
        updated_at: datetime,
        last_training: Optional[datetime]
    ) -> None:
        self._icon = icon
        self._name = name
        self._type = type
        self._updated_at = updated_at
        self._last_training = last_training

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def last_training(self) -> Optional[datetime]:
        return self._last_training
