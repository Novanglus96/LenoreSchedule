from ninja import Schema
from typing import Optional, List
from datetime import date, time
from staff.api.schemas.location import LocationOut


class DayEntryOut(Schema):
    source: str
    entry_type: str
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[LocationOut] = None
    confirmed: Optional[bool] = None
    notes: Optional[str] = None
    holiday_name: Optional[str] = None
    calendar_entry_id: Optional[int] = None


class EmployeeDayOut(Schema):
    date: date
    entries: List[DayEntryOut]


class EmployeeWeekScheduleOut(Schema):
    employee_id: int
    first_name: str
    last_name: str
    group_name: str
    default_location_id: Optional[int] = None
    days: List[EmployeeDayOut]


class GroupWeekScheduleOut(Schema):
    group_name: str
    employees: List[EmployeeWeekScheduleOut]


class DivisionWeekScheduleOut(Schema):
    division_id: int
    division_name: str
    groups: List[GroupWeekScheduleOut]


class WeeklyScheduleOut(Schema):
    week_label: str
    week_start: date
    week_end: date
    page: int
    total_pages: int
    current_page: int
    divisions: List[DivisionWeekScheduleOut]
