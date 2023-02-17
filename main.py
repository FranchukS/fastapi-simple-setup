import environs
import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models import User
from repository import UserRepo
from schemas import UserSchema, UserOutSchema, UserActivity

app = FastAPI()
env = environs.Env()
env.read_env(".env")

CONFIG = {
    "connections": {
    "default": env("DB_CONNECTION_URL")
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    }
}

def hash_password(password):
    return password


@app.post("/users/signup")
async def user_signup(user: UserSchema):
    await UserRepo.add(user.dict())
    return sign_jwt(user.email)


@app.post("/users/login")
async def user_login():
    pass


@app.get("/users/", response_model=list[UserOutSchema])
async def get_users():
    return await UserRepo.get_all()


@app.get("/users/{user_id}/activity", response_model=UserActivity)
async def last_activity(user_id: int):
    return await UserRepo.get(id=user_id)


@app.post("/post")
async def post_create(post: ):



@app.get("/post")
async def post_list():
    pass


@app.get("/post/{post_id}")
async def get_post(post_id: int):
    pass


@app.post("/post/{post_id}/like")
async def like_or_unlike_post(post_id: int):
    pass


@app.get("analytics")
async def get_like_analytics():
    pass


register_tortoise(
    app=app,
    config=CONFIG
)

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8000, log_level="info", reload=True)
