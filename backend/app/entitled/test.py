from typing import Set

from entitled import permissions, roles
from entitled.policies import Policy


class User:
    def __init__(self, login: str, email: str) -> None:
        self.login = login
        self.email = email
        self.subject_permissions: Set[permissions.Permission] = set()
        self.roles: Set[roles.Role] = set()


class Post:
    def __init__(self, title: str, owner: User) -> None:
        self.title: str = title
        self.owner: User = owner
        self.shared_users: list[User] = []


def start_test() -> None:
    edit_post = permissions.Permission("post:edit")
    view_post = permissions.Permission("post:view")

    guest_role = roles.Role("guest")
    admin_role = roles.Role("admin")

    user1 = User(login="mathias", email="m.bigaignon@xefi.fr")
    user2 = User(login="gautier", email="g.deleglise@xefi.fr")

    post = Post(title="New Post", owner=user2)

    admin_role.permissions.add(edit_post)
    admin_role.permissions.add(view_post)

    user1.roles.add(admin_role)
    user2.roles.add(guest_role)

    class PostPolicy(Policy):
        @classmethod
        @Policy.register
        def can_edit(cls, user, post) -> bool:
            return post.owner == user or "admin" in user.roles

    class UserPolicy(Policy):
        @classmethod
        @Policy.register
        def can_see(cls) -> bool:
            return True

    print(UserPolicy.authorize("can_see", user1, post))
    print(PostPolicy.authorize("can_edit"))
