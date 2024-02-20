from typing import List

from sqlalchemy import select

from src.auth.models import User as UserModel
from src.database import User as DbUser
from src.database import get_session
from src.gql.scalars.users import User


async def get_users() -> List[User]:
    async with get_session() as s:
        sql = select(DbUser).order_by(DbUser.username)
        users = (await s.execute(sql)).scalars().unique().all()

    user_models = [UserModel(**user.__dict__) for user in users]
    return [User.from_pydantic(user) for user in user_models]


# def get_user(login: str) -> Optional[User]:
# user = user_repo.get_user(login)
# if user:
#     return User.from_pydantic(user)

# return None
