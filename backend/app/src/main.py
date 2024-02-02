import asyncio
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.database import async_create
from app.schema import Query

asyncio.run(async_create())

schema = strawberry.Schema(query=Query)

graphql_app: GraphQLRouter = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

