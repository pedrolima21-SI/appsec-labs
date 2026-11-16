"""Access control demonstration for the fictional lab scenario.

This module intentionally models a small, local authorization policy for a
fictional reporting application. It is designed for didactic review and
cannot be treated as a validation of a real system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class User:
    username: str
    role: str


@dataclass(frozen=True)
class Resource:
    kind: str
    title: str
    owner: str | None = None
    published: bool = False


def allow_access(user: User, action: str, resource: Resource) -> bool:
    """Apply a small fictional authorization policy.

    The rules are intentionally conservative and are meant for study rather than
    production use.
    """
    if user.role == "administrator":
        return True

    if user.role == "editor":
        if action == "view_report" and resource.published:
            return True
        if action == "create_draft":
            return True
        if action == "edit_draft" and resource.kind == "draft":
            return resource.owner == user.username
        if action == "publish_report" and resource.kind == "report":
            return False
        return False

    if user.role == "reader":
        if action == "view_report" and resource.published:
            return True
        return False

    return False


def run_scenarios() -> Iterable[tuple[str, bool]]:
    """Return a representative set of allowed/denied checks."""
    scenarios = [
        (
            "reader can view a published report",
            allow_access(
                User("alice", "reader"),
                "view_report",
                Resource("report", "Quarterly Summary", published=True),
            ),
            True,
        ),
        (
            "reader cannot create a draft",
            allow_access(
                User("alice", "reader"),
                "create_draft",
                Resource("report", "Quarterly Summary", published=True),
            ),
            False,
        ),
        (
            "editor can edit own draft",
            allow_access(
                User("bob", "editor"),
                "edit_draft",
                Resource("draft", "Draft 01", owner="bob"),
            ),
            True,
        ),
        (
            "editor cannot edit another user's draft",
            allow_access(
                User("bob", "editor"),
                "edit_draft",
                Resource("draft", "Draft 02", owner="carol"),
            ),
            False,
        ),
        (
            "administrator can manage roles",
            allow_access(
                User("admin", "administrator"),
                "manage_roles",
                Resource("config", "Application configuration"),
            ),
            True,
        ),
    ]
    return scenarios


def main() -> int:
    """Print a simple scenario matrix for the fictional lab."""
    print("Access control simulation for the fictional reporting app")
    print("Scenario | Expected result | Outcome")
    for name, result, expected in run_scenarios():
        status = "ALLOW" if result else "DENY"
        outcome = "PASS" if result == expected else "FAIL"
        print(f"{name} | {expected} | {status} ({outcome})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
