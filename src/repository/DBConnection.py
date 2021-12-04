import os
from sqlalchemy import create_engine

from src.exceptions.IsSingletonException import IsSingletonException


class DBConnection:
    __engine = None

    def __init__(self) -> None:
        raise IsSingletonException()

    @classmethod
    def get_instance(cls):
        if cls.__engine is None:
            user = os.environ["POSTGRES_USER"]
            password = os.environ["POSTGRES_PASSWORD"]
            database = os.environ["POSTGRES_DATABASE"]
            password = os.environ["POSTGRES_PASSWORD"]
            host = os.environ["POSTGRES_HOST"]
            cls.__engine = create_engine(
                f"postgresql+psycopg2://{user}:{password}@{host}/{database}?charset=utf8mb4"
            )
        return cls.__engine
