from __future__ import annotations

from fastapi.testclient import TestClient


def test_register_user_creates_account(secure_client: TestClient):
    response = secure_client.post("/auth/register", json={"username": "dave", "password": "dave12345", "role": "reader", "scope_id": "team-c"})
    assert response.status_code == 200
    assert response.json()["username"] == "dave"


def test_auth_requires_token(secure_client: TestClient):
    response = secure_client.get("/auth/me")
    assert response.status_code == 401


def test_unknown_user_is_rejected(secure_client: TestClient):
    response = secure_client.post("/auth/token", json={"username": "ghost", "password": "does-not-matter"})
    assert response.status_code == 401
