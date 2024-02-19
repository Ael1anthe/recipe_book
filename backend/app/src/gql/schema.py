import strawberry
from src.gql.mutations.main import Mutation
from src.gql.queries.main import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
