from __future__ import annotations

from fastapi.testclient import TestClient

from conftest import auth, login


def test_registration_forces_reader_and_server_scope(secure_client: TestClient):
    response = secure_client.post("/auth/register", json={"username": "new-reader", "password": "strong-password-123"})
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "reader"
    profile = secure_client.get("/auth/me", headers=auth(data["access_token"]))
    assert profile.status_code == 200
    assert profile.json()["scope_id"] == "team-a"


def test_registration_rejects_role_and_scope_mass_assignment(secure_client: TestClient):
    for extra in ({"role": "administrator"}, {"scope_id": "org-global"}):
        payload = {"username": "malicious-user", "password": "strong-password-123", **extra}
        assert secure_client.post("/auth/register", json=payload).status_code == 422


def test_login_and_bad_credentials(secure_client: TestClient):
    assert secure_client.post("/auth/token", json={"username": "alice", "password": "alice12345"}).status_code == 200
    assert secure_client.post("/auth/token", json={"username": "alice", "password": "wrong"}).status_code == 401
    assert secure_client.post("/auth/token", json={"username": "unknown", "password": "wrong"}).status_code == 401


def test_authentication_rejects_missing_and_invalid_tokens(secure_client: TestClient):
    assert secure_client.get("/auth/me").status_code == 401
    assert secure_client.get("/auth/me", headers=auth("invalid.token.value")).status_code == 401


def test_inactive_account_cannot_login(secure_client: TestClient):
    response = secure_client.post("/auth/token", json={"username": "inactive", "password": "inactive12345"})
    assert response.status_code == 401
