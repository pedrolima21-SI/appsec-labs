from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.config import VULNERABLE_MODE
from app.database import get_db, init_db
from app.models import Report, User
from app.schemas import ReportRead, ReportUpdate, TokenResponse, UserLogin, UserRegister

if not VULNERABLE_MODE:
    raise RuntimeError("Vulnerable API is disabled. Set VULNERABLE_MODE=true for a loopback-only local lab.")

app = FastAPI(title="AppSec Labs - Intentionally Vulnerable Reporting API", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> TokenResponse:
    if db.scalar(select(User).where(User.username == payload.username)) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is unavailable")
    user = User(username=payload.username, password_hash=hash_password(payload.password), role="reader", scope_id="team-a", active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(user.username), token_type="bearer", user_id=user.id, username=user.username, role=user.role, expires_in=8 * 60 * 60)


@app.post("/auth/token", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or not user.active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.username), token_type="bearer", user_id=user.id, username=user.username, role=user.role, expires_in=8 * 60 * 60)


@app.get("/api/reports/{report_id}", response_model=ReportRead)
def read_report(report_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return ReportRead(id=report.id, title=report.title, content=report.content, status=report.status, scope_id=report.scope_id, owner_id=report.owner_id)


@app.patch("/api/reports/{report_id}", response_model=ReportRead)
def update_report(report_id: int, payload: ReportUpdate, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    if payload.title is not None:
        report.title = payload.title
    if payload.content is not None:
        report.content = payload.content
    db.commit()
    db.refresh(report)
    return ReportRead(id=report.id, title=report.title, content=report.content, status=report.status, scope_id=report.scope_id, owner_id=report.owner_id)
