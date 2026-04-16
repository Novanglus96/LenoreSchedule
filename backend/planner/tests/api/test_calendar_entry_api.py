import pytest
from datetime import date
from planner.factories import CalendarEntryFactory
from planner.models import CalendarEntry
from staff.factories import EmployeeFactory, LocationFactory

AUTH = {"Authorization": "Bearer test-api-key"}
BASE = "/calendar"


# ---------------------------------------------------------------------------
# POST /create_entry
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_create_calendar_entry_scheduled_success(api_client):
    """Test that a scheduled calendar entry is created successfully."""
    employee = EmployeeFactory()
    location = LocationFactory()

    response = api_client.post(
        f"{BASE}/create_entry",
        json={
            "employee_id": employee.id,
            "calendar_date": "2025-01-06",
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "confirmed": False,
            "entry_type": "scheduled",
            "location_id": location.id,
        },
        headers=AUTH,
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert CalendarEntry.objects.filter(
        employee_id=employee.id, calendar_date=date(2025, 1, 6)
    ).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_create_calendar_entry_full_day_vacation_success(api_client):
    """Test that a full-day vacation entry (null times) is created successfully."""
    employee = EmployeeFactory()

    response = api_client.post(
        f"{BASE}/create_entry",
        json={
            "employee_id": employee.id,
            "calendar_date": "2025-01-06",
            "confirmed": False,
            "entry_type": "vacation",
        },
        headers=AUTH,
    )

    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.django_db
@pytest.mark.api
def test_create_calendar_entry_with_notes_success(api_client):
    """Test that a calendar entry with notes is created successfully."""
    employee = EmployeeFactory()

    response = api_client.post(
        f"{BASE}/create_entry",
        json={
            "employee_id": employee.id,
            "calendar_date": "2025-01-06",
            "confirmed": False,
            "entry_type": "sick",
            "notes": "Flu symptoms.",
        },
        headers=AUTH,
    )

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.api
def test_create_calendar_entry_duplicate_returns_400(api_client):
    """Test that creating a duplicate calendar entry returns 400."""
    existing = CalendarEntryFactory(entry_type="scheduled")

    response = api_client.post(
        f"{BASE}/create_entry",
        json={
            "employee_id": existing.employee.id,
            "calendar_date": str(existing.calendar_date),
            "start_time": str(existing.start_time),
            "end_time": str(existing.end_time),
            "confirmed": existing.confirmed,
            "entry_type": existing.entry_type,
            "location_id": existing.location.id if existing.location else None,
        },
        headers=AUTH,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "CalendarEntry already exists"


# ---------------------------------------------------------------------------
# PUT /update_entry/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_update_calendar_entry_success(api_client):
    """Test that a calendar entry is updated successfully."""
    existing = CalendarEntryFactory(entry_type="scheduled")

    response = api_client.put(
        f"{BASE}/update_entry/{existing.id}",
        json={
            "employee_id": existing.employee.id,
            "calendar_date": str(existing.calendar_date),
            "start_time": "10:00:00",
            "end_time": "18:00:00",
            "confirmed": True,
            "entry_type": "overtime",
            "notes": "Covering for colleague.",
        },
        headers=AUTH,
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}


@pytest.mark.django_db
@pytest.mark.api
def test_update_calendar_entry_not_found_returns_404(api_client):
    """Test that updating a non-existent calendar entry returns 404."""
    employee = EmployeeFactory()

    response = api_client.put(
        f"{BASE}/update_entry/99999",
        json={
            "employee_id": employee.id,
            "calendar_date": "2025-01-06",
            "confirmed": False,
            "entry_type": "scheduled",
        },
        headers=AUTH,
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /view/{timeframe}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_list_calendar_entries_current_year(api_client, today_date):
    """Test that calendar entries for the current year are returned."""
    employee = EmployeeFactory()
    CalendarEntryFactory(employee=employee, calendar_date=today_date)

    response = api_client.get(f"{BASE}/view/current", headers=AUTH)

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "entry_type" in data[0]
    assert "notes" in data[0]


@pytest.mark.django_db
@pytest.mark.api
def test_list_calendar_entries_includes_entry_type_and_notes(api_client, today_date):
    """Test that the list response includes entry_type and notes fields."""
    CalendarEntryFactory(
        calendar_date=today_date,
        entry_type="vacation",
        notes="Annual leave.",
        start_time=None,
        end_time=None,
        location=None,
    )

    response = api_client.get(f"{BASE}/view/current", headers=AUTH)

    assert response.status_code == 200
    vacation_entries = [e for e in response.json() if e["entry_type"] == "vacation"]
    assert len(vacation_entries) == 1
    assert vacation_entries[0]["notes"] == "Annual leave."
    assert vacation_entries[0]["start_time"] is None


# ---------------------------------------------------------------------------
# DELETE /delete_entry/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_delete_calendar_entry_success(api_client):
    """Test that a calendar entry is deleted successfully."""
    existing = CalendarEntryFactory()

    response = api_client.delete(
        f"{BASE}/delete_entry/{existing.id}", headers=AUTH
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert not CalendarEntry.objects.filter(id=existing.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_calendar_entry_not_found_returns_404(api_client):
    """Test that deleting a non-existent calendar entry returns 404."""
    response = api_client.delete(
        f"{BASE}/delete_entry/99999", headers=AUTH
    )

    assert response.status_code == 404
