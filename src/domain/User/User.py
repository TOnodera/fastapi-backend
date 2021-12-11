from datetime import datetime

from src.repository.User.User import User as UserRepository
from src.exceptions.ArgumentsIsNotSet import ArgumentsIsNotSet
from src.domain.Value.User.CreateUser import CreateValue
from src.domain.Value.User.UpdateUser import UpdateValue


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
        if id is not None:
            user = cls.__repositpry.read(id)
            return User(**user)
        raise ArgumentsIsNotSet("idにNoneがセットされています。")

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

    def delete(self):
        self.__repositpry.delete(self.id)
