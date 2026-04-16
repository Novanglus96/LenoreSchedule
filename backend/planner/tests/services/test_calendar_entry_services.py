import pytest
from datetime import date, time
from planner.dto import DomainCalendarEntry, DomainCalendarEntryIn
from planner.factories import CalendarEntryFactory
from planner.models import CalendarEntry
from planner.services.calendar_services import (
    create_calendar_entry,
    update_calendar_entry,
    delete_calendar_entry,
)
from planner.exceptions import (
    CalendarEntryAlreadyExists,
    CalendarEntryDoesNotExist,
)
from staff.factories import EmployeeFactory, LocationFactory


# ---------------------------------------------------------------------------
# create_calendar_entry
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_create_calendar_entry_scheduled_success():
    """Creating a scheduled calendar entry with times should succeed."""
    employee = EmployeeFactory()
    location = LocationFactory()
    dto = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        start_time=time(9, 0),
        end_time=time(17, 0),
        confirmed=False,
        entry_type="scheduled",
        location_id=location.id,
    )

    result = create_calendar_entry(dto)

    assert isinstance(result, DomainCalendarEntry)
    assert result.entry_type == "scheduled"
    assert result.start_time == time(9, 0)
    assert CalendarEntry.objects.filter(
        employee_id=employee.id, calendar_date=date(2025, 1, 6)
    ).exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_calendar_entry_full_day_absence_success():
    """Creating a full-day vacation entry with null times should succeed."""
    employee = EmployeeFactory()
    dto = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        confirmed=False,
        entry_type="vacation",
    )

    result = create_calendar_entry(dto)

    assert isinstance(result, DomainCalendarEntry)
    assert result.entry_type == "vacation"
    assert result.start_time is None
    assert result.end_time is None
    assert result.location is None


@pytest.mark.django_db
@pytest.mark.service
def test_create_calendar_entry_with_notes_success():
    """Creating a calendar entry with notes should store them correctly."""
    employee = EmployeeFactory()
    dto = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        confirmed=False,
        entry_type="sick",
        notes="Doctor appointment.",
    )

    result = create_calendar_entry(dto)

    assert result.notes == "Doctor appointment."


@pytest.mark.django_db
@pytest.mark.service
def test_create_calendar_entry_multiple_blocks_same_day_success():
    """Creating two non-contiguous blocks on the same day should succeed."""
    employee = EmployeeFactory()
    location = LocationFactory()
    dto1 = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        start_time=time(10, 0),
        end_time=time(14, 0),
        confirmed=False,
        entry_type="scheduled",
        location_id=location.id,
    )
    dto2 = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        start_time=time(16, 0),
        end_time=time(18, 0),
        confirmed=False,
        entry_type="scheduled",
        location_id=location.id,
    )

    create_calendar_entry(dto1)
    result = create_calendar_entry(dto2)

    assert result.id is not None
    assert CalendarEntry.objects.filter(
        employee_id=employee.id, calendar_date=date(2025, 1, 6)
    ).count() == 2


@pytest.mark.django_db
@pytest.mark.service
def test_create_calendar_entry_duplicate_raises():
    """Creating an identical entry (same employee, date, times, type) should raise."""
    employee = EmployeeFactory()
    location = LocationFactory()
    dto = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        start_time=time(9, 0),
        end_time=time(17, 0),
        confirmed=False,
        entry_type="scheduled",
        location_id=location.id,
    )

    create_calendar_entry(dto)

    with pytest.raises(CalendarEntryAlreadyExists):
        create_calendar_entry(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_calendar_entry_duplicate_full_day_raises():
    """Creating two full-day vacation entries for the same employee and date should raise."""
    employee = EmployeeFactory()
    dto = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        confirmed=False,
        entry_type="vacation",
    )

    create_calendar_entry(dto)

    with pytest.raises(CalendarEntryAlreadyExists):
        create_calendar_entry(dto)


# ---------------------------------------------------------------------------
# update_calendar_entry
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_update_calendar_entry_success():
    """Updating a calendar entry should persist the changes."""
    existing = CalendarEntryFactory(entry_type="scheduled", notes=None)
    dto = DomainCalendarEntryIn(
        employee_id=existing.employee.id,
        calendar_date=existing.calendar_date,
        start_time=time(10, 0),
        end_time=time(18, 0),
        confirmed=True,
        entry_type="overtime",
        location_id=existing.location.id,
        notes="Covering for absence.",
    )

    result = update_calendar_entry(existing.id, dto)

    assert isinstance(result, DomainCalendarEntry)
    assert result.entry_type == "overtime"
    assert result.notes == "Covering for absence."
    assert result.confirmed is True


@pytest.mark.django_db
@pytest.mark.service
def test_update_calendar_entry_to_full_day_absence():
    """Updating a scheduled entry to a full-day vacation should clear times."""
    existing = CalendarEntryFactory(
        start_time=time(9, 0),
        end_time=time(17, 0),
        entry_type="scheduled",
    )
    dto = DomainCalendarEntryIn(
        employee_id=existing.employee.id,
        calendar_date=existing.calendar_date,
        confirmed=False,
        entry_type="vacation",
    )

    result = update_calendar_entry(existing.id, dto)

    assert result.entry_type == "vacation"
    assert result.start_time is None
    assert result.end_time is None


@pytest.mark.django_db
@pytest.mark.service
def test_update_calendar_entry_not_found_raises():
    """Updating a non-existent calendar entry should raise CalendarEntryDoesNotExist."""
    employee = EmployeeFactory()
    dto = DomainCalendarEntryIn(
        employee_id=employee.id,
        calendar_date=date(2025, 1, 6),
        confirmed=False,
        entry_type="scheduled",
    )

    with pytest.raises(CalendarEntryDoesNotExist):
        update_calendar_entry(99999, dto)


@pytest.mark.django_db
@pytest.mark.service
def test_update_calendar_entry_same_values_does_not_raise():
    """Updating a calendar entry with the same values should succeed (no false AlreadyExists)."""
    existing = CalendarEntryFactory(entry_type="scheduled")
    dto = DomainCalendarEntryIn(
        employee_id=existing.employee.id,
        calendar_date=existing.calendar_date,
        start_time=existing.start_time,
        end_time=existing.end_time,
        confirmed=existing.confirmed,
        entry_type=existing.entry_type,
        location_id=existing.location.id if existing.location else None,
    )

    result = update_calendar_entry(existing.id, dto)

    assert result.id == existing.id


# ---------------------------------------------------------------------------
# delete_calendar_entry
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_delete_calendar_entry_success():
    """Deleting a calendar entry should remove it from the database."""
    existing = CalendarEntryFactory()

    result = delete_calendar_entry(existing.id)

    assert result == existing.calendar_date
    assert not CalendarEntry.objects.filter(id=existing.id).exists()


@pytest.mark.django_db
@pytest.mark.service
def test_delete_calendar_entry_not_found_raises():
    """Deleting a non-existent calendar entry should raise CalendarEntryDoesNotExist."""
    with pytest.raises(CalendarEntryDoesNotExist):
        delete_calendar_entry(99999)
