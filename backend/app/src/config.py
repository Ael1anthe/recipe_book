from typing import Any, Optional

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "host"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "master"
    DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_uri(cls, v: Optional[str], values: FieldValidationInfo) -> Any:
        match v:
            case str(v):
                return v
            case None:
                data = values.data
                return (
                    f"postgresql+asyncpg://{data['POSTGRES_USER']}:{data['POSTGRES_PASSWORD']}"
                    + f"@{data['POSTGRES_SERVER']}:{data['POSTGRES_PORT']}/{data['POSTGRES_DB']}"
                )


SETTINGS = Settings()
