from hashlib import sha256
from datetime import date

import uvicorn
from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise

import settings
from auth.auth_bearer import JWTBearer
from auth.auth_handler import sign_jwt
from repository import UserRepo, PostRepo, LikeRepo
from schemas import UserSchema, UserOutSchema, UserActivity, PostIn, UserLogin, PostOut

app = FastAPI()


def hash_(password):
    sha256().update(password.encode('utf-8'))
    hashed_password = sha256().digest().hex()
    return hashed_password


async def check_user(user: UserLogin):
    verify = await UserRepo.get_by_email(user.email)
    if verify and verify.hash_password == hash_(user.password):
        return True
    return False


def add_hash_password(user: UserSchema):
    payload = user.dict()
    payload["hash_password"] = hash_(payload["password"])
    return payload


@app.post("/users/signup", tags=["user"])
async def user_signup(user: UserSchema):
    await UserRepo.add(add_hash_password(user))
    return sign_jwt(user.email)


@app.post("/users/login", tags=["user"])
async def user_login(user: UserLogin):
    if await check_user(user):
        return sign_jwt(user.email)
    else:
        return {
            "error": "Invalid login details"
        }


@app.get("/users/", response_model=list[UserOutSchema], tags=["user"])
async def get_users():
    return await UserRepo.get_all()


@app.get("/users/{user_id}/activity", response_model=UserActivity, tags=["user"])
async def last_activity(user_id: int):
    return await UserRepo.get(id=user_id)


@app.post("/post", response_model=PostOut, dependencies=[Depends(JWTBearer())], tags=["post"])
async def post_create(post: PostIn):
    payload = post.dict()
    payload["owner_id"] = 1 # get user from jwt token
    return await PostRepo.add(payload)


@app.get("/post", response_model=list[PostOut], tags=["post"])
async def post_list():
    return await PostRepo.get_all()


@app.get("/post/{post_id}", response_model=PostOut, tags=["post"])
async def get_post(post_id: int):
    return await PostRepo.get(id=post_id)


@app.post("/post/{post_id}/like", dependencies=[Depends(JWTBearer())], tags=["post"])
async def like_or_unlike_post(post_id: int):
    post = await PostRepo.get(post_id)
    user = await UserRepo.get(id=1) # get user from jwt token

    if user in await PostRepo.get_liked_by(post):
        like = await LikeRepo.get_like(user_id=user.id, post_id=post.id)
        await LikeRepo.delete(like.id)
        return {"like deleted"}

    await LikeRepo.add_like(post=post, user=user)
    return {"like added"}


@app.get("/analytics")
async def get_like_analytics(
        start_date: date = date(2022, 1, 1),
        end_date: date = date.today()
):
    return await LikeRepo.likes_by_day(start_date=start_date, end_date=end_date)


register_tortoise(
    app=app,
    config=settings.CONFIG
)

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8000, log_level="info", reload=True)
