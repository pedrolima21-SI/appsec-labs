from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.config import DEFAULT_SCOPE_ID
from app.database import get_db, init_db
from app.models import Report, User
from app.policies import can_create_report, can_edit_report, can_publish_report, can_read_report
from app.schemas import ReportCreate, ReportRead, ReportUpdate, TokenResponse, UserLogin, UserRegister

app = FastAPI(title="AppSec Labs - Secure Reporting API", version="1.0.0")


def seed_demo_data(db: Session) -> None:
    if db.scalar(select(User.id).limit(1)) is not None:
        return

    users = [
        User(username="alice", password_hash=hash_password("alice12345"), role="reader", scope_id="team-a", active=True),
        User(username="bob", password_hash=hash_password("bob12345"), role="editor", scope_id="team-a", active=True),
        User(username="carol", password_hash=hash_password("carol12345"), role="editor", scope_id="team-b", active=True),
        User(username="admin", password_hash=hash_password("admin12345"), role="administrator", scope_id="org-global", active=True),
        User(username="inactive", password_hash=hash_password("inactive12345"), role="reader", scope_id="team-a", active=False),
    ]
    db.add_all(users)
    db.commit()

    user_map = {user.username: user.id for user in db.scalars(select(User)).all()}
    db.add_all(
        [
            Report(title="Public summary", content="team-a public report", status="published", scope_id="team-a", owner_id=user_map["alice"]),
            Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=user_map["bob"]),
            Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=user_map["carol"]),
            Report(title="Admin review", content="global review", status="published", scope_id="org-global", owner_id=user_map["admin"]),
        ]
    )
    db.commit()


@app.on_event("startup")
def startup() -> None:
    init_db()
    db = next(iter(__import__("app.database").database.SessionLocal().__iter__()))
    seed_demo_data(db)
    db.close()


@app.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> TokenResponse:
    if db.scalar(select(User).where(User.username == payload.username)) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is unavailable")

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="reader",
        scope_id=DEFAULT_SCOPE_ID,
        active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(user.username),
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        role=user.role,
        expires_in=8 * 60 * 60,
    )


@app.post("/auth/token", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or not user.active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenResponse(
        access_token=create_access_token(user.username),
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        role=user.role,
        expires_in=8 * 60 * 60,
    )


@app.get("/auth/me")
def me(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    return {"id": current_user.id, "username": current_user.username, "role": current_user.role, "scope_id": current_user.scope_id}


@app.get("/api/reports", response_model=list[ReportRead])
def list_reports(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ReportRead]:
    reports = db.scalars(select(Report).order_by(Report.id)).all()
    visible = [report for report in reports if can_read_report(current_user, report)]
    return [
        ReportRead(
            id=report.id,
            title=report.title,
            content=report.content,
            status=report.status,
            scope_id=report.scope_id,
            owner_id=report.owner_id,
        )
        for report in visible
    ]


@app.post("/api/reports", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_report(payload: ReportCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
    if not can_create_report(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not permitted")

    report = Report(
        title=payload.title,
        content=payload.content,
        status="draft",
        scope_id=current_user.scope_id,
        owner_id=current_user.id,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return ReportRead(
        id=report.id,
        title=report.title,
        content=report.content,
        status=report.status,
        scope_id=report.scope_id,
        owner_id=report.owner_id,
    )


@app.get("/api/reports/{report_id}", response_model=ReportRead)
def get_report(report_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
    report = db.get(Report, report_id)
    if report is None or not can_read_report(current_user, report):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return ReportRead(
        id=report.id,
        title=report.title,
        content=report.content,
        status=report.status,
        scope_id=report.scope_id,
        owner_id=report.owner_id,
    )


@app.patch("/api/reports/{report_id}", response_model=ReportRead)
def update_report(report_id: int, payload: ReportUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    if not can_edit_report(current_user, report):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    if payload.title is not None:
        report.title = payload.title
    if payload.content is not None:
        report.content = payload.content

    db.commit()
    db.refresh(report)
    return ReportRead(
        id=report.id,
        title=report.title,
        content=report.content,
        status=report.status,
        scope_id=report.scope_id,
        owner_id=report.owner_id,
    )


@app.post("/api/reports/{report_id}/publish", response_model=ReportRead)
def publish_report(report_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    if not can_publish_report(current_user, report):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    report.status = "published"
    db.commit()
    db.refresh(report)
    return ReportRead(
        id=report.id,
        title=report.title,
        content=report.content,
        status=report.status,
        scope_id=report.scope_id,
        owner_id=report.owner_id,
    )
