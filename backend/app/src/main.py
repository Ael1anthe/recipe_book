from fastapi import FastAPI

from src.routers import auth, graphql, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(graphql.router, prefix="/graphql")
