import pytest
from rest_framework import status
from rest_framework.test import APIClient

from server.apps.departments.models import Department


@pytest.mark.django_db
class TestDepartmentAPI:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def department(self):
        return Department.objects.create(name="IT")

    # CREATE endpoint
    def test_create_department(self, client):
        data = {"name": "Backend Team"}
        response = client.post("/api/v1/departments/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Backend Team"

    def test_create_department_with_parent(self, client, department):
        data = {"name": "Backend", "parent_id": department.id}
        response = client.post("/api/v1/departments/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["parent_id"] == str(department.id)

    # RETRIEVE endpoint
    def test_get_department_detail(self, client, department):
        response = client.get(f"/api/v1/departments/{department.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["department"]["id"] == department.id
        assert "employees" in response.data
        assert "children" in response.data

    def test_get_department_with_depth(self, client, department):
        response = client.get(f"/api/v1/departments/{department.id}/?depth=2")

        assert response.status_code == status.HTTP_200_OK

    # UPDATE endpoint
    def test_patch_department_name(self, client, department):
        data = {"name": "New Department Name"}
        response = client.patch(f"/api/v1/departments/{department.id}/", data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["department"]["name"] == "New Department Name"

    def test_patch_change_parent(self, client, department):
        parent = Department.objects.create(name="Main Office")
        data = {"parent_id": parent.id}

        response = client.patch(f"/api/v1/departments/{department.id}/", data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["department"]["parent"] == parent.id

    # DELETE endpoint
    def test_delete_department_cascade(self, client, department):
        response = client.delete(f"/api/v1/departments/{department.id}/?mode=cascade")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Department.objects.filter(id=department.id).exists()

    # CREATE Employee endpoint
    def test_add_employee_to_department(self, client, department):
        data = {
            "full_name": "Иван Иванов",
            "position": "Senior Developer",
            "hired_at": "2025-01-15"
        }
        response = client.post(f"/api/v1/departments/{department.id}/employees/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["full_name"] == "Иван Иванов"