import pytest
from datetime import date, time
from planner.models import CalendarEntry
from staff.factories import EmployeeFactory, LocationFactory


@pytest.mark.django_db
@pytest.mark.unit
def test_calendar_entry_creation_with_times():
    """Test CalendarEntry is created successfully with start/end times."""
    employee = EmployeeFactory()
    location = LocationFactory()
    entry = CalendarEntry.objects.create(
        employee=employee,
        calendar_date=date(2025, 1, 6),
        start_time=time(9, 0),
        end_time=time(17, 0),
        location=location,
        entry_type="scheduled",
    )

    assert entry.id is not None
    assert entry.entry_type == "scheduled"
    assert entry.notes is None
    assert entry.location == location


@pytest.mark.django_db
@pytest.mark.unit
def test_calendar_entry_creation_full_day_absence():
    """Test CalendarEntry is created successfully as a full-day absence (null times)."""
    employee = EmployeeFactory()
    entry = CalendarEntry.objects.create(
        employee=employee,
        calendar_date=date(2025, 1, 6),
        entry_type="vacation",
    )

    assert entry.start_time is None
    assert entry.end_time is None
    assert entry.location is None


@pytest.mark.django_db
@pytest.mark.unit
def test_calendar_entry_notes_stored():
    """Test that notes are stored correctly."""
    employee = EmployeeFactory()
    entry = CalendarEntry.objects.create(
        employee=employee,
        calendar_date=date(2025, 1, 6),
        entry_type="sick",
        notes="Doctor appointment in the morning.",
    )

    assert entry.notes == "Doctor appointment in the morning."


@pytest.mark.django_db
@pytest.mark.unit
def test_calendar_entry_multiple_blocks_same_day():
    """Test that multiple CalendarEntry blocks on the same day are allowed."""
    employee = EmployeeFactory()
    location = LocationFactory()
    CalendarEntry.objects.create(
        employee=employee,
        calendar_date=date(2025, 1, 6),
        start_time=time(10, 0),
        end_time=time(14, 0),
        entry_type="scheduled",
        location=location,
    )
    second = CalendarEntry.objects.create(
        employee=employee,
        calendar_date=date(2025, 1, 6),
        start_time=time(16, 0),
        end_time=time(18, 0),
        entry_type="scheduled",
        location=location,
    )

    assert second.id is not None
    assert CalendarEntry.objects.filter(employee=employee, calendar_date=date(2025, 1, 6)).count() == 2


@pytest.mark.django_db
@pytest.mark.unit
def test_calendar_entry_string_representation():
    """Test __str__ includes date, times, and employee name."""
    employee = EmployeeFactory()
    entry = CalendarEntry.objects.create(
        employee=employee,
        calendar_date=date(2025, 1, 6),
        start_time=time(9, 0),
        end_time=time(17, 0),
        entry_type="scheduled",
    )

    result = str(entry)

    assert "2025-01-06" in result
    assert employee.last_name in result
