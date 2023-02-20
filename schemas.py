from datetime import date, datetime

from pydantic import EmailStr, BaseModel


class UserSchema(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOutSchema(BaseModel):
    id: int
    nickname: str
    email: str


class UserActivity(BaseModel):
    nickname: str
    email: str
    last_login: datetime
    last_activity: datetime


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(BaseModel):
    id: int
    created_at: date
    title: str
    content: str
    owner_id: int
