from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=80)
    password: str = Field(..., min_length=8, max_length=255)
    role: str = Field(default="reader", pattern="^(reader|editor|administrator)$")
    scope_id: str = Field(default="team-a", min_length=1, max_length=80)


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=80)
    password: str = Field(..., min_length=1, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    role: str


class ReportCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    scope_id: str = Field(default="team-a", min_length=1, max_length=80)
    status: str = Field(default="draft", pattern="^(draft|published)$")


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    scope_id: Optional[str] = None


class ReportRead(BaseModel):
    id: int
    title: str
    content: str
    status: str
    scope_id: str
    owner_id: int
