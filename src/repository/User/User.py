import hashlib
from os import name
from src.repository.DBConnection import DBConnection
from src.domain.User.User import User as UserDomain


class User:
    def __init__(self, is_test=False) -> None:
        DBConnection.connect(is_test)
        self.users = DBConnection.get_users()
        self.session = DBConnection.get_session()

    def insert(self, user: UserDomain):
        hashed_pass = hashlib.sha512(user.password.encode()).hexdigest()
        new_user = self.users(name=user.name, email=user.email, password=hashed_pass)
        self.session.add(new_user)
        self.session.commit()
        self.session.flush()
        return new_user
