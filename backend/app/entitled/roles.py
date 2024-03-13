from typing import Set

from entitled import permissions as perms


class Role(perms.PermissionMixin):
    """Base Role class"""

    __match_args__ = "name"

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

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


class AuthMixin(perms.PermissionMixin):
    def __init__(self) -> None:
        super().__init__()
        self.roles: Set[Role] = set[Role]()

    def has_perm(self, permission: str | perms.Permission) -> bool:
        """Return the user's permissions"""
        match permission:
            case str():
                _permission = perms.Permission(permission)
            case perms.Permission():
                _permission = permission
            case _:
                return False

        return _permission in self.permissions or any(
            _permission in role.permissions for role in self.roles
        )
