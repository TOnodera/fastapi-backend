import hashlib
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import false, update
from src.repository.DBConnection import DBConnection
from src.domain.User.User import User as UserDomain


class User:
    def __init__(self, is_test=False) -> None:
        DBConnection.connect(is_test)
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

    def get(self, id) -> dict:
        orm = self.session.query(self.users).filter(self.users.id == id).one()
        return {"id": orm.id, "name": orm.name, "email": orm.email}

    def update(
        self, *, id: int, name: str = None, email: str = None, password: str = None
    ) -> bool:
        """
        データの更新を行う。

        Params
        -----
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
            self.session.commit()

        return updated

    def delete(self, id: int):
        orm = self.session.query(self.users).filter(self.users.id == id).one()
        self.session.delete(orm)

    def truncate(self):
        """
        userテーブルを空にする。テストで使う。
        """
        sql = text("TRUNCATE table users;")
        self.session.execute(sql)
