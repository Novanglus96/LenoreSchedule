import pytest
from planner.factories import ScheduleTemplateFactory
from planner.models import ScheduleTemplate
from staff.factories import EmployeeFactory, LocationFactory

AUTH = {"Authorization": "Bearer test-api-key"}
BASE = "/schedule_templates"


# ---------------------------------------------------------------------------
# POST /create
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_create_schedule_template_success(api_client):
    """Test that a schedule_template is created successfully."""
    employee = EmployeeFactory()

    response = api_client.post(
        f"{BASE}/create",
        json={
            "employee_id": employee.id,
            "day_of_week": 0,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
        },
        headers=AUTH,
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert ScheduleTemplate.objects.filter(employee_id=employee.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_create_schedule_template_with_location_success(api_client):
    """Test that a schedule_template is created with a location."""
    employee = EmployeeFactory()
    location = LocationFactory()

    response = api_client.post(
        f"{BASE}/create",
        json={
            "employee_id": employee.id,
            "day_of_week": 0,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "location_id": location.id,
        },
        headers=AUTH,
    )

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.api
def test_create_schedule_template_invalid_day_returns_400(api_client):
    """Test that an invalid day_of_week returns 400."""
    employee = EmployeeFactory()

    response = api_client.post(
        f"{BASE}/create",
        json={
            "employee_id": employee.id,
            "day_of_week": 7,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
        },
        headers=AUTH,
    )

    assert response.status_code == 400
    assert "day_of_week" in response.json()["detail"]


@pytest.mark.django_db
@pytest.mark.api
def test_create_schedule_template_invalid_time_range_returns_400(api_client):
    """Test that start_time after end_time returns 400."""
    employee = EmployeeFactory()

    response = api_client.post(
        f"{BASE}/create",
        json={
            "employee_id": employee.id,
            "day_of_week": 0,
            "start_time": "17:00:00",
            "end_time": "09:00:00",
        },
        headers=AUTH,
    )

    assert response.status_code == 400
    assert "time range" in response.json()["detail"]


# ---------------------------------------------------------------------------
# PUT /update/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_update_schedule_template_success(api_client):
    """Test that a schedule_template is updated successfully."""
    existing = ScheduleTemplateFactory(day_of_week=0)

    response = api_client.put(
        f"{BASE}/update/{existing.id}",
        json={
            "employee_id": existing.employee.id,
            "day_of_week": 2,
            "start_time": "10:00:00",
            "end_time": "18:00:00",
        },
        headers=AUTH,
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}


@pytest.mark.django_db
@pytest.mark.api
def test_update_schedule_template_not_found_returns_404(api_client):
    """Test that updating a non-existent schedule_template returns 404."""
    employee = EmployeeFactory()

    response = api_client.put(
        f"{BASE}/update/99999",
        json={
            "employee_id": employee.id,
            "day_of_week": 0,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
        },
        headers=AUTH,
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /get/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_get_schedule_template_success(api_client):
    """Test that a schedule_template is retrieved successfully."""
    existing = ScheduleTemplateFactory(day_of_week=0)

    response = api_client.get(f"{BASE}/get/{existing.id}", headers=AUTH)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == existing.id
    assert data["day_of_week"] == 0
    assert "employee" in data
    assert "start_time" in data
    assert "end_time" in data


@pytest.mark.django_db
@pytest.mark.api
def test_get_schedule_template_not_found_returns_404(api_client):
    """Test that getting a non-existent schedule_template returns 404."""
    response = api_client.get(f"{BASE}/get/99999", headers=AUTH)

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /employee/{employee_id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_list_schedule_templates_for_employee_success(api_client):
    """Test that all schedule_templates for an employee are returned."""
    employee = EmployeeFactory()
    ScheduleTemplateFactory(employee=employee, day_of_week=0)
    ScheduleTemplateFactory(employee=employee, day_of_week=1)

    response = api_client.get(f"{BASE}/employee/{employee.id}", headers=AUTH)

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
@pytest.mark.api
def test_list_schedule_templates_for_employee_empty(api_client):
    """Test that an empty list is returned when no templates exist for the employee."""
    employee = EmployeeFactory()

    response = api_client.get(f"{BASE}/employee/{employee.id}", headers=AUTH)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
@pytest.mark.api
def test_list_schedule_templates_excludes_other_employees(api_client):
    """Test that only templates belonging to the specified employee are returned."""
    employee = EmployeeFactory()
    other_employee = EmployeeFactory()
    ScheduleTemplateFactory(employee=employee, day_of_week=0)
    ScheduleTemplateFactory(employee=other_employee, day_of_week=0)

    response = api_client.get(f"{BASE}/employee/{employee.id}", headers=AUTH)

    assert len(response.json()) == 1
    assert response.json()[0]["employee"]["id"] == employee.id


# ---------------------------------------------------------------------------
# DELETE /delete/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_delete_schedule_template_success(api_client):
    """Test that a schedule_template is deleted successfully."""
    existing = ScheduleTemplateFactory()

    response = api_client.delete(f"{BASE}/delete/{existing.id}", headers=AUTH)

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert not ScheduleTemplate.objects.filter(id=existing.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_schedule_template_not_found_returns_404(api_client):
    """Test that deleting a non-existent schedule_template returns 404."""
    response = api_client.delete(f"{BASE}/delete/99999", headers=AUTH)

    assert response.status_code == 404
