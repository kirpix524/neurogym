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

    @property
    def user_name(self) -> str:
        pass

    @user_name.setter
    def user_name(self, user_name: str) -> None:
        pass