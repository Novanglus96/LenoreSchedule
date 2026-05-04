from ninja import Schema
from datetime import time
from typing import Optional
from staff.api.schemas.employee import EmployeeOut
from staff.api.schemas.location import LocationOut


class ScheduleTemplateIn(Schema):
    """
    Schema to validate a ScheduleTemplate object.

    Attributes:
        employee_id (int): ID of the employee.
        day_of_week (int): Day of the week (0=Monday … 6=Sunday).
        start_time (time): Start of the time block.
        end_time (time): End of the time block.
        location_id (int): ID of the location. Optional.
    """

    employee_id: int
    day_of_week: int
    start_time: time
    end_time: time
    break_minutes: int = 0
    location_id: Optional[int] = None


class ScheduleTemplateOut(Schema):
    """
    Schema to represent a ScheduleTemplate object.

    Attributes:
        id (int): ID of the schedule template.
        employee (EmployeeOut): Employee object.
        day_of_week (int): Day of the week (0=Monday … 6=Sunday).
        start_time (time): Start of the time block.
        end_time (time): End of the time block.
        location (LocationOut): Location object. Optional.
    """

    id: int
    employee: EmployeeOut
    day_of_week: int
    start_time: time
    end_time: time
    break_minutes: int = 0
    location: Optional[LocationOut] = None
