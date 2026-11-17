from __future__ import annotations

from app.models import Report, User

VALID_ROLES = frozenset({"reader", "editor", "administrator"})


def is_known_user(user: User | None) -> bool:
    return user is not None and user.active and user.role in VALID_ROLES


def can_read_report(user: User, report: Report) -> bool:
    if not is_known_user(user):
        return False
    if user.role == "administrator":
        return True
    if report.status == "published":
        return report.scope_id == user.scope_id
    return report.owner_id == user.id and report.scope_id == user.scope_id


def can_create_report(user: User) -> bool:
    return is_known_user(user) and user.role in {"editor", "administrator"}


def can_edit_report(user: User, report: Report) -> bool:
    if not is_known_user(user):
        return False
    if user.role == "administrator":
        return True
    return report.owner_id == user.id and report.scope_id == user.scope_id and report.status == "draft"


def can_publish_report(user: User, report: Report) -> bool:
    if not is_known_user(user):
        return False
    return user.role == "administrator" and report.status == "draft"
