from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.auth.main import get_current_user
from src.database import User, get_session
from src.models import users

CurrentUser = Annotated[users.User, Depends(get_current_user)]

router = APIRouter(prefix="/users")


@router.get("/")
async def read_users(current_user: CurrentUser) -> List[users.User]:
    async with get_session() as s:
        sql = select(User).order_by(User.username)
        db_users = (await s.execute(sql)).scalars().unique().all()
    users_list = [users.User(**user.__dict__) for user in db_users]
    return users_list


@router.post("/")
async def create_user(current_user: CurrentUser, data: users.NewUserData):
    pass


@router.get("/{id}")
async def read_user(current_user: CurrentUser, id: int) -> users.User:
    async with get_session() as s:
        sql = select(User).where(User.id == id)
        result = (await s.execute(sql)).scalars().unique().first()
    return users.User(**result.__dict__)


@router.put("/{id}")
async def update_user(current_user: CurrentUser, id: int) -> users.User:
    return current_user


@router.delete("/{id}")
async def delete_user(current_user: CurrentUser, id: int) -> users.User:
    return current_user


@router.get("/me/", response_model=users.User)
async def read_current_user(
    current_user: Annotated[users.User, Depends(get_current_user)]
):
    return current_user
