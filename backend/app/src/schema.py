import strawberry
from typing import List

from app.scalars import User
from app.resolvers import get_users

@strawberry.type
class Query:

    @strawberry.field
    async def users(self) -> List[User]:
        """Get all users"""
        users_data_list = await get_users()
        return users_data_list
    
