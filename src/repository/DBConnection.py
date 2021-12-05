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

    @classmethod
    def connect(cls, is_test=False):
        if cls.__engine is None:
            if is_test:
                # テストの場合はテスト用DBを使用する
                user = os.environ["POSTGRES_TEST_USER"]
                password = os.environ["POSTGRES_TEST_PASSWORD"]
                password = os.environ["POSTGRES_TEST_PASSWORD"]
                host = os.environ["POSTGRES_TEST_HOST"]
                database = os.environ["POSTGRES_TEST_DATABASE"]
                port = os.environ["POSTGRES_PORT"]
            else:
                # 本番環境用接続データ
                user = os.environ["POSTGRES_USER"]
                password = os.environ["POSTGRES_PASSWORD"]
                password = os.environ["POSTGRES_PASSWORD"]
                host = os.environ["POSTGRES_HOST"]
                database = os.environ["POSTGRES_DATABASE"]
                port = os.environ["POSTGRES_PORT"]

            cls.__engine = create_engine(
                f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
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
