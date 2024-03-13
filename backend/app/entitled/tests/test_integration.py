from result import result

from entitled import permissions, policies, roles, rules
from entitled.rules import Rule


class User(roles.AuthMixin):
    def __init__(self, login: str, email: str) -> None:
        super().__init__()
        self.login = login
        self.email = email


class Post:
    def __init__(self, title: str, owner: User) -> None:
        self.title: str = title
        self.owner: User = owner
        self.shared_users: list[User] = []


def test() -> None:
    create_post = permissions.Permission("post:create")
    view_post = permissions.Permission("post:view")
    edit_post = permissions.Permission("post:edit")
    delete_post = permissions.Permission("post:delete")

    guest_role = roles.Role("guest")
    user_role = roles.Role("user")
    admin_role = roles.Role("admin")

    guest_role.permissions.add(view_post)
    user_role.permissions = set([create_post, view_post, edit_post, delete_post])
    admin_role.permissions = set([create_post, view_post, edit_post, delete_post])

    user1 = User(login="mathias", email="m.bigaignon@xefi.fr")
    user2 = User(login="gautier", email="g.deleglise@xefi.fr")
    user3 = User(login="alex", email="a.achard@xefi.fr")

    user1.roles.add(user_role)
    user2.roles.add(guest_role)
    user3.roles.add(admin_role)

    post = Post(title="New Post", owner=user1)

    def user_is_admin(user: User, *args):
        if roles.Role("admin") in user.roles:
            return True

    rules.Rule.set_precheck(user_is_admin)

    class PostPolicy(policies.Policy):
        @classmethod
        @policies.register("post:create")
        def create(cls, user: User) -> bool:
            return user.has_perm("post:create")

        @classmethod
        @policies.register("post:view")
        def view(cls, user: User, post: Post) -> bool:
            return user.has_perm("post:view") and (
                post.owner == user or user in post.shared_users
            )

        @classmethod
        @policies.register("post:edit")
        def edit(cls, user: User, post: Post) -> bool:
            return user.has_perm("post:edit") and post.owner == user

    assert PostPolicy.authorize("create", user1) == result.Ok(True)
    assert PostPolicy.authorize("view", user1, post) == result.Ok(True)
    assert PostPolicy.authorize("edit", user1, post) == result.Ok(True)

    assert PostPolicy.authorize("create", user2) == result.Ok(False)
    assert PostPolicy.authorize("view", user2, post) == result.Ok(False)
    post.shared_users.append(user2)
    assert PostPolicy.authorize("view", user2, post) == result.Ok(True)
    assert PostPolicy.authorize("edit", user2, post) == result.Ok(False)

    assert PostPolicy.authorize("create", user3) == result.Ok(True)
    assert PostPolicy.authorize("view", user3, post) == result.Ok(True)
    assert PostPolicy.authorize("edit", user3, post) == result.Ok(True)
