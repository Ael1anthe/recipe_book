from src.auth import permissions as perms


class Role:
    """Base Role class"""

    __match_args__ = "name"

    def __init__(self, name: str) -> None:
        self.name = name
        self.permissions: list[perms.Permission] = []

    def __eq__(self, obj: object) -> bool:
        match obj:
            case str():
                return obj == self.name
            case Role():
                return obj.name == self.name
            case _:
                return False


class AuthorisationMixin:
    def __init__(self) -> None:
        self.roles: list[Role] = []
        self.permissions: list[perms.Permission] = []

    def has_permission(self, perm: str | perms.Permission):
        return perm in self.permissions or any(
            perm in role.permissions for role in self.roles
        )


test = AuthorisationMixin()
# class UserRoles:
#     """User roles manager"""
#     _roles: list[Role] = []

#     def __contains__(self, role: str) -> bool:
#         return Role(role) in self._roles

#     def __iter__(self) -> typing.Generator[Role, None, None]:
#         for role in self._roles:
#             yield role

#     def set(self, roles: list[Role]) -> None:
#         """Sets the user's roles"""
#         self._roles = roles

#     def add(self, role: Role) -> None:
#         """Adds a role to the user"""
#         self._roles.append(role)

#     def remove(self, role: Role) -> None:
#         """Removes a role to the user"""
#         self._roles.remove(role)

#     def clear(self) -> None:
#         """Clears the user's roles"""
#         self.set([])
