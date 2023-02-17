from datetime import date

from pydantic import BaseModel, EmailStr

from models import User


class UserSchema(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class UserOutSchema(BaseModel):
    id: int
    nickname: str
    email: str


class UserActivity(BaseModel):
    nickname: str
    email: str
    last_login: date
    last_activity: date


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(BaseModel):
    title: str
    content: str
    user: User
c