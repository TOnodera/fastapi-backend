import os
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
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
    def connect(cls):
        if cls.__engine is None:
            if "IS_TEST" in os.environ and int(os.environ["IS_TEST"]) == 1:
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

    @classmethod
    def now(cls):
        sql = text("SELECT NOW() AS NOW")
        return cls.__session.execute(sql)["NOW"]

    @classmethod
    def truncate_users(cls):
        """
        userテーブルを空にする。テストで使う。
        """
        sql = text("TRUNCATE table users;")
        cls.__session.execute(sql)
        cls.__session.commit()
