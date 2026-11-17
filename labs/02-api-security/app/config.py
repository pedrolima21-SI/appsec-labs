from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "api_security_lab.db"

# Prefer explicit DB path/URL but keep compatibility with older environment names.
DB_PATH = Path(os.getenv("APP_DB_PATH", str(DEFAULT_DB_PATH)))
DATABASE_URL = os.getenv("APP_DATABASE_URL") or f"sqlite:///{DB_PATH}"
JWT_SECRET = os.getenv("JWT_SECRET", "")
VULNERABLE_MODE = os.getenv("VULNERABLE_MODE", "false").strip().lower() in {"1", "true", "yes", "on"}
DEFAULT_SCOPE_ID = os.getenv("DEFAULT_SCOPE_ID", "team-a")

__all__ = ["BASE_DIR", "DB_PATH", "DATABASE_URL", "JWT_SECRET", "VULNERABLE_MODE", "DEFAULT_SCOPE_ID"]
