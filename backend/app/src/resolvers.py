from typing import List

from sqlalchemy import select

from app import database
from app.scalars import User



async def get_users() -> List[User]:
    async with database.get_session() as s:
        sql = select(database.User).order_by(database.User.name)
        users = (await s.execute(sql)).scalars().unique().all()

    results = [User(**db_user) for db_user in users]
    return results
