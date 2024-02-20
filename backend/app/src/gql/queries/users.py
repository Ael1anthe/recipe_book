from typing import List

import strawberry

from src.gql.resolvers import users as users_resolver
from src.gql.scalars.users import User


@strawberry.type
class UsersQuery:
    users: List[User] = strawberry.field(resolver=users_resolver.get_users)
    # user: Optional[User] = strawberry.field(resolver=users_resolver.get_user)
