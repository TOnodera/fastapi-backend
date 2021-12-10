from datetime import datetime
import re
from src.repository.User.User import User as UserRepository
from src.exceptions.ValidationException import ValidationException


class User:
    def __init__(
        self, *, id: int, name: str = None, email: str = None, password: str = None
    ):
        self.__repo = UserRepository()
        self.__name = self.__validate_name(name)
        self.__email = self.__validate_email(email)
        self.__password = self.__validate_password(password)
        self.__id = self.__validate_id(id)

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
    def id(self) -> int:
        return self.__id

    def __validate_name(self, name: str) -> str:
        return name

    def __validate_email(self, email: str) -> str:

        if email is not None:
            # メールアドレスの形式チェック
            if not re.match(
                r"^[a-zA-Z0-9.+_-]+[^.]@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$", email
            ):
                raise ValidationException("メールアドレスの形式が不正です。")

            # 登録済みメールアドレスのチェック
            if self.__repo.read_by_email(email) is not None:
                raise ValidationException(f"{email}: メールアドレスは既に登録されています。")

        return email

    def __validate_password(self, password: str) -> str:

        if password is not None:
            if len(password) < 8:
                raise ValidationException("パスワードは8文字以上で入力してください。")
            if 32 < len(password):
                raise ValidationException("パスワードは32文字以内で入力してください。")

        return password

    def __validate_id(self, id: int) -> int:

        if id is None:
            raise ValidationException("IDを入力してください。")
        if id <= 0:
            raise ValidationException("IDの値が不正です。")

        return id
