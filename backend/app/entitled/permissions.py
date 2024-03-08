from typing import Set


class Permission:
    """Base permission class"""

    __match_args__ = "name"

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, obj: object) -> bool:
        match obj:
            case str():
                return obj == self.name
            case Permission():
                return obj.name == self.name
            case _:
                return False

    def __repr__(self) -> str:
        return f"Permission({self.name})"

    def __hash__(self) -> int:
        return hash(repr(self))


class PermissionSet(Set[Permission]):
    def __contains__(self, __o: object) -> bool:
        match __o:
            case str():
                return super().__contains__(Permission(__o))
            case Permission():
                return super().__contains__(__o)
            case _:
                return False
