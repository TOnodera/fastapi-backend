from datetime import datetime
from os import EX_TEMPFAIL, name
import re

from sqlalchemy.sql import selectable
from src.repository.User.User import User as UserRepository
from src.exceptions.ValidationException import ValidationException


class User:

    __repositpry = UserRepository()

    def __init__(
        self,
        name: str,
        email: str,
        id: int = None,
        password: str = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    def create(self) -> int:
        # 必須項目入力チェック
        if self.name is None or self.name == "":
            raise ValidationException("氏名を入力してください。")
        if self.email is None or self.email == "":
            raise ValidationException("メールアドレスを入力してください。")
        if self.password is None or self.password == "":
            raise ValidationException("氏名を入力してください。")

        # メールアドレス形式チェック
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$",
            self.email,
        ):
            raise ValidationException("メールアドレスの形式で入力してください。")
        if self.__repositpry.read_by_email(self.email) is not None:
            raise ValidationException("入力されたメールアドレスは既に登録されています。")

        id = self.__repositpry.create(
            name=self.name, email=self.email, password=self.password
        )

        registered_user = self.read(id)

        self.id = id
        self.name = registered_user.name
        self.email = registered_user.email
        self.created_at = registered_user.created_at
        self.updated_at = registered_user.updated_at

        return id

    @classmethod
    def read(cls, id: int) -> "User":
        user = cls.__repositpry.read(id)
        return User(**user)

    def update(
        self, *, name: str = None, email: str = None, password: str = None
    ) -> bool:
        updated = False

        if name is not None:
            self.name = name
            updated = self.__repositpry.update(name=name, id=self.id)

        if email is not None:
            self.email = email
            updated = self.__repositpry.update(email=email, id=self.id)

        if password is not None:
            self.password = password
            updated = self.__repositpry.update(password=password, id=self.id)

        if updated:
            updated_user = self.read(self.id)
            self.updated_at = updated_user.updated_at

        return updated

    def delete(self, id: int):
        pass

    def __load(self, name: str = None, email: str = None, updated_at: datetime = None):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if updated_at is not None:
            self.update_at = updated_at
