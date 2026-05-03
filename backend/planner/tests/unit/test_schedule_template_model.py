import pytest
from datetime import time
from planner.models import ScheduleTemplate
from staff.factories import EmployeeFactory, LocationFactory


@pytest.mark.django_db
@pytest.mark.unit
def test_schedule_template_creation():
    """Test ScheduleTemplate is created successfully with required fields."""
    employee = EmployeeFactory()
    template = ScheduleTemplate.objects.create(
        employee=employee,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
    )

    assert template.id is not None
    assert template.day_of_week == 0
    assert template.start_time == time(9, 0)
    assert template.end_time == time(17, 0)
    assert template.location is None


@pytest.mark.django_db
@pytest.mark.unit
def test_schedule_template_creation_with_location():
    """Test ScheduleTemplate is created successfully with an optional location."""
    employee = EmployeeFactory()
    location = LocationFactory()
    template = ScheduleTemplate.objects.create(
        employee=employee,
        day_of_week=1,
        start_time=time(10, 0),
        end_time=time(14, 0),
        location=location,
    )

    assert template.location == location


@pytest.mark.django_db
@pytest.mark.unit
def test_schedule_template_multiple_blocks_same_day():
    """Test that multiple blocks on the same day are allowed for one employee."""
    employee = EmployeeFactory()
    ScheduleTemplate.objects.create(
        employee=employee,
        day_of_week=0,
        start_time=time(10, 0),
        end_time=time(14, 0),
    )
    second = ScheduleTemplate.objects.create(
        employee=employee,
        day_of_week=0,
        start_time=time(16, 0),
        end_time=time(18, 0),
    )

    assert second.id is not None
    assert ScheduleTemplate.objects.filter(employee=employee, day_of_week=0).count() == 2


@pytest.mark.django_db
@pytest.mark.unit
def test_schedule_template_string_representation():
    """Test __str__ returns employee name, day, and time range."""
    employee = EmployeeFactory()
    template = ScheduleTemplate.objects.create(
        employee=employee,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
    )

    result = str(template)

    assert "Monday" in result
    assert "09:00:00" in result
    assert "17:00:00" in result


@pytest.mark.django_db
@pytest.mark.unit
def test_schedule_template_location_nulled_on_location_delete():
    """Test that location is set to null when the location is deleted."""
    employee = EmployeeFactory()
    location = LocationFactory()
    template = ScheduleTemplate.objects.create(
        employee=employee,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
        location=location,
    )

    location.delete()
    template.refresh_from_db()

    assert template.location is None


@pytest.mark.django_db
@pytest.mark.unit
def test_schedule_template_deleted_on_employee_delete():
    """Test that ScheduleTemplate is deleted when the employee is deleted."""
    employee = EmployeeFactory()
    template = ScheduleTemplate.objects.create(
        employee=employee,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
    )
    template_id = template.id

    employee.delete()

    assert not ScheduleTemplate.objects.filter(id=template_id).exists()
