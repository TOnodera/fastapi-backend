import pytest
import hashlib

from src.exceptions import ValidationException
from src.domain.User import User as UserDomain


def test_create():
    user = UserDomain()
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }
    id: int = user.create(**data)

    updated_data = user.read(id)

    assert isinstance(updated_data, UserDomain)
    assert updated_data.id == id
    assert updated_data.name == data["name"]
    assert updated_data.email == data["email"]
    assert updated_data.password == hashlib.sha512(data["password"])
    assert updated_data.created_at is not None
    assert updated_data.updated_at is not None

    # メールアドレスの重複チェック
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }
    with pytest.raises(ValidationException):
        user.create(data)


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

    updated_data = user.read(id)

    assert updated_data.id == id
    assert updated_data.name == data["name"]
    assert updated_data.email == data["email"]
    assert updated_data.password == hashlib.sha512(data["password"])
    assert updated_data.created_at is not None
    assert updated_data.updated_at is not None

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
