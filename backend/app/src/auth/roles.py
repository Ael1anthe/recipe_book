class Role:
    """Base Role class"""

    def __init__(self, label: str) -> None:
        self.label = label


class UserRoles:
    """User roles manager"""

    def __init__(self) -> None:
        self.__roles: list[Role] = []

    def set(self, roles: list[Role]) -> None:
        """Sets the user's roles"""
        self.__roles = roles

    def add(self, role: Role) -> None:
        """Adds a role to the user"""
        self.__roles.append(role)

    def remove(self, role: Role) -> None:
        """Removes a role to the user"""
        self.__roles.remove(role)

    def clear(self) -> None:
        """Clears the user's roles"""
        self.set([])


class AuthorisationMixin:
    def __init__(self) -> None:
        self.__roles = UserRoles()

    @property
    def roles(self) -> UserRoles:
        """This user's roles"""
        return self.__roles
