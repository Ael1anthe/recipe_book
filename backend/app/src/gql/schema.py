import strawberry

from src.gql.mutations.main import Mutation
from src.gql.queries.main import Query
from src.gql.subscriptions.subscriptions import Subscription

schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
