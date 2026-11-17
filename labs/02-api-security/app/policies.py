from __future__ import annotations

from fastapi import HTTPException, status

from app.models import Report, User


def is_admin(user: User) -> bool:
    return user.role == "administrator"


def can_read_report(user: User, report: Report) -> bool:
    if is_admin(user):
        return True
    if report.status == "draft":
        return report.owner_id == user.id
    return report.scope_id == user.scope_id


def can_edit_report(user: User, report: Report) -> bool:
    if is_admin(user):
        return True
    return report.owner_id == user.id and report.scope_id == user.scope_id


def can_publish_report(user: User, report: Report) -> bool:
    if is_admin(user):
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
