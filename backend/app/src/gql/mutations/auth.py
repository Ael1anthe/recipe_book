import strawberry
from fastapi import HTTPException

from src.auth.main import authenticate_user, create_access_token


@strawberry.type
class AuthResponse:
    access_token: str
    token_type: str


@strawberry.type
class AuthMutation:
    @strawberry.field
    async def login(self, username: str, password: str) -> AuthResponse:
        user = await authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Blabla")
        access_token = create_access_token(data={"sub": user.username})
        return AuthResponse(access_token=access_token, token_type="bearer")
