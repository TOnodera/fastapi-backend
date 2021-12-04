from src.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_create_user():
    body = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "very_secret_code",
    }
    response = client.post("/users/create", json=body)
    assert response.status_code == 201


def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
