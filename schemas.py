from datetime import date

from pydantic import EmailStr, BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from models import Post


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


class UserLike(BaseModel):
    nickname: str


class UserActivity(BaseModel):
    nickname: str
    email: str
    last_login: date
    last_activity: date


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(BaseModel):
    id: int
    created_at: date
    title: str
    content: str
    owner_id: int
