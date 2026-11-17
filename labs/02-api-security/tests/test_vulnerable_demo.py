from __future__ import annotations

from fastapi.testclient import TestClient


def test_login_with_valid_credentials(secure_client: TestClient):
    response = secure_client.post("/auth/token", json={"username": "alice", "password": "alice123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_invalid_password_is_rejected(secure_client: TestClient):
    response = secure_client.post("/auth/token", json={"username": "alice", "password": "wrong"})
    assert response.status_code == 401


def test_missing_token_is_rejected(secure_client: TestClient):
    response = secure_client.get("/auth/me")
    assert response.status_code == 401


def test_vulnerable_mode_allows_cross_owner_read(vulnerable_client: TestClient):
    token = vulnerable_client.post("/auth/token", json={"username": "alice", "password": "alice123"}).json()["access_token"]
    response = vulnerable_client.get("/api/reports/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_secure_mode_blocks_cross_owner_read(secure_client: TestClient):
    token = secure_client.post("/auth/token", json={"username": "alice", "password": "alice123"}).json()["access_token"]
    response = secure_client.get("/api/reports/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
