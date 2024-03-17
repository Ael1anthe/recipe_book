import typing
from datetime import timedelta

from fastapi import APIRouter, param_functions, security, status
from starlette import exceptions

from src.auth import main
from src.models import tokens

router = APIRouter()


@router.post("/authenticate")
async def authenticate(
    form_data: typing.Annotated[
        security.OAuth2PasswordRequestForm, param_functions.Depends()
    ]
) -> tokens.Token:
    user = await main.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=main.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = main.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return tokens.Token(access_token=access_token, token_type="bearer")
