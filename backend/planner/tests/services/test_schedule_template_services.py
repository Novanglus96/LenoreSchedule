import pytest
from datetime import time
from planner.dto import DomainScheduleTemplate, DomainScheduleTemplateIn
from planner.factories import ScheduleTemplateFactory
from planner.models import ScheduleTemplate
from planner.services.schedule_template_services import (
    create_schedule_template,
    update_schedule_template,
    get_schedule_template,
    get_schedule_templates_for_employee,
    delete_schedule_template,
)
from planner.exceptions import (
    ScheduleTemplateDoesNotExist,
    ScheduleTemplateInvalidDayOfWeek,
    ScheduleTemplateInvalidTimeRange,
)
from staff.factories import EmployeeFactory, LocationFactory


# ---------------------------------------------------------------------------
# create_schedule_template
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_create_schedule_template_success():
    """Creating a schedule_template should be successful and persistent."""
    employee = EmployeeFactory()
    dto = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
    )

    result = create_schedule_template(dto)

    assert isinstance(result, DomainScheduleTemplate)
    assert result.day_of_week == 0
    assert result.start_time == time(9, 0)
    assert ScheduleTemplate.objects.filter(employee_id=employee.id).exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_schedule_template_with_location_success():
    """Creating a schedule_template with a location should store it correctly."""
    employee = EmployeeFactory()
    location = LocationFactory()
    dto = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=1,
        start_time=time(10, 0),
        end_time=time(14, 0),
        location_id=location.id,
    )

    result = create_schedule_template(dto)

    assert result.location is not None
    assert result.location.id == location.id


@pytest.mark.django_db
@pytest.mark.service
def test_create_schedule_template_multiple_blocks_same_day():
    """Creating multiple blocks on the same day for one employee should succeed."""
    employee = EmployeeFactory()
    dto1 = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=0,
        start_time=time(10, 0),
        end_time=time(14, 0),
    )
    dto2 = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=0,
        start_time=time(16, 0),
        end_time=time(18, 0),
    )

    create_schedule_template(dto1)
    result = create_schedule_template(dto2)

    assert result.id is not None
    assert ScheduleTemplate.objects.filter(employee_id=employee.id, day_of_week=0).count() == 2


@pytest.mark.django_db
@pytest.mark.service
def test_create_schedule_template_invalid_day_of_week_raises():
    """Creating a schedule_template with day_of_week outside 0–6 should raise."""
    employee = EmployeeFactory()
    dto = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=7,
        start_time=time(9, 0),
        end_time=time(17, 0),
    )

    with pytest.raises(ScheduleTemplateInvalidDayOfWeek):
        create_schedule_template(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_schedule_template_start_equals_end_raises():
    """Creating a schedule_template where start_time equals end_time should raise."""
    employee = EmployeeFactory()
    dto = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(9, 0),
    )

    with pytest.raises(ScheduleTemplateInvalidTimeRange):
        create_schedule_template(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_schedule_template_start_after_end_raises():
    """Creating a schedule_template where start_time is after end_time should raise."""
    employee = EmployeeFactory()
    dto = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=0,
        start_time=time(17, 0),
        end_time=time(9, 0),
    )

    with pytest.raises(ScheduleTemplateInvalidTimeRange):
        create_schedule_template(dto)


# ---------------------------------------------------------------------------
# update_schedule_template
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_update_schedule_template_success():
    """Updating a schedule_template should return an updated DomainScheduleTemplate."""
    existing = ScheduleTemplateFactory(day_of_week=0, start_time=time(9, 0), end_time=time(17, 0))
    dto = DomainScheduleTemplateIn(
        employee_id=existing.employee.id,
        day_of_week=1,
        start_time=time(10, 0),
        end_time=time(18, 0),
    )

    result = update_schedule_template(existing.id, dto)

    assert isinstance(result, DomainScheduleTemplate)
    assert result.day_of_week == 1
    assert result.start_time == time(10, 0)


@pytest.mark.django_db
@pytest.mark.service
def test_update_schedule_template_not_found_raises():
    """Updating a non-existent schedule_template should raise ScheduleTemplateDoesNotExist."""
    employee = EmployeeFactory()
    dto = DomainScheduleTemplateIn(
        employee_id=employee.id,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
    )

    with pytest.raises(ScheduleTemplateDoesNotExist):
        update_schedule_template(99999, dto)


@pytest.mark.django_db
@pytest.mark.service
def test_update_schedule_template_invalid_time_range_raises():
    """Updating a schedule_template with start >= end should raise ScheduleTemplateInvalidTimeRange."""
    existing = ScheduleTemplateFactory()
    dto = DomainScheduleTemplateIn(
        employee_id=existing.employee.id,
        day_of_week=0,
        start_time=time(17, 0),
        end_time=time(9, 0),
    )

    with pytest.raises(ScheduleTemplateInvalidTimeRange):
        update_schedule_template(existing.id, dto)


# ---------------------------------------------------------------------------
# get_schedule_template
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_get_schedule_template_success():
    """Getting a schedule_template by id should return a DomainScheduleTemplate."""
    existing = ScheduleTemplateFactory()

    result = get_schedule_template(existing.id)

    assert isinstance(result, DomainScheduleTemplate)
    assert result.id == existing.id


@pytest.mark.django_db
@pytest.mark.service
def test_get_schedule_template_not_found_raises():
    """Getting a non-existent schedule_template should raise ScheduleTemplateDoesNotExist."""
    with pytest.raises(ScheduleTemplateDoesNotExist):
        get_schedule_template(99999)


# ---------------------------------------------------------------------------
# get_schedule_templates_for_employee
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_get_schedule_templates_for_employee_returns_list():
    """get_schedule_templates_for_employee should return a list of DomainScheduleTemplate."""
    employee = EmployeeFactory()
    ScheduleTemplateFactory(employee=employee, day_of_week=0)
    ScheduleTemplateFactory(employee=employee, day_of_week=1)

    result = get_schedule_templates_for_employee(employee.id)

    assert len(result) == 2
    assert all(isinstance(t, DomainScheduleTemplate) for t in result)


@pytest.mark.django_db
@pytest.mark.service
def test_get_schedule_templates_for_employee_empty():
    """get_schedule_templates_for_employee should return an empty list when none exist."""
    employee = EmployeeFactory()

    result = get_schedule_templates_for_employee(employee.id)

    assert result == []


@pytest.mark.django_db
@pytest.mark.service
def test_get_schedule_templates_for_employee_ordered_by_day_then_time():
    """Templates should be ordered by day_of_week ascending, then start_time ascending."""
    employee = EmployeeFactory()
    ScheduleTemplateFactory(employee=employee, day_of_week=2, start_time=time(9, 0), end_time=time(13, 0))
    ScheduleTemplateFactory(employee=employee, day_of_week=0, start_time=time(16, 0), end_time=time(18, 0))
    ScheduleTemplateFactory(employee=employee, day_of_week=0, start_time=time(9, 0), end_time=time(14, 0))

    result = get_schedule_templates_for_employee(employee.id)

    assert result[0].day_of_week == 0
    assert result[0].start_time == time(9, 0)
    assert result[1].day_of_week == 0
    assert result[1].start_time == time(16, 0)
    assert result[2].day_of_week == 2


@pytest.mark.django_db
@pytest.mark.service
def test_get_schedule_templates_for_employee_excludes_other_employees():
    """Templates from other employees should not appear in the result."""
    employee = EmployeeFactory()
    other_employee = EmployeeFactory()
    ScheduleTemplateFactory(employee=employee, day_of_week=0)
    ScheduleTemplateFactory(employee=other_employee, day_of_week=0)

    result = get_schedule_templates_for_employee(employee.id)

    assert len(result) == 1
    assert result[0].employee.id == employee.id


# ---------------------------------------------------------------------------
# delete_schedule_template
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_delete_schedule_template_success():
    """Deleting a schedule_template should remove it from the database."""
    existing = ScheduleTemplateFactory()

    result = delete_schedule_template(existing.id)

    assert isinstance(result, str)
    assert not ScheduleTemplate.objects.filter(id=existing.id).exists()


@pytest.mark.django_db
@pytest.mark.service
def test_delete_schedule_template_not_found_raises():
    """Deleting a non-existent schedule_template should raise ScheduleTemplateDoesNotExist."""
    with pytest.raises(ScheduleTemplateDoesNotExist):
        delete_schedule_template(99999)
