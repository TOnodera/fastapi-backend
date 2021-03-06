import time

import pytest
from sqlalchemy.exc import NoResultFound

from src.exceptions.NoSuchObjectException import NoSuchObjectException
from src.exceptions.ValidationException import ValidationException
from src.domain.User.User import User as UserDomain
from src.repository.DBConnection import DBConnection


@pytest.fixture(autouse=True)
def set_up():
    DBConnection.connect()
    DBConnection.truncate_users()


def test_create():
    data = {
        "username": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }
    user = UserDomain(**data)
    id = user.create()
    registered_data = user.read(id)

    assert isinstance(registered_data, UserDomain)
    assert registered_data.id == id
    assert registered_data.username == data["username"]
    assert registered_data.email == data["email"]
    assert registered_data.password is None
    assert registered_data.created_at is not None
    assert registered_data.updated_at is not None

    # メールアドレスの重複チェック
    data = {
        "username": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }

    user2 = UserDomain(**data)
    with pytest.raises(ValidationException):
        user2.create()

    # メールアドレスの形式チェック
    invalid_email_data = {
        "username": "test",
        "email": "this_is_email_daaaa",
        "password": "pass",
    }

    with pytest.raises(ValidationException):
        user = UserDomain(**invalid_email_data)
        user.create()


@pytest.mark.usefixtures("set_up")
def test_read():
    data = {
        "username": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }

    user = UserDomain(**data)
    id: int = user.create()

    registered_data = user.read(id)
    assert registered_data.id == id
    assert registered_data.username == data["username"]
    assert registered_data.email == data["email"]
    assert registered_data.created_at is not None
    assert registered_data.updated_at is not None


@pytest.mark.usefixtures("set_up")
def test_update():
    data = {
        "username": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }

    user = UserDomain(**data)
    id: int = user.create()

    registered_data = user.read(id)
    created_at = registered_data.created_at
    updated_at = registered_data.updated_at

    data2 = {
        "username": "test_string2",
        "email": "test_email2@net.com",
        "password": "password2",
    }

    time.sleep(1)
    user.update(**data2)

    assert user.username == data2["username"]
    assert user.email == data2["email"]
    assert user.created_at == created_at
    assert user.updated_at > updated_at


@pytest.mark.usefixtures("set_up")
def test_delete():
    data = {
        "username": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }

    user = UserDomain(**data)
    id: int = user.create()
    registered_data = user.read(id)

    registered_data.delete()

    with pytest.raises(NoSuchObjectException):
        user.read(id)


@pytest.mark.usefixtures("set_up")
def test_all():
    # テスト用データ作成
    id_list = []
    for i in range(10):
        data = {
            "username": f"test_user{i}",
            "email": f"test_email{i}@net.com",
            "password": "password",
        }
        user = UserDomain(**data)
        id = user.create()
        id_list.append(id)

    assert len(id_list) == 10

    # 登録したデータを取得できるかテスト
    users = UserDomain.all(0, 10)
    assert len(users) == 10

    for index, user in enumerate(users):
        assert user.username == f"test_user{index}"
        assert user.email == f"test_email{index}@net.com"
