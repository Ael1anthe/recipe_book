from typing import Set

from entitled import permissions as perms


class Role:
    """Base Role class"""

    __match_args__ = "name"

    def __init__(self, name: str) -> None:
        self.name = name
        self.permissions: Set[perms.Permission] = set()

    def __eq__(self, obj: object) -> bool:
        match obj:
            case str():
                return obj == self.name
            case Role():
                return obj.name == self.name
            case _:
                return False

    def __repr__(self) -> str:
        return f"Role({self.name})"

    def __hash__(self) -> int:
        return hash(repr(self))


class RoleSet(Set[Role]):
    def __contains__(self, __o: object) -> bool:
        match __o:
            case str():
                return super().__contains__(perms.Permission(__o))
            case Role():
                return super().__contains__(__o)
            case _:
                return False
