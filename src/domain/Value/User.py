from datetime import datetime
from os import pread
import re

from sqlalchemy.engine import create_engine

from src.repository.User.User import User as UserRepository
from src.exceptions.ValidationException import ValidationException


class User:
    def __init__(
        self,
        *,
        name: str,
        email: str,
        password: str = None,
        crerated_at: datetime = None,
        updated_at: datetime = None
    ):
        self.__name = self.__validate_name(name)
        self.__email = self.__validate_email(email)
        self.__password = self.__validate_password(password)
        self.__created_at = self.__validate_crerated_at(crerated_at)
        self.__updated_at = self.__validate_updated_at(updated_at)
        self.__repo = UserRepository()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    def __validate_name(self, name: str) -> None:
        self.__name = name

    def __validate_email(self, email: str) -> None:
        # メールアドレスの形式チェック
        if not re.match(r"^[a-zA-Z0-9.-+_]+[^.]@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+", email):
            raise ValidationException("メールアドレスの形式が不正です。")

        # 登録済みメールアドレスのチェック
        if self.__repo.read_by_email(email) is not None:
            raise ValidationException("そのメールアドレスは既に登録されています。")

        self.__email = email

    def __validate_password(self, password: str) -> None:
        self.__password = password

    def __validate_crerated_at(self, created_at: datetime):
        if created_at is not None:
            self.__created_at = created_at

    def __validate_updated_at(self, updated_at: datetime):
        if updated_at is not None:
            self.__updated_at = updated_at
