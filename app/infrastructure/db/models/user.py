from typing import Optional
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app.config import SQL_DATA
from app.extensions import db


class User(db.Model):
    __tablename__ = SQL_DATA["users_table_name"]

    # Protected атрибуты БД
    _id = db.Column('id', db.Integer, primary_key=True)
    _username = db.Column('username', db.String(80), unique=True, nullable=True)
    _email = db.Column('email', db.String(120), unique=True, nullable=False)
    _password_hash = db.Column('password_hash', db.String(128), nullable=False)

    def __init__(self, email: str, username: Optional[str] = None) -> None:
        self._username = username
        self._email = email

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        if self._username is None:
            return self._email
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @hybrid_property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @property
    def password(self) -> None:
        raise AttributeError('Password is write-only.')

    @password.setter
    def password(self, raw_password: str) -> None:
        self._password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self._password_hash, raw_password)
