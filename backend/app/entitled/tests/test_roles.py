from entitled import permissions, roles


class TestRoles:
    def test_create(self):
        role1 = roles.Role("admin")
        assert role1 == roles.Role("admin")
        assert role1 == "admin"
        assert role1.permissions == set()

    def test_add_perm(self):
        role1 = roles.Role("admin")

        role1.permissions.add(permissions.Permission("post:view"))
        assert role1.permissions == set([permissions.Permission("post:view")])
