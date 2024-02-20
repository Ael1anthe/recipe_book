import strawberry

from src.auth import models


@strawberry.experimental.pydantic.type(model=models.User)
class User:
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto
