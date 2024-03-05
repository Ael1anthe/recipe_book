import typing
import strawberry

from src.gql.resolvers import users as users_resolver
from src.gql.scalars.users import User


@strawberry.type
class UsersQuery:
    all: typing.List[User] = strawberry.field(resolver=users_resolver.get_users)
