from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserRegister(StrictModel):
    username: str = Field(..., min_length=3, max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(..., min_length=12, max_length=128)


class UserLogin(StrictModel):
    username: str = Field(..., min_length=1, max_length=80)
    password: str = Field(..., min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int | None = None
    username: str | None = None
    role: str | None = None
    expires_in: int = 8 * 60 * 60


class ReportCreate(StrictModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=20000)


class ReportUpdate(StrictModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=20000)


class ReportRead(BaseModel):
    id: int
    title: str
    content: str
    status: str
    scope_id: str
    owner_id: int
