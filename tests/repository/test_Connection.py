from src.exceptions.IsSingletonException import IsSingletonException
from fastapi.testclient import TestClient
from src.repository.DBConnection import DBConnection
import pytest


def test_Connection():
    DBConnection.connect(is_test=True)
    # 取得するqueryは必ず同じオブジェクト
    session1 = DBConnection.get_session()
    session2 = DBConnection.get_session()
    assert session1 is session2, print(session1, session2)

    # コンストラクタ経由でインスタンスを生成すると例外発生
    with pytest.raises(IsSingletonException):
        DBConnection()
