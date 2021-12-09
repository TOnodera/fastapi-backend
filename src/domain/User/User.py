from datetime import datetime
from os import EX_TEMPFAIL, environ, name
import re

from sqlalchemy.sql import selectable
from src.repository.User.User import User as UserRepository
from src.exceptions.ValidationException import ValidationException
from src.domain.Value.User import User as UserValue


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

        user_value = UserValue(name=self.name, email=self.email, password=self.password)

        id = self.__repositpry.create(
            name=user_value.name, email=user_value.email, password=user_value.password
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

    def delete(self):
        self.__repositpry.delete(self.id)
