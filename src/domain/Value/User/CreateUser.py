from datetime import datetime
import re
from src.repository.User.User import User as UserRepository
from src.exceptions.ValidationException import ValidationException


class CreateValue:
    def __init__(self, *, username: str, email: str, password: str = None):
        self.__repo = UserRepository()
        self.__username = self.__validate_username(username)
        self.__email = self.__validate_email(email)
        self.__password = self.__validate_password(password)

    @property
    def username(self) -> str:
        return self.__username

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    def __validate_username(self, username: str) -> str:

        if username is None:
            raise ValidationException("名前を入力してください。")

        return username

    def __validate_email(self, email: str) -> str:

        # メールアドレスの入力は必須
        if email is None:
            raise ValidationException("メールアドレスを入力してください。")
        # メールアドレスの形式チェック
        if not re.match(r"^[a-zA-Z0-9.+_-]+[^.]@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+$", email):
            raise ValidationException("メールアドレスの形式が不正です。")

        # 登録済みメールアドレスのチェック
        if self.__repo.read_by_email(email) is not None:
            raise ValidationException(f"{email}: メールアドレスは既に登録されています。")

        return email

    def __validate_password(self, password: str) -> str:

        if password is None:
            raise ValidationException("パスワードを入力してください。")

        if password is not None:
            if len(password) < 8:
                raise ValidationException("パスワードは8文字以上で入力してください。")
            if 32 < len(password):
                raise ValidationException("パスワードは32文字以内で入力してください。")

        return password
