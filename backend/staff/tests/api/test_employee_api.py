import pytest
from staff.models import Employee
from staff.factories import EmployeeFactory, GroupFactory, DepartmentFactory


@pytest.mark.django_db
@pytest.mark.api
def test_create_employee_success(api_client):
    """
    Test employee created succssfully.
    """
    group = GroupFactory()
    department = DepartmentFactory()
    response = api_client.post(
        "/employees/create",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "someone@somewhere.com",
            "department_id": department.id,
            "group_id": group.id,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.django_db
@pytest.mark.api
def test_create_employee_duplicate_email_raises(api_client):
    """
    Test employee creation with duplicate email raises error.
    """
    employee = EmployeeFactory()
    group = GroupFactory()
    department = DepartmentFactory()
    response = api_client.post(
        "/employees/create",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": employee.email,
            "department_id": department.id,
            "group_id": group.id,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Employee already exists"


@pytest.mark.django_db
@pytest.mark.api
def test_get_employee_success(api_client):
    """
    Test getting a employee is successful.
    """
    employee = EmployeeFactory()
    response = api_client.get(
        f"/employees/get/{employee.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["first_name"] == employee.first_name
    assert response.json()["last_name"] == employee.last_name
    assert response.json()["email"] == employee.email


@pytest.mark.django_db
@pytest.mark.api
def test_get_employee_not_found(api_client):
    """
    Test getting a employee that doesn't exist raises error.
    """
    response = api_client.get(
        "/employees/get/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_list_employees(api_client):
    """
    Test list of employees is retrieved and ordered.
    """
    EmployeeFactory(last_name="Adams")
    EmployeeFactory(last_name="Smith")
    EmployeeFactory(last_name="Cooke")

    response = api_client.get(
        "/employees/list", headers={"Authorization": "Bearer test-api-key"}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3
    assert data[0]["last_name"] == "Adams"
    assert data[1]["last_name"] == "Cooke"
    assert data[2]["last_name"] == "Smith"


@pytest.mark.django_db
@pytest.mark.api
def test_update_employee_success(api_client):
    """
    Test updating a employee is successful.
    """
    employee = EmployeeFactory()
    response = api_client.put(
        f"/employees/update/{employee.id}",
        json={
            "last_name": "Updated",
            "first_name": employee.first_name,
            "email": employee.email,
            "group_id": employee.group.id,
            "department_id": employee.department.id,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    employee.refresh_from_db()
    assert employee.last_name == "Updated"


@pytest.mark.django_db
@pytest.mark.api
def test_update_employee_duplicate(api_client):
    """
    Test updating a employee with a duplicate name raises error.
    """
    employee1 = EmployeeFactory()
    EmployeeFactory(email="someone@somewhere.com")

    response = api_client.put(
        f"/employees/update/{employee1.id}",
        json={
            "last_name": employee1.last_name,
            "first_name": employee1.first_name,
            "email": "someone@somewhere.com",
            "group_id": employee1.group.id,
            "department_id": employee1.department.id,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Employee not updated: employee email exists"
    )


@pytest.mark.django_db
@pytest.mark.api
def test_update_employee_not_found(api_client):
    """
    Test upraing a employee that doesn't exist raises error.
    """
    response = api_client.put(
        "/employees/update/999",
        json={
            "last_name": "Doe",
            "first_name": "John",
            "email": "someone@somewhere.com",
            "group_id": 1,
            "department_id": 1,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_delete_employee_success(api_client):
    """
    Test deleting a employee is successful.
    """
    employee = EmployeeFactory()
    response = api_client.delete(
        f"/employees/delete/{employee.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not Employee.objects.filter(id=employee.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_employee_not_found(api_client):
    """
    Test deleting a employee that doesn't exist raises error.
    """
    response = api_client.delete(
        "/employees/delete/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404
