from django.db import IntegrityError, transaction
from planner.models import Holiday
from planner.dto import DomainHoliday, DomainHolidayIn
from planner.exceptions import (
    HolidayAlreadyExists,
    HolidayCreationError,
    HolidayDoesNotExist,
    HolidayInvalidRuleError,
    HolidayInvalidObservedRuleError,
    HolidayInvalidMonthError,
    HolidayInvalidDayError,
    HolidayInvalidWeekDayError,
    HolidayInvalidWeekError,
)
from planner.mappers import domain_holiday_to_model, model_to_domain_holiday
from typing import List
from datetime import date, timedelta
import calendar
from django.core.exceptions import ValidationError


def get_last_weekday(year, month, weekday) -> int:
    """
    `get_last_weekday` gets the last day (M-Su) of a month for a year.

    Args:
        year (int): 4 digit year
        month (int): 1-12 for month.
        weekday (int): 0-6 for M-Su

    Returns:
        (int): The date of the last day.
    """
    # Returns a matrix of weeks (0 represents days outside the month)
    cal = calendar.monthcalendar(year, month)

    # Extract the column for the specific weekday and filter out the zeros
    last_day = [week[weekday] for week in cal if week[weekday] != 0][-1]

    return last_day


def calculate_easter(year) -> date:
    """
    `calculate_easter` calculates the date of easter for a given year.

    Args:
        year (int): 4 digit year

    Returns:
        (date): The date of easter for the year.
    """
    # The Anonymous Gregorian Algorithm
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) // 451

    month = (h + L - 7 * m + 114) // 31
    day = ((h + L - 7 * m + 114) % 31) + 1

    return date(year, month, day)


def get_nth_weekday(year, month, nth, weekday) -> int:
    """
    `get_nth_weekday` calculates the nth weekday of the month.

    Args:
        year (int): 4 digit year
        month (int): 1-12 for month.
        nth (int): The nth occurrence
        weekday (int): 0-6 for M-Su

    Returns:
        (int): The date of the nth occurrence.
    """
    # Returns a list of lists representing the calendar month
    cal = calendar.monthcalendar(year, month)

    # Extract the specific column for the weekday you want
    # This gives you a list of dates for that weekday across all weeks
    days_of_month = [week[weekday] for week in cal if week[weekday] != 0]

    try:
        return days_of_month[nth - 1]
    except IndexError:
        return None  # In case you ask for the 5th Monday and there are only 4


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
        holiday.full_clean()
    except ValidationError as exc:
        if "rule_type" in exc.message_dict:
            raise HolidayInvalidRuleError(
                f"Invalid rule_type: {dto.rule_type}"
            ) from exc
        elif "observed_rule" in exc.message_dict:
            raise HolidayInvalidObservedRuleError(
                f"Invalid observed_rule: {dto.observed_rule}"
            ) from exc
        raise  # re-raise anything else

    if holiday.month and (holiday.month < 1 or holiday.month > 12):
        raise HolidayInvalidMonthError

    if holiday.day and (holiday.day < 1 or holiday.day > 31):
        raise HolidayInvalidDayError

    if holiday.weekday and (holiday.weekday < 0 or holiday.weekday > 6):
        raise HolidayInvalidWeekDayError

    if holiday.week and (holiday.week < 1 or holiday.week > 5):
        raise HolidayInvalidWeekError

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
        (str): The name of the deleted holiday.
    """
    holiday = get_holiday_model_or_raise(holiday_id)
    holiday_name = holiday.holiday_name

    holiday.delete()
    return holiday_name


def get_holiday_date_for_year(holiday_id: int, year: int) -> dict:
    """
    `get_holiday_date_for_year` gets the date of a holiday for the provided
    year.  Returns the holiday name, date, and wether it is observed in a dictionary.

    Args:
        holiday_id (int): The id of the holiday to delete.
        year (int): 4 digit year

    Returns:
        (dict): {"holiday_name": holiday name, "holiday_date": date of holiday, "observed": True/False}
    """
    holiday = get_holiday_model_or_raise(holiday_id)
    holiday_date = None
    observed = False

    if holiday.rule_type == "fixed_date":
        holiday_date = date(year, holiday.month, holiday.day)
        if holiday.observed_rule == "nearest_weekday":
            if holiday_date.weekday() == 5:
                holiday_date = holiday_date - timedelta(days=1)
                observed = True
            elif holiday_date.weekday() == 6:
                holiday_date = holiday_date + timedelta(days=1)
                observed = True
        elif holiday.observed_rule == "next_business_day":
            if holiday_date.weekday() == 5:
                holiday_date = holiday_date + timedelta(days=2)
                observed = True
            elif holiday_date.weekday() == 6:
                holiday_date = holiday_date + timedelta(days=1)
                observed = True
    elif holiday.rule_type == "nth_weekday":
        nth_day = get_nth_weekday(
            year, holiday.month, holiday.week, holiday.weekday
        )
        holiday_date = date(year, holiday.month, nth_day)
    elif holiday.rule_type == "last_weekday":
        last_day = get_last_weekday(year, holiday.month, holiday.weekday)
        holiday_date = date(year, holiday.month, last_day)
    elif holiday.rule_type == "custom":
        if "easter" in holiday.holiday_name.lower():
            holiday_date = calculate_easter(year)
        if "good friday" in holiday.holiday_name.lower():
            holiday_date = calculate_easter(year) - timedelta(days=2)
        if "election" in holiday.holiday_name.lower():
            nth_day = get_nth_weekday(year, 11, 1, 0)
            holiday_date = date(year, 11, nth_day) + timedelta(days=1)
    return {
        "holiday_name": holiday.holiday_name,
        "holiday_date": holiday_date,
        "observed": observed,
    }
