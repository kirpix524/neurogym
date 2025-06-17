# domain/entities/user.py

from typing import Any, List

from app.domain.entities.interfaces.user_interface import IUser


class User(IUser):
    def __init__(self, id: int, email: str, hashed_password: str):
        pass

    @property
    def id(self) -> int:
        pass

    @property
    def email(self) -> str:
        pass

    @email.setter
    def email(self, email: str) -> None:
        pass

    @property
    def hashed_password(self) -> str:
        pass

    @hashed_password.setter
    def hashed_password(self, hashed_password: str) -> None:
        pass

    def add_item(self, item: Any, folder_id: int) -> None:
        pass

    def remove_item(self, item_id: int) -> None:
        pass

    def list_items(self) -> List[Any]:
        pass

    def remove_folder(self, folder_id: int) -> None:
        pass

    def add_folder(self, folder: Any) -> None:
        pass
