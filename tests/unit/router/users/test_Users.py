from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_user():
    body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=body)
    assert response.status_code == 201


def test_read_users():
    response = client.get("/users/1")
    assert response.status_code == 200
