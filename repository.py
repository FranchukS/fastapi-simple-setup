from tortoise import Model

from models import User, BaseBlogModel, Post, Like


class BaseRepo:
    model: BaseBlogModel

    @classmethod
    async def get(cls, id: int) -> Model | None:
        return await cls.model.get_or_none(id=id)

    @classmethod
    async def add(cls, payload: dict) -> Model:
        return await cls.model.create(**payload)

    @classmethod
    async def get_all(cls) -> list[Model]:
        return await cls.model.all()

    @classmethod
    async def update(cls, payload: dict) -> Model:
        return await cls.model.update_from_dict(payload)

    @classmethod
    async def delete(cls, id: int) -> None:
        obj = await cls.model.get_or_none(id=id)
        await obj.delete()


class UserRepo(BaseRepo):
    model = User


class PostRepo(BaseRepo):
    model = Post


class LikeRepo(BaseRepo):
    model = Like
