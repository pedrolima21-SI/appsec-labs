from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config
from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.config import DEFAULT_SCOPE_ID
from app.database import SessionLocal, get_db, init_db
from app.models import Report, User
from app.schemas import ReportRead, ReportUpdate, TokenResponse, UserLogin, UserRegister


def create_app(*, initialize_database: bool = True) -> FastAPI:
    if not config.VULNERABLE_MODE:
        raise RuntimeError("Vulnerable API disabled. Set VULNERABLE_MODE=true for this local lab.")

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        if initialize_database:
            init_db()
            with SessionLocal() as db:
                _seed_demo_data(db)
        yield

    application = FastAPI(title="AppSec Labs - Intentionally Vulnerable Reporting API", version="1.0.0", lifespan=lifespan)

    @application.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
    def register(payload: UserRegister, db: Session = Depends(get_db)) -> TokenResponse:
        if db.scalar(select(User.id).where(User.username == payload.username)) is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is unavailable")
        user = User(username=payload.username, password_hash=hash_password(payload.password), role="reader", scope_id=DEFAULT_SCOPE_ID)
        db.add(user)
        db.commit()
        db.refresh(user)
        return TokenResponse(access_token=create_access_token(user.username), user_id=user.id, username=user.username, role=user.role)

    @application.post("/auth/token", response_model=TokenResponse)
    def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
        user = db.scalar(select(User).where(User.username == payload.username))
        if user is None or not user.active or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return TokenResponse(access_token=create_access_token(user.username), user_id=user.id, username=user.username, role=user.role)

    @application.get("/api/reports/{report_id}", response_model=ReportRead)
    def read_report(report_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
        # Intentionally omits ownership and scope authorization to demonstrate BOLA/IDOR.
        report = db.get(Report, report_id)
        if report is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        return ReportRead.model_validate(report, from_attributes=True)

    @application.patch("/api/reports/{report_id}", response_model=ReportRead)
    def update_report(report_id: int, payload: ReportUpdate, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReportRead:
        # Intentionally omits ownership and scope authorization to demonstrate BOLA/IDOR.
        report = db.get(Report, report_id)
        if report is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        if payload.title is not None:
            report.title = payload.title
        if payload.content is not None:
            report.content = payload.content
        db.commit()
        db.refresh(report)
        return ReportRead.model_validate(report, from_attributes=True)

    return application


def _seed_demo_data(db: Session) -> None:
    if db.scalar(select(User.id).limit(1)) is not None:
        return
    users = [
        User(username="alice", password_hash=hash_password("alice12345"), role="reader", scope_id="team-a"),
        User(username="bob", password_hash=hash_password("bob12345"), role="editor", scope_id="team-a"),
        User(username="carol", password_hash=hash_password("carol12345"), role="editor", scope_id="team-b"),
        User(username="admin", password_hash=hash_password("admin12345"), role="administrator", scope_id="org-global"),
    ]
    db.add_all(users)
    db.flush()
    ids = {user.username: user.id for user in users}
    db.add_all([
        Report(title="Public summary", content="team-a public report", status="published", scope_id="team-a", owner_id=ids["alice"]),
        Report(title="Bob draft", content="draft by bob", status="draft", scope_id="team-a", owner_id=ids["bob"]),
        Report(title="Carol draft", content="draft by carol", status="draft", scope_id="team-b", owner_id=ids["carol"]),
    ])
    db.commit()


app = create_app()
