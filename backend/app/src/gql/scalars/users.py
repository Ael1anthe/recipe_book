import strawberry

from src.models import users


@strawberry.experimental.pydantic.type(model=users.User)
class User:
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto
