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
    start_time: time
    end_time: time
    confirmed: bool
    location: DomainLocation
    hours: Decimal


@dataclass(frozen=True)
class DomainCalendarEntryIn:
    employee_id: int
    calendar_date: date
    start_time: time
    end_time: time
    confirmed: bool
    location_id: int
