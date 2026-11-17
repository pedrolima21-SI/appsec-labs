from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, init_db
from app.main import app as secure_app
from app.vulnerable import app as vulnerable_app


def build_client(app_object):
    return TestClient(app_object)


@pytest.fixture
def secure_client() -> TestClient:
    db_path = Path("/tmp") / "appsec_secure_test.db"
    os.environ["APP_DB_PATH"] = str(db_path)
    init_db()
    db = SessionLocal()
    from app.models import Report, User
    from app.auth import hash_password

    if db.query(User).count() == 0:
        for username, password, role, scope_id in [
            ("alice", "alice123", "reader", "team-a"),
            ("bob", "bob123", "editor", "team-a"),
            ("carol", "carol123", "editor", "team-b"),
            ("admin", "admin123", "administrator", "org-global"),
        ]:
            db.add(User(username=username, password_hash=hash_password(password), role=role, scope_id=scope_id))

        db.commit()
        users = db.query(User).all()
        user_map = {u.username: u.id for u in users}
        db.add_all([
            Report(title="Public report", content="team-a public report", status="published", scope_id="team-a", owner_id=user_map["alice"]),
            Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=user_map["bob"]),
            Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=user_map["carol"]),
            Report(title="Admin review", content="admin only report", status="published", scope_id="org-global", owner_id=user_map["admin"]),
        ])
        db.commit()
    db.close()
    return build_client(secure_app)


@pytest.fixture
def vulnerable_client() -> TestClient:
    db_path = Path("/tmp") / "appsec_vulnerable_test.db"
    os.environ["APP_DB_PATH"] = str(db_path)
    init_db()
    db = SessionLocal()
    from app.models import Report, User
    from app.auth import hash_password

    if db.query(User).count() == 0:
        for username, password, role, scope_id in [
            ("alice", "alice123", "reader", "team-a"),
            ("bob", "bob123", "editor", "team-a"),
            ("carol", "carol123", "editor", "team-b"),
            ("admin", "admin123", "administrator", "org-global"),
        ]:
            db.add(User(username=username, password_hash=hash_password(password), role=role, scope_id=scope_id))

        db.commit()
        users = db.query(User).all()
        user_map = {u.username: u.id for u in users}
        db.add_all([
            Report(title="Public report", content="team-a public report", status="published", scope_id="team-a", owner_id=user_map["alice"]),
            Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=user_map["bob"]),
            Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=user_map["carol"]),
            Report(title="Admin review", content="admin only report", status="published", scope_id="org-global", owner_id=user_map["admin"]),
        ])
        db.commit()
    db.close()
    return build_client(vulnerable_app)
