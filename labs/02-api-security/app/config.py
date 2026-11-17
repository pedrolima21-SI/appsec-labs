from __future__ import annotations

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.getenv("APP_DB_PATH", str(BASE_DIR / "data" / "api_security_lab.db")))
JWT_SECRET = os.getenv("JWT_SECRET", "local-demo-secret")
VULNERABLE_MODE = os.getenv("VULNERABLE_MODE", "false").lower() == "true"

__all__ = ["BASE_DIR", "DB_PATH", "JWT_SECRET", "VULNERABLE_MODE"]
