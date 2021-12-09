import pytest
import time
from sqlalchemy.exc import NoResultFound
from src.exceptions.ValidationException import ValidationException
from src.domain.User.User import User as UserDomain
from src.repository.User.User import User as UserRepository


@pytest.fixture
def set_up():
    repo = UserRepository()
    repo.truncate()


@pytest.mark.usefixtures("set_up")
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

    # メールアドレスの形式チェック
    invalid_email_data = {
        "name": "test",
        "email": "this_is_email_daaaa",
        "password": "pass",
    }

    with pytest.raises(ValidationException):
        UserDomain(**invalid_email_data)


@pytest.mark.usefixtures("set_up")
def test_read():
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }

    user = UserDomain(**data)
    id: int = user.create()

    registered_data = user.read(id)
    assert registered_data.id == id
    assert registered_data.name == data["name"]
    assert registered_data.email == data["email"]
    assert registered_data.created_at is not None
    assert registered_data.updated_at is not None


@pytest.mark.usefixtures("set_up")
def test_update():
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }

    user = UserDomain(**data)
    id: int = user.create()
    registered_data = user.read(id)
    created_at = registered_data.created_at
    updated_at = registered_data.updated_at

    data2 = {
        "name": "test_string2",
        "email": "test_email2@net.com",
        "password": "password2",
    }

    time.sleep(1)
    user.update(**data2)

    assert user.name == data2["name"]
    assert user.email == data2["email"]
    assert user.created_at == created_at
    assert user.updated_at > updated_at


def test_delete():
    data = {
        "name": "test_string",
        "email": "test_email@net.com",
        "password": "password",
    }

    user = UserDomain(**data)
    id: int = user.create()
    registered_data = user.read(id)

    registered_data.delete()

    with pytest.raises(NoResultFound):
        user.read(id)
