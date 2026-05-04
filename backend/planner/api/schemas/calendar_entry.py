from ninja import Schema
from datetime import date, time
from typing import Optional
from staff.api.schemas.employee import EmployeeOut
from staff.api.schemas.location import LocationOut
from decimal import Decimal


class ConfirmWeekIn(Schema):
    employee_id: int
    week_start: date
    week_end: date


class CalendarEntryIn(Schema):
    """
    Schema to validate a CalendarEntry object.

    Attributes:
        employee_id (int): ID of the employee.
        calendar_date (date): Date of the entry.
        confirmed (bool): Whether the entry is confirmed.
        entry_type (str): Type of entry (scheduled, vacation, sick, etc.).
        start_time (time): Start of the time block. Null for full-day entries.
        end_time (time): End of the time block. Null for full-day entries.
        location_id (int): ID of the location. Optional.
        notes (str): Free-text notes. Optional.
    """

    employee_id: int
    calendar_date: date
    confirmed: bool = False
    entry_type: str = "scheduled"
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location_id: Optional[int] = None
    break_minutes: int = 0
    notes: Optional[str] = None


class CalendarEntryOut(Schema):
    """
    Schema to represent a CalendarEntry object.

    Attributes:
        id (int): ID of the calendar entry.
        employee (EmployeeOut): Employee object.
        calendar_date (date): Date of the entry.
        confirmed (bool): Whether the entry is confirmed.
        entry_type (str): Type of entry.
        start_time (time): Start of the time block. Null for full-day entries.
        end_time (time): End of the time block. Null for full-day entries.
        location (LocationOut): Location object. Optional.
        hours (Decimal): Calculated hours for the block. Optional.
        notes (str): Free-text notes. Optional.
    """

    id: int
    employee: EmployeeOut
    calendar_date: date
    confirmed: bool = False
    entry_type: str = "scheduled"
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[LocationOut] = None
    hours: Optional[Decimal] = None
    break_minutes: int = 0
    notes: Optional[str] = None
