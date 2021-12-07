import pytest

from src.exceptions.ValidationException import ValidationException
from src.domain.User.User import User as UserDomain


def test_create():
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }
    user = UserDomain(**data)
    id = user.create()
    registered_data = user.read(id)

    assert isinstance(registered_data, UserDomain)
    assert registered_data.id == id
    assert registered_data.name == data["name"]
    assert registered_data.email == data["email"]
    assert registered_data.password is None
    assert registered_data.created_at is not None
    assert registered_data.updated_at is not None

    # メールアドレスの重複チェック
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }
    user2 = UserDomain(**data)
    with pytest.raises(ValidationException):
        user2.create()


def test_read():
    pass
    """
    user = UserDomain()
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }
    id: int = user.create(data)

    update_data = {
        "name": "test_string1",
        "email": "test_email@net.com2",
        "password": "password3",
    }
    user.update(update_data)

    registered_data = user.read(id)

    assert registered_data.id == id
    assert registered_data.name == data["name"]
    assert registered_data.email == data["email"]
    assert registered_data.password == hashlib.sha512(data["password"])
    assert registered_data.created_at is not None
    assert registered_data.updated_at is not None

    # メールアドレスの重複チェック
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }
    with pytest.raises(ValidationException):
        user.update(data)
    """


def test_update():
    pass


def test_delete():
    pass
