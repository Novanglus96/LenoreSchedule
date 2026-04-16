from django.db import IntegrityError, transaction
from planner.models import ScheduleTemplate
from planner.dto import DomainScheduleTemplate, DomainScheduleTemplateIn
from planner.exceptions import (
    ScheduleTemplateCreationError,
    ScheduleTemplateDoesNotExist,
    ScheduleTemplateInvalidDayOfWeek,
    ScheduleTemplateInvalidTimeRange,
)
from planner.mappers import (
    domain_schedule_template_to_model,
    model_to_domain_schedule_template,
)
from typing import List


def get_schedule_template_model_or_raise(
    schedule_template_id: int,
) -> ScheduleTemplate:
    """
    `get_schedule_template_model_or_raise` gets a schedule_template or raises
    an error if not found.

    Args:
        schedule_template_id (int): The id of the schedule_template to get.

    Raises:
        ScheduleTemplateDoesNotExist: ScheduleTemplate does not exist.

    Returns:
        ScheduleTemplate: A schedule_template model object.
    """
    try:
        return ScheduleTemplate.objects.get(id=schedule_template_id)
    except ScheduleTemplate.DoesNotExist:
        raise ScheduleTemplateDoesNotExist(schedule_template_id)


def create_schedule_template(
    dto: DomainScheduleTemplateIn,
) -> DomainScheduleTemplate:
    """
    `create_schedule_template` creates a schedule_template after validating
    the day_of_week and time range.

    Args:
        dto (DomainScheduleTemplateIn): A domain schedule_template object.

    Raises:
        ScheduleTemplateInvalidDayOfWeek: day_of_week is not 0–6.
        ScheduleTemplateInvalidTimeRange: start_time is not before end_time.
        ScheduleTemplateCreationError: Database integrity error.

    Returns:
        DomainScheduleTemplate: A domain schedule_template object.
    """
    if dto.day_of_week < 0 or dto.day_of_week > 6:
        raise ScheduleTemplateInvalidDayOfWeek()

    if dto.start_time >= dto.end_time:
        raise ScheduleTemplateInvalidTimeRange()

    schedule_template = domain_schedule_template_to_model(dto)

    try:
        with transaction.atomic():
            schedule_template.save()
    except IntegrityError as e:
        raise ScheduleTemplateCreationError() from e

    return model_to_domain_schedule_template(schedule_template)


def update_schedule_template(
    schedule_template_id: int, dto: DomainScheduleTemplateIn
) -> DomainScheduleTemplate:
    """
    `update_schedule_template` updates a schedule_template.

    Args:
        schedule_template_id (int): ID of the schedule_template to update.
        dto (DomainScheduleTemplateIn): The updated domain schedule_template object.

    Raises:
        ScheduleTemplateDoesNotExist: ScheduleTemplate does not exist.
        ScheduleTemplateInvalidDayOfWeek: day_of_week is not 0–6.
        ScheduleTemplateInvalidTimeRange: start_time is not before end_time.

    Returns:
        DomainScheduleTemplate: A domain schedule_template object.
    """
    schedule_template = get_schedule_template_model_or_raise(schedule_template_id)

    if dto.day_of_week < 0 or dto.day_of_week > 6:
        raise ScheduleTemplateInvalidDayOfWeek()

    if dto.start_time >= dto.end_time:
        raise ScheduleTemplateInvalidTimeRange()

    schedule_template.employee_id = dto.employee_id
    schedule_template.day_of_week = dto.day_of_week
    schedule_template.start_time = dto.start_time
    schedule_template.end_time = dto.end_time
    schedule_template.location_id = dto.location_id

    schedule_template.save()

    return model_to_domain_schedule_template(schedule_template)


def get_schedule_template(
    schedule_template_id: int,
) -> DomainScheduleTemplate:
    """
    `get_schedule_template` returns a domain schedule_template object.

    Args:
        schedule_template_id (int): ID of the schedule_template to get.

    Raises:
        ScheduleTemplateDoesNotExist: ScheduleTemplate does not exist.

    Returns:
        DomainScheduleTemplate: The domain schedule_template object.
    """
    schedule_template = get_schedule_template_model_or_raise(schedule_template_id)
    return model_to_domain_schedule_template(schedule_template)


def get_schedule_templates_for_employee(
    employee_id: int,
) -> List[DomainScheduleTemplate]:
    """
    `get_schedule_templates_for_employee` returns all schedule_template blocks
    for an employee, ordered by day_of_week then start_time.

    Args:
        employee_id (int): ID of the employee.

    Returns:
        List[DomainScheduleTemplate]: A list of domain schedule_template objects.
    """
    templates = ScheduleTemplate.objects.filter(
        employee_id=employee_id
    ).order_by("day_of_week", "start_time")

    return [model_to_domain_schedule_template(t) for t in templates]


def delete_schedule_template(schedule_template_id: int) -> str:
    """
    `delete_schedule_template` deletes a schedule_template and returns a
    description of the deleted block.

    Args:
        schedule_template_id (int): The id of the schedule_template to delete.

    Raises:
        ScheduleTemplateDoesNotExist: ScheduleTemplate does not exist.

    Returns:
        str: Description of the deleted schedule_template.
    """
    schedule_template = get_schedule_template_model_or_raise(schedule_template_id)
    description = str(schedule_template)

    schedule_template.delete()
    return description
