from _pytest.monkeypatch import resolve
import pytest

from fastapi.testclient import TestClient

from src.main import app
from src.repository.DBConnection import DBConnection

client = TestClient(app)


@pytest.fixture(autouse=True)
def set_up():
    DBConnection.connect()
    DBConnection.truncate_users()


def test_create_user():
    request_body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=request_body)
    assert response.status_code == 201


def test_read_users():
    request_body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }

    response = client.post("/users/create", json=request_body)
    registered_id = response.json()["id"]

    response = client.get(f"/users/{registered_id}")
    response_data = response.json()

    assert response.status_code == 200
    assert request_body["name"] == response_data["name"]
    assert request_body["email"] == response_data["email"]
    assert "password" not in response_data


@pytest.mark.skip
def update():

    # 登録リクエスト
    request_body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=request_body)
    registered_id = response.json()["id"]

    # 更新リクエスト
    update_body = {
        "name": "update_test_user",
        "email": "update_test@test.com",
        "password": "update_password",
    }
    response = client.put(f"/users/{registered_id}")
    assert response.status_code == 200

    # 更新を確認
    response = client.read(f"/users/{registered_id}")
    response_data = response.json()
    assert update_body["name"] == response_data["name"]
    assert update_body["email"] == response_data["email"]
    assert "password" not in response_data
