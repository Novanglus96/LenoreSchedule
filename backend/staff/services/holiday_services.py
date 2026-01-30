from django.db import IntegrityError, transaction
from staff.models import Holiday
from staff.dto import DomainHoliday, DomainHolidayIn
from staff.exceptions import (
    HolidayAlreadyExists,
    HolidayCreationError,
    HolidayDoesNotExist,
)
from staff.mappers import domain_holiday_to_model, model_to_domain_holiday
from typing import List


def get_holiday_model_or_raise(holiday_id: int) -> Holiday:
    """
    `get_holiday_model_or_raise` gets a holiday or raises an error
    if not found.

    Args:
        holiday_id (int): The id of the holiday to get.

    Raises:
        HolidayDoesNotExist: Holiday does not exist.

    Returns:
        Holiday: A holiday model object.
    """
    try:
        return Holiday.objects.get(id=holiday_id)
    except Holiday.DoesNotExist:
        raise HolidayDoesNotExist(holiday_id)


def create_holiday(dto: DomainHolidayIn) -> DomainHoliday:
    """
    `create_holiday` creates a holiday if a duplicate holiday does
    not exist.

    Args:
        dto (DomainHolidayIn): A domain holiday object.

    Raises:
        HolidayAlreadyExists: Holiday already exists.
        HolidayCreationError: Holidaye creation error.

    Returns:
        DomainHoliday: A domain holiday object.
    """
    if Holiday.objects.filter(holiday_name=dto.holiday_name).exists():
        raise HolidayAlreadyExists()

    holiday = domain_holiday_to_model(dto)

    try:
        with transaction.atomic():
            holiday.save()
    except IntegrityError as e:
        raise HolidayCreationError() from e

    return model_to_domain_holiday(holiday)


def update_holiday(holiday_id: int, dto: DomainHolidayIn) -> DomainHoliday:
    """
    `update_holiday` updates a holiday

    Args:
        holiday_id (int): ID of the holiday to update.
        dto (DomainHolidayIn): The updated domain holiday object.

    Raises:
        HolidayAlreadyExists: Holiday already exists.

    Returns:
        DomainHoliday: A domain holiday object.
    """
    holiday = get_holiday_model_or_raise(holiday_id)

    if Holiday.objects.filter(holiday_name=dto.holiday_name).exists():
        raise HolidayAlreadyExists()

    if dto.holiday_name is not None:
        holiday.holiday_name = dto.holiday_name

    if dto.rule_type is not None:
        holiday.rule_type = dto.rule_type

    if dto.observed_rule is not None:
        holiday.observed_rule = dto.observed_rule

    if dto.month is not None:
        holiday.month = dto.month

    if dto.day is not None:
        holiday.day = dto.month

    if dto.weekday is not None:
        holiday.weekday = dto.weekday

    if dto.week is not None:
        holiday.week = dto.week

    holiday.save()

    return model_to_domain_holiday(holiday)


def get_holiday(holiday_id: int) -> DomainHoliday:
    """
    `get_holiday` returns a domain holiday object.

    Args:
        holiday_id (int): ID of the holiday to get.

    Returns:
        DomainHoliday: The domain holiday object.
    """
    holiday = get_holiday_model_or_raise(holiday_id)

    return model_to_domain_holiday(holiday)


def get_ordered_list_of_holidays() -> List[DomainHoliday]:
    """
    `get_ordered_list_of_holidays` gets a list of domain holiday objects, ordered
    by holiday_name ascending.

    Returns:
        List[DomainHoliday]: A list of domain holiday objects.
    """
    holidays = Holiday.objects.all().order_by("holiday_name")

    return [model_to_domain_holiday(g) for g in holidays]


def delete_holiday(holiday_id: int) -> str:
    """
    `delete_holiday` deletes a holiday and returns the deleted holiday name.

    Args:
        holiday_id (int): The id of the holiday to delete.

    Returns:
        str: The name of the deleted holiday.
    """
    holiday = get_holiday_model_or_raise(holiday_id)
    holiday_name = holiday.holiday_name

    holiday.delete()
    return holiday_name
