import strawberry

from src.gql.queries.users import UsersQuery


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> UsersQuery:
        return UsersQuery()
