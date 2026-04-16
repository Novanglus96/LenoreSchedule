from ninja import Schema
from datetime import date, time
from staff.api.schemas.employee import EmployeeOut
from staff.api.schemas.location import LocationOut
from decimal import Decimal


# The class CalendaryEntryIn is a schema for validating calendar_entries.
class CalendarEntryIn(Schema):
    """
    Schema to validate a CalendaryEntry object.

    Attributes:
        employee_id (int): id of an employee object
        calendar_date (date): date of the entry
        start_time (time): start time
        end_time (time): end time
        confirmed (bool): wether confirmed or not
        location_id (int): id of a location
    """

    employee_id: int
    calendar_date: date
    start_time: time
    end_time: time
    confirmed: bool = False
    location_id: int


# The class CalendaryEntryOut is a schema for representing calendar_entries.
class CalendarEntryOut(Schema):
    """
    Schema to represent a CalendaryEntry object.

    Attributes:
        id (int): id of the calendar entry
        employee (EmployeeOut): Employee object.
        calendar_date (date): date of the entry
        start_time (time): start time
        end_time (time): end time
        confirmed (bool): wether confirmed or not
        location (LocationOut): location object
    """

    id: int
    employee: EmployeeOut
    calendar_date: date
    start_time: time
    end_time: time
    confirmed: bool = False
    location: LocationOut
    hours: Decimal
