from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Optional
from sqlalchemy import Table, Column, ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncAttrs, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from src.auth.models import DBUser

from src.config import SETTINGS

if SETTINGS.DATABASE_URL:
    engine = create_async_engine(SETTINGS.DATABASE_URL.unicode_string(), echo=True)

    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    @asynccontextmanager
    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session() as session:
            async with session.begin():
                try:
                    yield session
                finally:
                    await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    pass


users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    pwd_hash: Mapped[str]
    groups: Mapped[list["Group"]] = relationship(secondary=users_groups)

    def to_dict(self):
        return self.__dict__


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    members: Mapped[list["User"]] = relationship(secondary=users_groups)

async def get_user(username: str) -> Optional[DBUser]:
    async with get_session() as s:
        sql = select(User).where(User.username == username)
        user = (await s.execute(sql)).scalars().unique().first()
    if user:
        return DBUser(**user.to_dict())
    return None
