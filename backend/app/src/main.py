from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException
from strawberry.fastapi import GraphQLRouter

from src.auth.main import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from src.auth.models import Token, User
from src.gql.schema import schema

graphql_app: GraphQLRouter = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
