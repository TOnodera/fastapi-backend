from typing import List
import hashlib
from src.exceptions.NoSuchObjectException import NoSuchObjectException
from src.repository.DBConnection import DBConnection
from datetime import datetime


class User:
    def __init__(self) -> None:
        DBConnection.connect()
        self.users = DBConnection.get_users()
        self.session = DBConnection.get_session()

    def create(self, *, username: str, email: str, password: str) -> int:
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
        new_user = self.users(username=username, email=email, password=hashed_pass)
        self.session.add(new_user)
        self.session.commit()
        self.session.flush()
        return new_user.id

    def read(self, id) -> dict:
        orm = self.session.query(self.users).filter(self.users.id == id).first()
        if orm is not None:
            return {
                "id": orm.id,
                "username": orm.username,
                "email": orm.email,
                "created_at": orm.created_at,
                "updated_at": orm.updated_at,
            }
        return None

    def update(
        self, *, id: int, username: str = None, email: str = None, password: str = None
    ) -> bool:
        """
        データの更新を行う。

        Params
        -----
        id: int
        username: str
        email: str
        password: str

        Return
        -----
        updated: bool
            更新があった場合はtrueなければfalse
        """
        updated = False
        orm = self.session.query(self.users).filter(self.users.id == id).first()
        if username is not None and orm.username != username:
            orm.username = username
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
        user = self.session.query(self.users).filter(self.users.id == id).first()
        if user is not None:
            self.session.delete(user)
            self.session.commit()

    def read_by_email(self, email: str):
        return self.session.query(self.users).filter(self.users.email == email).first()

    def all(self, offset: int, limit: int) -> List[any]:
        users = self.session.query(self.users).offset(offset).limit(limit).all()
        results = []
        for user in users:
            results.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                }
            )
        return results
