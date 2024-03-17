import strawberry

from src.auth.main import get_password_hash
from src.database import User as DbUser
from src.database import get_session
from src.gql.scalars.users import User
from src.models.users import User as UserModel


@strawberry.type
class UsersMutation:
    @strawberry.mutation
    async def add_user(self, username: str, email: str, password: str) -> User:
        user = DbUser(
            username=username, email=email, pwd_hash=get_password_hash(password)
        )
        async with get_session() as s:
            s.add(user)
            await s.commit()

        user_model = UserModel(id=user.id, username=user.username, email=user.email)
        return User.from_pydantic(user_model)
