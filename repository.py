from tortoise import Model

from models import UserModel, BaseBlogModel, Post, Like


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
    model = UserModel

    @classmethod
    async def get_by_email(cls, email: str) -> Model | None:
        return await cls.model.get_or_none(email=email)


class PostRepo(BaseRepo):
    model = Post
    @classmethod
    async def get_liked_by(cls, post: Post) -> Model | None:
        return await post.liked_by.all()


class LikeRepo(BaseRepo):
    model = Like

    @classmethod
    async def get_like(cls, post_id: int, user_id: int) -> Model | None:
        return await cls.model.get_or_none(id=id)

    @classmethod
    async def add_like(cls, user: UserModel, post: Post) -> Model:
        return await cls.model.create(user=user, post=post)
