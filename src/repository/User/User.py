from os import name
from src.repository.DBConnection import DBConnection
from src.domain.User.User import User as UserDomain


class User:
    def __init__(self) -> None:
        DBConnection.connect()
        self.users = DBConnection.get_users()
        self.session = DBConnection.get_session()

    def insert(self, user: UserDomain):
        new_user = self.users(name=user.name, email=user.email, password=user.password)
        self.session.add(new_user)
        self.session.commit()
