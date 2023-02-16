import environs
import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models import User, UserIn, UserOut

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

@app.post("/")
async def root(user: UserIn):
    await User.create(**user.dict())
    return {"Success"}


@app.get("/{user_id}")
async def root(user_id: int):
    new = await User.get(id=user_id)
    return {"Success"}


register_tortoise(
    app=app,
    config=CONFIG
)

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8000, log_level="info", reload=True)
