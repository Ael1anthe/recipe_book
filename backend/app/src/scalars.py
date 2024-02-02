from typing import Optional
import strawberry


@strawberry.type
class User:
    id: int
    name: Optional[str] = ""


@strawberry.type
class AddUser:
    id: int
    name: Optional[str] = ""
