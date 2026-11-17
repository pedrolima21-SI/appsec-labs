from __future__ import annotations

import os
from collections.abc import Iterator

os.environ.setdefault("JWT_SECRET", "test-only-jwt-secret-value-with-32-chars")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import create_app as create_secure_app
from app.models import Report, User
from app.auth import hash_password


def _seed_database(session) -> None:
    if session.query(User).count():
        return
    users = [
        User(username="alice", password_hash=hash_password("alice12345"), role="reader", scope_id="team-a", active=True),
        User(username="bob", password_hash=hash_password("bob12345"), role="editor", scope_id="team-a", active=True),
        User(username="carol", password_hash=hash_password("carol12345"), role="editor", scope_id="team-b", active=True),
        User(username="admin", password_hash=hash_password("admin12345"), role="administrator", scope_id="org-global", active=True),
        User(username="inactive", password_hash=hash_password("inactive12345"), role="reader", scope_id="team-a", active=False),
    ]
    session.add_all(users)
    session.flush()
    ids = {user.username: user.id for user in users}
    session.add_all([
        Report(title="Public summary", content="team-a public report", status="published", scope_id="team-a", owner_id=ids["alice"]),
        Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=ids["bob"]),
        Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=ids["carol"]),
        Report(title="Admin review", content="global review", status="published", scope_id="org-global", owner_id=ids["admin"]),
    ])
    session.commit()


@pytest.fixture
 def _invalid_marker():
    pass
