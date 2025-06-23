from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.domain.entities.models.user import User

class IUserRepository(ABC):
    @abstractmethod
    def add(self, email: str, hashed_password: str) -> 'User':
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional['User']:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional['User']:
        pass

    @abstractmethod
    def remove(self, user_id: int) -> None:
        pass