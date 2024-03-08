from typing import Protocol, Set

from entitled import permissions, roles


class Authorizable(Protocol):
    subject_permissions: Set[permissions.Permission]
    roles: Set[roles.Role]
