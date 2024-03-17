from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr


class NewUserData(BaseModel):
    username: str
    email: EmailStr
    password: str


class DBUser(User):
    pwd_hash: str
