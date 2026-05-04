from django.db import IntegrityError, transaction
from planner.models import CalendarEntry
from planner.dto import DomainCalendarEntry, DomainCalendarEntryIn
from planner.exceptions import (
    CalendarEntryAlreadyExists,
    CalendarEntryCreationError,
    CalendarEntryDoesNotExist,
)
from planner.mappers import (
    domain_calendar_entry_to_model,
    model_to_domain_calendar_entry,
)
from typing import List, Optional
from datetime import timedelta, date
from core.utils.date_utils import current_date


def dates_in_year(year: int):
    """
    `dates_in_year` gets a list of all dates in a year.

    Args:
        year (int): The year to get dates for.

    Returns:
        (List[date]): A list of dates.
    """
    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    return [start + timedelta(days=i) for i in range((end - start).days)]


def get_calendar_entry_model_or_raise(calendar_entry_id: int) -> CalendarEntry:
    """
    `get_calendar_entry_model_or_raise` gets a calendar_entry or raises an error
    if not found.

    Args:
        calendar_entry_id (int): The id of the calendar_entry to get.

    Raises:
        CalendarEntryDoesNotExist: CalendarEntry does not exist.

    Returns:
        CalendarEntry: A calendar_entry model object.
    """
    try:
        return CalendarEntry.objects.get(id=calendar_entry_id)
    except CalendarEntry.DoesNotExist:
        raise CalendarEntryDoesNotExist(calendar_entry_id)


def create_calendar_entry(dto: DomainCalendarEntryIn) -> DomainCalendarEntry:
    """
    `create_calendar_entry` creates a calendar_entry if a duplicate does not exist.

    A duplicate is defined as the same employee, date, start_time, end_time, and
    entry_type. Full-day entries (null times) are matched on employee, date, and
    entry_type only.

    Args:
        dto (DomainCalendarEntryIn): A domain calendar_entry object.

    Raises:
        CalendarEntryAlreadyExists: CalendarEntry already exists.
        CalendarEntryCreationError: CalendarEntry creation error.

    Returns:
        DomainCalendarEntry: A domain calendar_entry object.
    """
    if CalendarEntry.objects.filter(
        calendar_date=dto.calendar_date,
        employee_id=dto.employee_id,
        start_time=dto.start_time,
        end_time=dto.end_time,
        entry_type=dto.entry_type,
    ).exists():
        raise CalendarEntryAlreadyExists()

    calendar_entry = domain_calendar_entry_to_model(dto)

    try:
        with transaction.atomic():
            calendar_entry.save()
    except IntegrityError as e:
        raise CalendarEntryCreationError() from e

    return model_to_domain_calendar_entry(calendar_entry)


def update_calendar_entry(
    calendar_entry_id: int, dto: DomainCalendarEntryIn
) -> DomainCalendarEntry:
    """
    `update_calendar_entry` updates a calendar_entry

    Args:
        calendar_entry_id (int): ID of the calendar_entry to update.
        dto (DomainCalendarEntryIn): The updated domain calendar_entry object.

    Raises:
        CalendarEntryAlreadyExists: CalendarEntry already exists.

    Returns:
        DomainCalendarEntry: A domain calendar_entry object.
    """
    calendar_entry = get_calendar_entry_model_or_raise(calendar_entry_id)

    if CalendarEntry.objects.filter(
        calendar_date=dto.calendar_date,
        employee_id=dto.employee_id,
        start_time=dto.start_time,
        end_time=dto.end_time,
        entry_type=dto.entry_type,
    ).exclude(id=calendar_entry_id).exists():
        raise CalendarEntryAlreadyExists()

    if dto.calendar_date is not None:
        calendar_entry.calendar_date = dto.calendar_date

    if dto.employee_id is not None:
        calendar_entry.employee_id = dto.employee_id

    calendar_entry.start_time = dto.start_time
    calendar_entry.end_time = dto.end_time

    if dto.confirmed is not None:
        calendar_entry.confirmed = dto.confirmed

    calendar_entry.location_id = dto.location_id
    calendar_entry.break_minutes = dto.break_minutes

    if dto.entry_type is not None:
        calendar_entry.entry_type = dto.entry_type

    calendar_entry.notes = dto.notes

    calendar_entry.save()

    return model_to_domain_calendar_entry(calendar_entry)


def get_calendar(
    timeframe: str,
    employee_id: Optional[int] = None,
    divisions=None,
) -> List[DomainCalendarEntry]:
    """
    `get_calendar` returns the calendar, optionally filtered by employee and/or divisions.

    Args:
        timeframe (str): "last", "current", or "next" year.
        employee_id (Optional[int]): Restrict to a single employee.
        divisions: Optional Division queryset. When provided, only entries for
            employees belonging to those divisions are returned.

    Returns:
        List[DomainCalendarEntry]: A list of domain calendar_entry objects.
    """
    today = current_date()
    current_year = today.year
    last_year = current_year - 1
    next_year = current_year + 1
    year = current_year
    if timeframe == "last":
        year = last_year
    if timeframe == "next":
        year = next_year
    calendar_entries = CalendarEntry.objects.filter(calendar_date__year=year)
    if divisions is not None:
        calendar_entries = calendar_entries.filter(employee__division__in=divisions)
    if employee_id:
        calendar_entries = calendar_entries.filter(employee_id=employee_id)
    return [
        model_to_domain_calendar_entry(g)
        for g in calendar_entries.order_by("calendar_date")
    ]


def delete_calendar_entry(calendar_entry_id: int) -> str:
    """
    `delete_calendar_entry` deletes a calendar_entry and returns the deleted calendar_entry name.

    Args:
        calendar_entry_id (int): The id of the calendar_entry to delete.

    Returns:
        (str): The name of the deleted calendar_entry.
    """
    calendar_entry = get_calendar_entry_model_or_raise(calendar_entry_id)
    calendar_entry_date = calendar_entry.calendar_date

    calendar_entry.delete()
    return calendar_entry_date
