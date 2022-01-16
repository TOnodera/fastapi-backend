import os
from pydoc import cli
from _pytest.monkeypatch import resolve
import pytest

from fastapi.testclient import TestClient

from src.main import app
from src.repository.DBConnection import DBConnection
from src.exceptions.NoSuchObjectException import NoSuchObjectException
from tests.config import TEST_USER_IMAGE_FILE_PATH

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


def test_update_user():
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
    response = client.put(f"/users/{registered_id}", json=update_body)
    assert response.status_code == 200

    # 更新を確認
    response = client.get(f"/users/{registered_id}")
    response_data = response.json()
    assert update_body["name"] == response_data["name"]
    assert update_body["email"] == response_data["email"]
    assert "password" not in response_data


def test_delete_user():
    # 登録リクエスト
    request_body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=request_body)
    registered_id = response.json()["id"]

    # 削除リクエスト
    response = client.delete(f"/users/{registered_id}")
    assert response.status_code == 204

    # データ取得
    response = client.get(f"/users/{registered_id}")


def test_upload_file():
    id = 999999
    seq = 1
    with open(TEST_USER_IMAGE_FILE_PATH, "rb") as f:
        file_name = TEST_USER_IMAGE_FILE_PATH.split("/")[-1]
        response = client.post(
            f"/users/{id}/{seq}/upload-file",
            files={"file": (file_name, f, "image/png")},
        )

        # レスポンスコード確認
        assert response.status_code < 300
        # ファイルの存在チェック
        ext = file_name.split(".")[-1]
        test_file_path = f"/home/python/app/storages/users/USER_{id}_{seq}.{ext}"
        assert os.path.exists(test_file_path)

        # 後始末
        os.remove(test_file_path)
