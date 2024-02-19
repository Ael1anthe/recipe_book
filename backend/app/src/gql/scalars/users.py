import strawberry

from src import models


@strawberry.experimental.pydantic.type(model=models.User)
class User:
    id: strawberry.auto
    name: strawberry.auto
