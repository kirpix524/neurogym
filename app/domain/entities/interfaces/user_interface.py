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

    @property
    def user_name(self) -> str:
        pass

    @user_name.setter
    def user_name(self, user_name: str) -> None:
        pass
