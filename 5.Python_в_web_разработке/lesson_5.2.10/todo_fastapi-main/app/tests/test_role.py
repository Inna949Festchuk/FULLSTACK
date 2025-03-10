from .api_client import TodoApiClient


class TestRole:
    def test_get_roles(self, admin_client: TodoApiClient):
        response = admin_client.get_roles()
        assert response.page == 1
        assert response.total == 2
        assert len(response.roles) >= 2

    def test_get_role(self, admin_client: TodoApiClient):
        response = admin_client.get_roles(name="admin")
        role = response.roles[0]

        role = admin_client.get_role(role.id)
        assert role.name == role.name
        assert role.id == role.id
        assert role.rights == role.rights

    def test_create_role(self, admin_client: TodoApiClient):
        response = None
        try:
            response = admin_client.create_role("test_create_role")
            assert response.id
            assert response.name == "test_create_role"
        finally:
            if response:
                admin_client.delete_role(response.id)

    def test_update_role(self, admin_client: TodoApiClient):
        create_role_response = admin_client.create_role("test_update_role")
        update_role_response = admin_client.update_role(create_role_response.id, name="test_update_role_new_name")
        assert update_role_response.name == "test_update_role_new_name"

        role = admin_client.get_role(create_role_response.id)
        assert role.name == "test_update_role_new_name"

        right_1 = admin_client.create_right("token", True, False, False)
        right_2 = admin_client.create_right("token", False, True, False)

        admin_client.update_role(create_role_response.id, rights=[right_1.id, right_2.id])

        role = admin_client.get_role(role.id)

        assert len(role.rights) == 2
        assert {right_1.id, right_2.id} == {right.id for right in role.rights}
