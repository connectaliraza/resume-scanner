from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    RECRUITER = "recruiter"
    ADMIN = "admin"
    CANDIDATE = "candidate"


class User(BaseModel):
    id: int
    email: EmailStr
    role: Role


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Role


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
