from datetime import datetime
import re
from src.repository.User.User import User as UserRepository
from src.exceptions.ValidationException import ValidationException


class User:
    def __init__(
        self,
        *,
        name: str,
        email: str,
        password: str = None,
        id: int = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.__repo = UserRepository()
        self.__name = self.__validate_name(name)
        self.__email = self.__validate_email(email)
        self.__password = self.__validate_password(password)
        self.__id = self.__validate_id(id)
        self.__created_at = self.__validate_crerated_at(created_at)
        self.__updated_at = self.__validate_updated_at(updated_at)

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
    def id(self) -> str:
        return self.__id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    def __validate_name(self, name: str) -> None:
        return name

    def __validate_email(self, email: str) -> None:
        # メールアドレスの形式チェック
        if not re.match(r"^[a-zA-Z0-9.+_-]+[^.]@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$", email):
            raise ValidationException("メールアドレスの形式が不正です。")

        # 登録済みメールアドレスのチェック
        if self.__repo.read_by_email(email) is not None:
            raise ValidationException(f"{email}: メールアドレスは既に登録されています。")

        return email

    def __validate_password(self, password: str) -> None:
        if password is not None:
            if len(password) < 8:
                raise ValidationException("パスワードは8文字以上で入力してください。")
            if 32 < len(password):
                raise ValidationException("パスワードは32文字以内で入力してください。")
            return password

    def __validate_id(self, id: int) -> None:
        if id is not None:
            return id

    def __validate_crerated_at(self, created_at: datetime):
        if created_at is not None:
            return created_at

    def __validate_updated_at(self, updated_at: datetime):
        if updated_at is not None:
            return updated_at
