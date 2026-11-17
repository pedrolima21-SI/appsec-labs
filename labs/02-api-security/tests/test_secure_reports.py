from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, init_db
from app.main import app as secure_app
from app.vulnerable import app as vulnerable_app


def _seed_demo_state(db_session):
    from app.models import Report, User
    from app.auth import hash_password

    if db_session.query(User).count() > 0:
        return

    demo_users = [
        ("alice", "alice123", "reader", "team-a"),
        ("bob", "bob123", "editor", "team-a"),
        ("carol", "carol123", "editor", "team-b"),
        ("admin", "admin123", "administrator", "org-global"),
    ]

    for username, password, role, scope_id in demo_users:
        db_session.add(User(username=username, password_hash=hash_password(password), role=role, scope_id=scope_id))

    db_session.commit()
    users = db_session.query(User).all()
    owner_map = {u.username: u.id for u in users}

    db_session.add_all([
        Report(title="Public report", content="team-a public report", status="published", scope_id="team-a", owner_id=owner_map["alice"]),
        Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=owner_map["bob"]),
        Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=owner_map["carol"]),
        Report(title="Admin review", content="admin only report", status="published", scope_id="org-global", owner_id=owner_map["admin"]),
    ])
    db_session.commit()


@pytest.fixture
def secure_client() -> TestClient:
    temp_db = Path("/tmp") / "appsec_secure_test.db"
    os.environ["APP_DB_PATH"] = str(temp_db)
    init_db()
    db = SessionLocal()
    _seed_demo_state(db)
    db.close()
    return TestClient(secure_app)


@pytest.fixture
def vulnerable_client() -> TestClient:
    temp_db = Path("/tmp") / "appsec_vulnerable_test.db"
    os.environ["APP_DB_PATH"] = str(temp_db)
    init_db()
    db = SessionLocal()
    _seed_demo_state(db)
    db.close()
    return TestClient(vulnerable_app)


@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("alice", "alice123", 200),
        ("bob", "bob123", 200),
        ("admin", "admin123", 200),
        ("ghost", "wrong", 401),
    ],
)
def test_auth_token_paths(secure_client, username, password, expected):
    response = secure_client.post("/auth/token", json={"username": username, "password": password})
    assert response.status_code == expected


def test_reader_cannot_access_report_outside_scope(secure_client):
    token = secure_client.post("/auth/token", json={"username": "alice", "password": "alice123"}).json()["access_token"]
    response = secure_client.get("/api/reports/3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_editor_can_access_own_report(secure_client):
    token = secure_client.post("/auth/token", json={"username": "bob", "password": "bob123"}).json()["access_token"]
    response = secure_client.get("/api/reports/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_administrator_can_publish_report(secure_client):
    token = secure_client.post("/auth/token", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    response = secure_client.post("/api/reports/2/publish", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_vulnerable_mode_allows_cross_owner_access(vulnerable_client):
    token = vulnerable_client.post("/auth/token", json={"username": "alice", "password": "alice123"}).json()["access_token"]
    response = vulnerable_client.get("/api/reports/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_vulnerable_mode_allows_cross_owner_edit(vulnerable_client):
    token = vulnerable_client.post("/auth/token", json={"username": "alice", "password": "alice123"}).json()["access_token"]
    response = vulnerable_client.patch(
        "/api/reports/2",
        json={"content": "tampered by alice"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
