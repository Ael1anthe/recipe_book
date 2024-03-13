import strawberry

from src.gql.mutations.auth import AuthMutation
from src.gql.mutations.users import UsersMutation


@strawberry.type
class Mutation:
    @strawberry.field
    def user(self) -> UsersMutation:
        return UsersMutation()

    @strawberry.field
    def auth(self) -> AuthMutation:
        return AuthMutation()
