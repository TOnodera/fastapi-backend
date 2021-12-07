from datetime import datetime

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
            ValidationException("氏名を入力してください。")
        if self.email is None or self.email == "":
            ValidationException("メールアドレスを入力してください。")
        if self.password is None or self.password == "":
            ValidationException("氏名を入力してください。")

        if self.__repositpry.read_by_email(self.email) is not None:
            ValidationException("入力されたメールアドレスは既に登録されています。")

        return self.__repositpry.create(
            name=self.name, email=self.email, password=self.password
        )

    @classmethod
    def read(cls, id: int) -> "User":
        user = cls.__repositpry.read(id)
        return User(**user)
