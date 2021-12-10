import hashlib
from sqlalchemy.sql import text
from src.repository.DBConnection import DBConnection
from datetime import datetime


class User:
    def __init__(self) -> None:
        DBConnection.connect()
        self.users = DBConnection.get_users()
        self.session = DBConnection.get_session()

    def create(self, *, name: str, email: str, password: str) -> int:
        """
        ユーザーデータの登録

        Parameters
        -----
        user: UserDomain

        Return
        -----
        id: int
            新しく登録されたデータを持つormオブジェクトのid


        """
        hashed_pass = hashlib.sha512(password.encode()).hexdigest()
        new_user = self.users(name=name, email=email, password=hashed_pass)
        self.session.add(new_user)
        self.session.commit()
        self.session.flush()
        return new_user.id

    def read(self, id) -> dict:
        orm = self.session.query(self.users).filter(self.users.id == id).one()
        return {
            "id": orm.id,
            "name": orm.name,
            "email": orm.email,
            "created_at": orm.created_at,
            "updated_at": orm.updated_at,
        }

    def update(
        self, *, id: int, name: str = None, email: str = None, password: str = None
    ) -> bool:
        """
        データの更新を行う。

        Params
        -----
        id: int
        name: str
        email: str
        password: str

        Return
        -----
        updated: bool
            更新があった場合はtrueなければfalse
        """
        updated = False
        orm = self.session.query(self.users).filter(self.users.id == id).one()
        if name is not None and orm.name != name:
            orm.name = name
            updated = True

        if email is not None and orm.email != email:
            orm.email = email
            updated = True

        if password is not None and orm.password != (
            new_password := hashlib.sha512(password.encode()).hexdigest()
        ):
            orm.password = new_password
            updated = True

        if updated:
            orm.updated_at = datetime.now()
            self.session.commit()

        return updated

    def delete(self, id: int):
        self.session.query(self.users).filter(self.users.id == id).delete()
        self.session.commit()

    def read_by_email(self, email: str):
        return self.session.query(self.users).filter(self.users.email == email).first()
