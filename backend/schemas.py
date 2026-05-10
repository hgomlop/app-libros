from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ── Books ─────────────────────────────────────────────────────────────────────

class BookCreate(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    cover_url: Optional[str] = None
    notes: Optional[str] = None
    rating: Optional[float] = None
    status: str = "reading"  # reading | finished | wishlist
    start_date: Optional[datetime] = None
    finish_date: Optional[datetime] = None
    year_read: Optional[int] = None
    is_recommended: bool = False


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    cover_url: Optional[str] = None
    notes: Optional[str] = None
    rating: Optional[float] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    finish_date: Optional[datetime] = None
    year_read: Optional[int] = None
    is_recommended: Optional[bool] = None


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str]
    cover_url: Optional[str]
    notes: Optional[str]
    rating: Optional[float]
    status: str
    start_date: Optional[datetime]
    finish_date: Optional[datetime]
    year_read: Optional[int]
    is_recommended: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
