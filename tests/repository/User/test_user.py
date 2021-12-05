import hashlib

import pytest
from sqlalchemy.exc import NoResultFound

from src.repository.User.User import User as UserRepository
from src.domain.User.User import User as UserDomain


def set_up():
    user_repository = UserRepository(is_test=True)
    user_repository.truncate()
    return user_repository


def test_insert():
    name = "takeshi"
    email = "takeshi@mail.com"
    password = "password"
    user_repository = set_up()

    user_data = {"name": name, "email": email, "password": password}
    id = user_repository.insert(**user_data)

    got_user = user_repository.get(id)

    assert got_user["name"] == user_data["name"]
    assert got_user["email"] == user_data["email"]
    assert got_user["id"] == id


def test_get():
    name = "takeshi"
    email = "takeshi@mail.com"
    password = "password"
    user_repository = set_up()

    user_data = {"name": name, "email": email, "password": password}
    id = user_repository.insert(**user_data)

    got_user = user_repository.get(id)
    assert got_user["id"] == id


def test_update():
    name = "takeshi"
    email = "takeshi@mail.com"
    password = "password"
    user_repository = set_up()

    user_data = {"name": name, "email": email, "password": password}
    id = user_repository.insert(**user_data)

    updated_data = {"name": "onodera", "id": id}
    updated = user_repository.update(**updated_data)
    got_user = user_repository.get(id)

    assert updated
    assert got_user["name"] == updated_data["name"]


def test_delete():
    name = "takeshi"
    email = "takeshi@mail.com"
    password = "password"
    user_repository = set_up()

    user_data = {"name": name, "email": email, "password": password}
    id = user_repository.insert(**user_data)

    user_repository.delete(id)

    with pytest.raises(NoResultFound):
        user_repository.get(id)
