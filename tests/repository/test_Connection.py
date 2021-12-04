from src.exceptions.IsSingletonException import IsSingletonException
from src.main import app
from fastapi.testclient import TestClient
from src.repository.DBConnection import DBConnection
import pytest

client = TestClient(app)


def test_Connection():
    # 取得するインスタンスは必ず同じオブジェクト
    db1 = DBConnection.get_instance()
    db2 = DBConnection.get_instance()
    assert db1 is db2

    # コンストラクタ経由でインスタンスを生成すると例外発生
    with pytest.raises(IsSingletonException):
        DBConnection()
