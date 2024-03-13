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


class PermissionMixin:
    def __init__(self) -> None:
        self._permissions: Set[Permission] = set()

    @property
    def permissions(self) -> Set[Permission]:
        """Returns this objects permissions"""
        return self._permissions

    @permissions.setter
    def permissions(self, perms_set: Set[Permission]):
        self._permissions = perms_set
