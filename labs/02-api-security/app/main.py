from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.database import init_db
from app.models import Report, User
from app.schemas import ReportCreate, ReportRead, ReportUpdate, TokenResponse, UserLogin, UserRegister

app = FastAPI(title="AppSec Labs - Secure Reporting API", version="0.1.0")

init_db()


def seed_demo_data(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    demo_users = [
        ("alice", "alice123", "reader", "team-a"),
        ("bob", "bob123", "editor", "team-a"),
        ("carol", "carol123", "editor", "team-b"),
        ("admin", "admin123", "administrator", "org-global"),
    ]

    for username, password, role, scope_id in demo_users:
        db.add(
            User(
                username=username,
                password_hash=hash_password(password),
                role=role,
                scope_id=scope_id,
            )
        )

    db.commit()

    alice = db.query(User).filter(User.username == "alice").one()
    bob = db.query(User).filter(User.username == "bob").one()
    carol = db.query(User).filter(User.username == "carol").one()
    admin = db.query(User).filter(User.username == "admin").one()

    reports = [
        Report(title="Public report", content="team-a public report", status="published", scope_id="team-a", owner_id=alice.id),
        Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=bob.id),
        Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=carol.id),
        Report(title="Admin review", content="admin only report", status="published", scope_id="org-global", owner_id=admin.id),
    ]
    db.add_all(reports)
    db.commit()


@app.on_event("startup")
def startup() -> None:
    db = next(iter([__import__("app.database").database.SessionLocal()]))
    seed_demo_data(db)
    db.close()


@app.post("/auth/register", response_model=TokenResponse)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> TokenResponse:
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role,
        scope_id=payload.scope_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"username": user.username, "role": user.role, "scope_id": user.scope_id})
    return TokenResponse(access_token=token, user_id=user.id, username=user.username, role=user.role)


@app.post("/auth/token", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"username": user.username, "role": user.role, "scope_id": user.scope_id})
    return TokenResponse(access_token=token, user_id=user.id, username=user.username, role=user.role)


@app.get("/auth/me")
def me(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "scope_id": current_user.scope_id,
    }


@app.get("/api/reports", response_model=list[ReportRead])
def list_reports(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ReportRead]:
    reports = db.query(Report).all()
    visible = [report for report in reports if report.owner_id == current_user.id or (report.status == "published" and report.scope_id == current_user.scope_id)]
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


@app.post("/api/reports", response_model=ReportRead)
def create_report(payload: ReportCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
    if current_user.role not in {"editor", "administrator"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    report = Report(
        title=payload.title,
        content=payload.content,
        status=payload.status,
        scope_id=payload.scope_id,
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
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    if report.owner_id != current_user.id and (report.status != "published" or report.scope_id != current_user.scope_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

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
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    if report.owner_id != current_user.id and current_user.role != "administrator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if payload.title is not None:
        report.title = payload.title
    if payload.content is not None:
        report.content = payload.content
    if payload.status is not None:
        report.status = payload.status
    if payload.scope_id is not None:
        if current_user.role != "administrator":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        report.scope_id = payload.scope_id

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
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    if current_user.role != "administrator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

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
