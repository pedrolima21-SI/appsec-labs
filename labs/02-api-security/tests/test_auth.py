from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient


def _seed_demo_state(db) -> None:
    from app.auth import hash_password
    from app.models import Report, User

    if db.query(User).count() > 0:
        return

    users = [
        User(username="alice", password_hash=hash_password("alice12345"), role="reader", scope_id="team-a", active=True),
        User(username="bob", password_hash=hash_password("bob12345"), role="editor", scope_id="team-a", active=True),
        User(username="carol", password_hash=hash_password("carol12345"), role="editor", scope_id="team-b", active=True),
        User(username="admin", password_hash=hash_password("admin12345"), role="administrator", scope_id="org-global", active=True),
        User(username="inactive", password_hash=hash_password("inactive12345"), role="reader", scope_id="team-a", active=False),
    ]
    db.add_all(users)
    db.flush()
    user_map = {user.username: user.id for user in users}
    db.add_all(
        [
            Report(title="Public summary", content="team-a public report", status="published", scope_id="team-a", owner_id=user_map["alice"]),
            Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=user_map["bob"]),
            Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=user_map["carol"]),
            Report(title="Admin review", content="global review", status="published", scope_id="org-global", owner_id=user_map["admin"]),
        ]
    )
    db.commit()


@pytest.fixture
def secure_client(tmp_path, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "0123456789abcdef0123456789abcdef")
    monkeypatch.setenv("APP_DB_PATH", str(tmp_path / "secure.sqlite3"))
    monkeypatch.delenv("APP_DATABASE_URL", raising=False)

    import app.database as database_module
    import app.main as main_module
    import app.models as models_module

    importlib.reload(database_module)
    importlib.reload(models_module)
    importlib.reload(main_module)
    database_module.init_db()

    db = database_module.SessionLocal()
    _seed_demo_state(db)
    db.close()
    return TestClient(main_module.app)


@pytest.fixture
def vulnerable_client(tmp_path, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "0123456789abcdef0123456789abcdef")
    monkeypatch.setenv("APP_DB_PATH", str(tmp_path / "vulnerable.sqlite3"))
    monkeypatch.setenv("VULNERABLE_MODE", "true")
    monkeypatch.delenv("APP_DATABASE_URL", raising=False)

    import app.database as database_module
    import app.models as models_module
    import app.vulnerable as vulnerable_module

    importlib.reload(database_module)
    importlib.reload(models_module)
    importlib.reload(vulnerable_module)
    database_module.init_db()

    db = database_module.SessionLocal()
    _seed_demo_state(db)
    db.close()
    return TestClient(vulnerable_module.app)


def auth(token_value: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token_value}"}


def login(client: TestClient, username: str, password: str) -> str:
    response = client.post("/auth/token", json={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]
