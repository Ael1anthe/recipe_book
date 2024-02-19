from typing import List, Optional
import strawberry

from src.gql.scalars.users import User
from src.gql.resolvers import users as users_resolver

@strawberry.type
class UsersQuery:
    users: List[User] = strawberry.field(resolver=users_resolver.get_users)
    # user: Optional[User] = strawberry.field(resolver=users_resolver.get_user)
