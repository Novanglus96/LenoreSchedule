import pytest
from staff.models import Department
from staff.factories import DepartmentFactory


@pytest.mark.django_db
@pytest.mark.api
def test_create_department_success(api_client):
    """
    Test department created succssfully.
    """
    response = api_client.post(
        "/departments/create",
        json={"department_name": "New Department"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.django_db
@pytest.mark.api
def test_get_department_success(api_client):
    """
    Test getting a department is successful.
    """
    department = DepartmentFactory()
    response = api_client.get(
        f"/departments/get/{department.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["department_name"] == department.department_name


@pytest.mark.django_db
@pytest.mark.api
def test_get_department_not_found(api_client):
    """
    Test getting a department that doesn't exist raises error.
    """
    response = api_client.get(
        "/departments/get/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_list_departments(api_client):
    """
    Test list of departments is retrieved and ordered.
    """
    DepartmentFactory(department_name="B Department")
    DepartmentFactory(department_name="A Department")

    response = api_client.get(
        "/departments/list", headers={"Authorization": "Bearer test-api-key"}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["department_name"] == "A Department"
    assert data[1]["department_name"] == "B Department"


@pytest.mark.django_db
@pytest.mark.api
def test_update_department_success(api_client):
    """
    Test updating a department is successful.
    """
    department = DepartmentFactory()
    response = api_client.put(
        f"/departments/update/{department.id}",
        json={"department_name": "Updated Name"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    department.refresh_from_db()
    assert department.department_name == "Updated Name"


@pytest.mark.django_db
@pytest.mark.api
def test_update_department_duplicate(api_client):
    """
    Test updating a department with a duplicate name raises error.
    """
    department1 = DepartmentFactory(department_name="Department1")
    DepartmentFactory(department_name="Department2")

    response = api_client.put(
        f"/departments/update/{department1.id}",
        json={"department_name": "Department2"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Department not updated: department name exists"
    )


@pytest.mark.django_db
@pytest.mark.api
def test_update_department_not_found(api_client):
    """
    Test upraing a department that doesn't exist raises error.
    """
    response = api_client.put(
        "/departments/update/999",
        json={"department_name": "Department2"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_delete_department_success(api_client):
    """
    Test deleting a department is successful.
    """
    department = DepartmentFactory()
    response = api_client.delete(
        f"/departments/delete/{department.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not Department.objects.filter(id=department.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_department_not_found(api_client):
    """
    Test deleting a department that doesn't exist raises error.
    """
    response = api_client.delete(
        "/departments/delete/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404
