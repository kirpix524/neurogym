# application/interfaces/user_interface.py
from abc import ABC, abstractmethod
from typing import Any, List

class IUser(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @email.setter
    @abstractmethod
    def email(self, email: str) -> None:
        pass

    @property
    @abstractmethod
    def hashed_password(self) -> str:
        pass

    @hashed_password.setter
    @abstractmethod
    def hashed_password(self, hashed_password: str) -> None:
        pass

    @abstractmethod
    def add_item(self, item: Any, folder_id: int) -> None:
        pass

    @abstractmethod
    def add_folder(self, folder: Any) -> None:
        pass

    @abstractmethod
    def remove_item(self, item_id: int) -> None:
        pass

    @abstractmethod
    def remove_folder(self, folder_id: int) -> None:
        pass

    @abstractmethod
    def list_items(self) -> List[Any]:
        pass
