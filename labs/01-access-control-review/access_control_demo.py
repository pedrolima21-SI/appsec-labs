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


ALLOWED_ADMIN_ACTIONS = {
    "view_report",
    "create_draft",
    "edit_draft",
    "publish_report",
    "manage_roles",
    "alter_config",
}


def allow_access(user: User, action: str, resource: Resource) -> bool:
    """Apply a conservative access-control policy for a fictional app.

    The rules are intentionally explicit: unknown roles and actions default to
    denial. Administrators are allowed only for actions defined in the lab.
    """
    if user.role not in {"reader", "editor", "administrator"}:
        return False

    if user.role == "administrator":
        return action in ALLOWED_ADMIN_ACTIONS

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


def run_scenarios() -> list[tuple[str, bool, bool]]:
    """Return a representative set of allowed/denied checks."""
    scenarios: list[tuple[str, bool, bool]] = [
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
            "editor can create a draft",
            allow_access(
                User("bob", "editor"),
                "create_draft",
                Resource("report", "Quarterly Summary", published=True),
            ),
            True,
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
            "editor cannot publish a report",
            allow_access(
                User("bob", "editor"),
                "publish_report",
                Resource("report", "Quarterly Summary", published=False),
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
        (
            "administrator can alter config",
            allow_access(
                User("admin", "administrator"),
                "alter_config",
                Resource("config", "Application configuration"),
            ),
            True,
        ),
        (
            "administrator cannot perform unknown action",
            allow_access(
                User("admin", "administrator"),
                "delete_everything",
                Resource("config", "Application configuration"),
            ),
            False,
        ),
        (
            "unknown role is denied by default",
            allow_access(
                User("ghost", "guest"),
                "view_report",
                Resource("report", "Quarterly Summary", published=True),
            ),
            False,
        ),
        (
            "unknown action is denied by default",
            allow_access(
                User("alice", "reader"),
                "read_private_data",
                Resource("report", "Quarterly Summary", published=True),
            ),
            False,
        ),
    ]
    return scenarios


def main() -> int:
    """Print scenario results and exit non-zero on mismatch."""
    print("Access control simulation for the fictional reporting app")
    print("Scenario | Expected | Outcome")
    failed = 0

    for name, actual, expected in run_scenarios():
        outcome = "PASS" if actual == expected else "FAIL"
        if outcome == "FAIL":
            failed += 1
        print(f"{name} | {expected} | {actual} ({outcome})")

    if failed:
        print(f"\nFAIL: {failed} scenario(s) did not match expected behavior.")
        return 1

    print("\nPASS: all access-control scenarios matched the expected policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
