import strawberry


from src.gql.scalars.users import User
from src.database import User as DbUser, get_session
from src.models import User as UserModel


@strawberry.type
class UsersMutation:
    @strawberry.mutation
    async def add_user(self, name: str, id: int) -> User:
        user = DbUser(name=name, id=id)
        async with get_session() as s:
            s.add(user)
            await s.commit()

        user_model = UserModel(id=user.id, name=user.name, email="a@test.fr")
        return User.from_pydantic(user_model)
