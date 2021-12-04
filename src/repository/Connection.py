import os
from sqlalchemy import create_engine

from src.exceptions.IsSingletonException import IsSingletonException

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
database = os.environ["POSTGRES_DATABASE"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}/{database}?charset=utf8mb4"
)


class DBConnection:
    __instanse = None

    @staticmethod
    def get_instance():
        if DBConnection.__instanse == None:
            DBConnection()
        return DBConnection.__instanse

    def __init__(self):
        if DBConnection.__instanse != None:
            raise IsSingletonException("複数のインスタンスを作成出来ません。")
        else:
            DBConnection.__instanse = self
