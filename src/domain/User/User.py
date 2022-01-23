from datetime import datetime
from typing import List

from fastapi import File, UploadFile

from src.repository.User.User import User as UserRepository
from src.exceptions.ArgumentsIsNotSet import ArgumentsIsNotSet
from src.domain.Value.User.CreateUser import CreateValue
from src.domain.Value.User.UpdateUser import UpdateValue
from src.exceptions.NoSuchObjectException import NoSuchObjectException
from src.repository.File.User.UserFile import UserFile


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
        value_object = CreateValue(
            name=self.name, email=self.email, password=self.password
        )
        id = self.__repositpry.create(
            name=value_object.name,
            email=value_object.email,
            password=value_object.password,
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
        if id is None:
            raise ArgumentsIsNotSet("idにNoneがセットされています。")
        user = cls.__repositpry.read(id)
        if user is None:
            raise NoSuchObjectException("指定されたIDと一致するユーザーが存在しません。")
        return User(**user)

    @classmethod
    def all(cls, offset: int, limit: int) -> List["User"]:
        datas = cls.__repositpry.all(offset, limit)
        users = []
        for data in datas:
            users.append(User(**data))
        return users

    def update(
        self, *, name: str = None, email: str = None, password: str = None
    ) -> bool:
        updated = False
        value_object = UpdateValue(
            id=self.id, name=name, email=email, password=password
        )
        if name is not None:
            self.name = value_object.name
            updated = self.__repositpry.update(name=name, id=self.id)

        if email is not None:
            self.email = value_object.email
            updated = self.__repositpry.update(email=email, id=self.id)

        if password is not None:
            self.password = value_object.password
            updated = self.__repositpry.update(password=password, id=self.id)

        if updated:
            updated_user = self.read(self.id)
            self.updated_at = updated_user.updated_at

        return updated

    def regist_file(self, id: int, seq: int, file: UploadFile = File(...)) -> None:
        user_file = UserFile()
        user_file.regist(id, seq, file)

    def delete(self):
        self.__repositpry.delete(self.id)
