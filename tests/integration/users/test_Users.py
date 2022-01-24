import os
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.repository.DBConnection import DBConnection
from src.exceptions.NoSuchObjectException import NoSuchObjectException
from src.config import settings
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
    # 登録リクエスト
    request_body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=request_body)
    id = response.json()["id"]

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


def test_delete_file():
    # 登録リクエスト
    request_body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=request_body)
    id = response.json()["id"]

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

        # ファイル削除リクエスト
        client.delete(f"/users/{id}/{seq}/delete-file")

        # ファイルの削除チェック
        ext = file_name.split(".")[-1]
        test_file_path = f"/home/python/app/storages/users/USER_{id}_{seq}.{ext}"
        assert not os.path.exists(test_file_path)


def test_delete_files():
    # 登録リクエスト
    request_body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=request_body)
    id = response.json()["id"]

    for seq in range(1, 10):
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

    # 削除リクエスト
    client.delete(f"/users/{id}/delete-files")

    for seq in range(1, 10):
        file_name = TEST_USER_IMAGE_FILE_PATH.split("/")[-1]
        # ファイルの削除チェック
        ext = file_name.split(".")[-1]
        test_file_path = f"/home/python/app/storages/users/USER_{id}_{seq}.{ext}"
        assert not os.path.exists(test_file_path)


def test_users_all():
    expects = []
    for i in range(10):
        # 登録リクエスト
        request_body = {
            "name": f"testuser_{i}",
            "email": f"test{i}@test.com",
            "password": "very_secret_code",
        }
        response = client.post("/users/create", json=request_body)
        # レスポンスとして期待するデータを登録しておく
        response_data = response.json()
        id = response_data["id"]
        expect = {
            "id": id,
            "name": request_body["name"],
            "email": request_body["email"],
            "paths": [],
        }
        # 画像を登録
        for seq in range(1, 10):
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
                test_file_path = (
                    f"/home/python/app/storages/users/USER_{id}_{seq}.{ext}"
                )
                assert os.path.exists(test_file_path)
                expect["paths"].append(
                    f"{settings.CLIENT_STORAGE_DIR}/users/USER_{id}_{seq}.{ext}"
                )

        expects.append(expect)

    responses = client.get("/users")
    users = responses.json()
    users = sorted(users, key=lambda user: user["id"])
    for index, user in enumerate(users):
        # 登録したデータが存在するか確認する
        assert expects[index]["id"] == user["id"]

        # 画像のパスが帰ってきてるかチェック
        for path in user["paths"]:
            # assert path in expects[index]["paths"]
            pass
