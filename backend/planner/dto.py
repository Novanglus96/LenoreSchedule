from dataclasses import dataclass
from typing import Optional
from staff.dto import DomainEmployee, DomainLocation
from datetime import date, time
from decimal import Decimal


@dataclass
class DomainHoliday:
    id: int
    holiday_name: str
    rule_type: str
    observed_rule: str = None
    month: Optional[int] = None
    day: Optional[int] = None
    weekday: Optional[int] = None
    week: Optional[int] = None


@dataclass(frozen=True)
class DomainHolidayIn:
    holiday_name: str
    rule_type: str
    observed_rule: str = None
    month: Optional[int] = None
    day: Optional[int] = None
    weekday: Optional[int] = None
    week: Optional[int] = None


@dataclass
class DomainCalendarEntry:
    id: int
    employee: DomainEmployee
    calendar_date: date
    confirmed: bool
    entry_type: str
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[DomainLocation] = None
    hours: Optional[Decimal] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class DomainCalendarEntryIn:
    employee_id: int
    calendar_date: date
    confirmed: bool
    entry_type: str = "scheduled"
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location_id: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class DomainScheduleTemplate:
    id: int
    employee: DomainEmployee
    day_of_week: int
    start_time: time
    end_time: time
    location: Optional[DomainLocation] = None


@dataclass(frozen=True)
class DomainScheduleTemplateIn:
    employee_id: int
    day_of_week: int
    start_time: time
    end_time: time
    location_id: Optional[int] = None
