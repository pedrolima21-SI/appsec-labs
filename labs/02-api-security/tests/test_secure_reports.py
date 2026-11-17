from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth, login


def test_register_user_is_forced_to_reader_role(secure_client: TestClient):
    response = secure_client.post("/auth/register", json={"username": "newreader", "password": "newreader12345"})
    assert response.status_code == 201
    payload = response.json()
    assert payload["role"] == "reader"
    assert payload["username"] == "newreader"
    me = secure_client.get("/auth/me", headers=auth(payload["access_token"]))
    assert me.status_code == 200
    assert me.json()["role"] == "reader"
    assert me.json()["scope_id"] == "team-a"


def test_register_rejects_admin_role_and_scope_assignment(secure_client: TestClient):
    response = secure_client.post(
        "/auth/register",
        json={"username": "malicious-admin", "password": "maliciousadmin12345", "role": "administrator", "scope_id": "org-global"},
    )
    assert response.status_code == 422


def test_authentication_requires_valid_token(secure_client: TestClient):
    assert secure_client.get("/auth/me").status_code == 401
    assert secure_client.get("/api/reports").status_code == 401


def test_invalid_credentials_are_rejected(secure_client: TestClient):
    assert secure_client.post("/auth/token", json={"username": "alice", "password": "wrong-password"}).status_code == 401
    assert secure_client.post("/auth/token", json={"username": "ghost", "password": "anything"}).status_code == 401


def test_inactive_user_cannot_authenticate(secure_client: TestClient):
    response = secure_client.post("/auth/token", json={"username": "inactive", "password": "inactive12345"})
    assert response.status_code == 401


def test_login_returns_token_for_active_user(secure_client: TestClient):
    token_value = login(secure_client, "alice", "alice12345")
    assert isinstance(token_value, str)
    assert len(token_value) > 20
