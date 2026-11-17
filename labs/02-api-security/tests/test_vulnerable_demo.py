from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth, login


def test_reader_can_view_published_report_in_scope(secure_client: TestClient):
    headers = auth(login(secure_client, "alice", "alice12345"))
    response = secure_client.get("/api/reports/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["content"] == "team-a public report"


def test_reader_cannot_view_private_or_other_scope(secure_client: TestClient):
    headers = auth(login(secure_client, "alice", "alice12345"))
    assert secure_client.get("/api/reports/2", headers=headers).status_code == 404
    assert secure_client.get("/api/reports/3", headers=headers).status_code == 404


def test_reader_cannot_create_report(secure_client: TestClient):
    headers = auth(login(secure_client, "alice", "alice12345"))
    response = secure_client.post("/api/reports", headers=headers, json={"title": "Nope", "content": "nope"})
    assert response.status_code == 403


def test_editor_can_create_draft_but_not_publish(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    blocked = secure_client.post("/api/reports", headers=headers, json={"title": "Blocked", "content": "payload", "status": "published"})
    assert blocked.status_code == 422

    created = secure_client.post("/api/reports", headers=headers, json={"title": "Bob created", "content": "new draft"})
    assert created.status_code == 201
    assert created.json()["status"] == "draft"
    assert created.json()["scope_id"] == "team-a"


def test_editor_can_edit_own_draft_only(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    own = secure_client.patch("/api/reports/2", headers=headers, json={"content": "updated bob draft"})
    other = secure_client.patch("/api/reports/3", headers=headers, json={"content": "malicious"})
    published = secure_client.patch("/api/reports/1", headers=headers, json={"content": "malicious"})
    assert own.status_code == 200
    assert other.status_code == 404
    assert published.status_code == 404


def test_reader_cannot_edit_any_report(secure_client: TestClient):
    headers = auth(login(secure_client, "alice", "alice12345"))
    response = secure_client.patch("/api/reports/1", headers=headers, json={"content": "tampered"})
    assert response.status_code == 404


def test_editor_cannot_publish_report(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    response = secure_client.post("/api/reports/2/publish", headers=headers)
    assert response.status_code == 404


def test_administrator_can_publish_draft(secure_client: TestClient):
    headers = auth(login(secure_client, "admin", "admin12345"))
    response = secure_client.post("/api/reports/2/publish", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "published"


def test_patch_cannot_change_status_or_scope(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    response = secure_client.patch("/api/reports/2", headers=headers, json={"status": "published", "scope_id": "org-global"})
    assert response.status_code == 422


def test_list_reports_returns_only_visible_items(secure_client: TestClient):
    headers = auth(login(secure_client, "alice", "alice12345"))
    response = secure_client.get("/api/reports", headers=headers)
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [1]
