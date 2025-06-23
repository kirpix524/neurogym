from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.domain.entities.models.user import User
    from app.domain.repositories.interfaces.user_repo_interface import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, storage) -> None:
        self._storage = storage

    def add(self, email: str, hashed_password: str) -> User:
        pass

    def get_by_email(self, email: str) -> Optional[User]:
        pass

    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    def remove(self, user_id: int) -> None:
        pass