import datetime

from tortoise import fields, Model


class BaseBlogModel(Model):
    """Base model for with standard field in models"""
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseBlogModel):
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    owner = fields.ForeignKeyField(
        "models.User",
        related_name="posts",
        on_delete=fields.CASCADE
    )
    liked_by = fields.ManyToManyField(
        "models.User",
        through="Like",
        related_name="liked_posts",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("created_at",)


class Like(BaseBlogModel):
    post = fields.ForeignKeyField("models.Post", related_name="likes", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField(
        "models.User", related_name="likes", on_delete=fields.CASCADE,
    )
    date = fields.DateField(default=datetime.date.today())


class User(BaseBlogModel):
    nickname = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    hash_password = fields.CharField(max_length=255)
    last_login = fields.DatetimeField(auto_now_add=True)
    last_activity = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user"
