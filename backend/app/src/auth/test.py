from src.auth import roles, permissions, policies


class User(roles.AuthorisationMixin):
    def __init__(self, login: str, email: str) -> None:
        super().__init__()
        self.login = login
        self.email = email


class Post:
    def __init__(self, title: str, owner: User) -> None:
        self.title: str = title
        self.owner: User = owner
        self.shared_users : list[User] = []
        


class PostPolicy(policies.BasePolicy):
    @classmethod
    @policies.BasePolicy.rule
    def edit(cls, post: Post, user: User) -> bool:
        return post.owner == user or user.has_permission("post:edit")

    @classmethod
    @policies.BasePolicy.rule
    def view(cls, post: Post, user: User) -> bool:
        return user.has_permission("post:view") or (
            "guest" in user.roles and user in post.shared_users
        )


def start_test() -> None:
    edit_post = permissions.Permission("post:edit")
    view_post = permissions.Permission("post:view")

    guest_role = roles.Role("guest")
    admin_role = roles.Role("admin")

    admin_role.permissions.append(edit_post)
    admin_role.permissions.append(view_post)

    editor = User(login="mathias", email="m.bigaignon@xefi.fr")
    guest = User(login="gautier", email="g.deleglise@xefi.fr")

    editor.roles.append(admin_role)
    guest.roles.append(guest_role)

    post = Post(title="New Post", owner=editor)

    print(editor.roles)
    print(guest.roles)
    print(PostPolicy.authorize("view", post, editor))
    print(PostPolicy.authorize("edit", post, editor))
    print(PostPolicy.authorize("view", post, guest))
    print(PostPolicy.authorize("edit", post, guest))
