from dataclasses import dataclass, field
from typing import Optional, List
from staff.dto import DomainEmployee, DomainLocation
from datetime import date, time
from decimal import Decimal


@dataclass
class DomainEntryType:
    id: int
    name: str
    code: str


@dataclass(frozen=True)
class DomainEntryTypeIn:
    name: str
    code: str


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
    break_minutes: int = 0
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
    break_minutes: int = 0
    notes: Optional[str] = None


@dataclass
class DomainScheduleTemplate:
    id: int
    employee: DomainEmployee
    day_of_week: int
    start_time: time
    end_time: time
    break_minutes: int = 0
    location: Optional[DomainLocation] = None


@dataclass(frozen=True)
class DomainScheduleTemplateIn:
    employee_id: int
    day_of_week: int
    start_time: time
    end_time: time
    break_minutes: int = 0
    location_id: Optional[int] = None


@dataclass
class DomainDayEntry:
    source: str  # "template" | "calendar" | "holiday"
    entry_type: str
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[DomainLocation] = None
    confirmed: Optional[bool] = None
    break_minutes: int = 0
    notes: Optional[str] = None
    holiday_name: Optional[str] = None
    calendar_entry_id: Optional[int] = None


@dataclass
class DomainEmployeeDay:
    date: date
    entries: List[DomainDayEntry] = field(default_factory=list)


@dataclass
class DomainEmployeeWeekSchedule:
    employee_id: int
    first_name: str
    last_name: str
    group_name: str
    default_location_id: Optional[int] = None
    days: List[DomainEmployeeDay] = field(default_factory=list)


@dataclass
class DomainGroupWeekSchedule:
    group_name: str
    employees: List[DomainEmployeeWeekSchedule] = field(default_factory=list)


@dataclass
class DomainDivisionWeekSchedule:
    division_id: int
    division_name: str
    groups: List[DomainGroupWeekSchedule] = field(default_factory=list)


@dataclass
class DomainWeeklySchedule:
    week_label: str
    week_start: date
    week_end: date
    page: int
    total_pages: int
    current_page: int
    divisions: List[DomainDivisionWeekSchedule] = field(default_factory=list)
