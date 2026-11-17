from __future__ import annotations

from fastapi.testclient import TestClient

from conftest import auth, login


def test_reader_reads_published_same_scope_only(secure_client: TestClient):
    headers = auth(login(secure_client, "alice", "alice12345"))
    assert secure_client.get("/api/reports/1", headers=headers).status_code == 200
    assert secure_client.get("/api/reports/2", headers=headers).status_code == 404
    assert secure_client.get("/api/reports/3", headers=headers).status_code == 404
    assert secure_client.get("/api/reports/4", headers=headers).status_code == 404


def test_reader_cannot_create_or_edit(secure_client: TestClient):
    headers = auth(login(secure_client, "alice", "alice12345"))
    assert secure_client.post("/api/reports", headers=headers, json={"title": "Denied", "content": "body"}).status_code == 403
    assert secure_client.patch("/api/reports/1", headers=headers, json={"content": "tamper"}).status_code == 404


def test_editor_can_create_draft_in_own_scope(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    response = secure_client.post("/api/reports", headers=headers, json={"title": "New draft", "content": "draft body"})
    assert response.status_code == 201
    assert response.json()["status"] == "draft"
    assert response.json()["scope_id"] == "team-a"
    assert response.json()["owner_id"] == 2


def test_report_create_rejects_mass_assignment(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    for extra in ({"status": "published"}, {"scope_id": "org-global"}, {"owner_id": 1}):
        response = secure_client.post("/api/reports", headers=headers, json={"title": "Invalid", "content": "body", **extra})
        assert response.status_code == 422


def test_editor_edits_only_own_draft(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    assert secure_client.patch("/api/reports/2", headers=headers, json={"content": "updated"}).status_code == 200
    assert secure_client.patch("/api/reports/3", headers=headers, json={"content": "tamper"}).status_code == 404
    assert secure_client.patch("/api/reports/1", headers=headers, json={"content": "tamper"}).status_code == 404


def test_patch_rejects_status_scope_and_owner(secure_client: TestClient):
    headers = auth(login(secure_client, "bob", "bob12345"))
    for extra in ({"status": "published"}, {"scope_id": "org-global"}, {"owner_id": 1}):
        assert secure_client.patch("/api/reports/2", headers=headers, json=extra).status_code == 422


def test_only_administrator_can_publish_draft_once(secure_client: TestClient):
    editor_headers = auth(login(secure_client, "bob", "bob12345"))
    admin_headers = auth(login(secure_client, "admin", "admin12345"))
    assert secure_client.post("/api/reports/2/publish", headers=editor_headers).status_code == 404
    published = secure_client.post("/api/reports/2/publish", headers=admin_headers)
    assert published.status_code == 200
    assert published.json()["status"] == "published"
    assert secure_client.post("/api/reports/2/publish", headers=admin_headers).status_code == 404


def test_administrator_can_read_all_but_cannot_edit_by_implicit_privilege(secure_client: TestClient):
    headers = auth(login(secure_client, "admin", "admin12345"))
    assert secure_client.get("/api/reports/3", headers=headers).status_code == 200
    assert secure_client.patch("/api/reports/2", headers=headers, json={"content": "edit"}).status_code == 404
