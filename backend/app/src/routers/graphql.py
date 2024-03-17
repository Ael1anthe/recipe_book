from strawberry.fastapi import GraphQLRouter

from src.gql.schema import schema

router: GraphQLRouter = GraphQLRouter(schema)
