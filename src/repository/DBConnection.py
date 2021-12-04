import os
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from src.exceptions.DatabaseIsNotInitialized import DatabaseIsNotInitialized

from src.exceptions.IsSingletonException import IsSingletonException


class DBConnection:
    __engine = None
    __session = None
    __Users = None

    def __init__(self) -> None:
        raise IsSingletonException()

    @classmethod
    def __mapping(cls):
        """
        ORMにテーブルをマッピング
        """
        Base = automap_base()
        Base.prepare(cls.__engine, reflect=True)
        cls.__Users = Base.classes.users
        print(cls.__Users)

    @classmethod
    def connect(cls):
        if cls.__engine is None:
            user = os.environ["POSTGRES_USER"]
            password = os.environ["POSTGRES_PASSWORD"]
            database = os.environ["POSTGRES_DATABASE"]
            password = os.environ["POSTGRES_PASSWORD"]
            host = os.environ["POSTGRES_HOST"]
            cls.__engine = create_engine(
                f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
            )
            cls.__mapping()
            cls.__session = Session(cls.__engine)

    @classmethod
    def get_session(cls):
        if cls.__session is None:
            raise DatabaseIsNotInitialized()
        return cls.__session

    @classmethod
    def get_users(cls):
        if cls.__Users is None:
            raise DatabaseIsNotInitialized()
        return cls.__Users
