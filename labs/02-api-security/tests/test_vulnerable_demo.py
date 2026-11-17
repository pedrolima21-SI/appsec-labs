from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from conftest import auth, login


def test_vulnerable_api_allows_cross_owner_read_and_secure_api_blocks_it(vulnerable_client: TestClient, secure_client: TestClient):
    vulnerable_headers = auth(login(vulnerable_client, "alice", "alice12345"))
    secure_headers = auth(login(secure_client, "alice", "alice12345"))
    assert vulnerable_client.get("/api/reports/2", headers=vulnerable_headers).status_code == 200
    assert secure_client.get("/api/reports/2", headers=secure_headers).status_code == 404


def test_vulnerable_api_allows_cross_owner_edit_and_secure_api_blocks_it(vulnerable_client: TestClient, secure_client: TestClient):
    vulnerable_headers = auth(login(vulnerable_client, "alice", "alice12345"))
    secure_headers = auth(login(secure_client, "alice", "alice12345"))
    changed = vulnerable_client.patch("/api/reports/2", headers=vulnerable_headers, json={"content": "cross-owner update"})
    assert changed.status_code == 200
    assert changed.json()["content"] == "cross-owner update"
    assert secure_client.patch("/api/reports/2", headers=secure_headers, json={"content": "blocked update"}).status_code == 404


def test_vulnerable_app_requires_explicit_mode(monkeypatch):
    from app import config
    from app.vulnerable import create_app

    monkeypatch.setattr(config, "VULNERABLE_MODE", False)
    with pytest.raises(RuntimeError, match="VULNERABLE_MODE=true"):
        create_app(initialize_database=False)
