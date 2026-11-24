"""Data for the home-page dashboard widgets."""

import calendar
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional, Tuple

from django.db.models import Q

from options.exceptions import PayrollInfoDoesNotExist
from options.services.payroll_services import get_payroll_weeks
from planner.models import CalendarEntry
from planner.services.weekly_schedule_services import _holidays_for_range
from staff.models import Employee

VACATION_CODE = "VAC"
HOLIDAY_WINDOW_DAYS = 90
HOLIDAY_LIMIT = 5
UNCONFIRMED_LIMIT = 10


@dataclass
class DashboardVacation:
    employee_id: int
    first_name: str
    last_name: str
    dates: List[date]


@dataclass
class DashboardHoliday:
    holiday_date: date
    holiday_name: str


@dataclass
class DashboardUnconfirmed:
    calendar_entry_id: int
    employee_id: int
    first_name: str
    last_name: str
    calendar_date: date
    entry_type: str


@dataclass
class DashboardBirthday:
    employee_id: int
    first_name: str
    last_name: str
    birthday_date: date


@dataclass
class DomainDashboard:
    week_start: date
    week_end: date
    vacations: List[DashboardVacation] = field(default_factory=list)
    holidays: List[DashboardHoliday] = field(default_factory=list)
    unconfirmed: List[DashboardUnconfirmed] = field(default_factory=list)
    unconfirmed_total: int = 0
    birthdays: List[DashboardBirthday] = field(default_factory=list)


def current_week(today: date) -> Tuple[date, date]:
    """
    The week the dashboard calls "this week": the payroll week containing
    ``today`` (the same week the schedule opens on), or Monday-Sunday when no
    payroll info covers it. Early-January dates can belong to the previous
    payroll year's last week, so that year is checked too.
    """
    for year in (today.year, today.year - 1):
        try:
            weeks = get_payroll_weeks(year)
        except PayrollInfoDoesNotExist:
            continue
        for w in weeks:
            if w["week_start"] <= today <= w["week_end"]:
                return w["week_start"], w["week_end"]
    monday = today - timedelta(days=today.weekday())
    return monday, monday + timedelta(days=6)


def _birthday_in_year(month: int, day: int, year: int) -> date:
    """Feb 29 birthdays fall on Feb 28 in non-leap years."""
    if month == 2 and day == 29 and not calendar.isleap(year):
        return date(year, 2, 28)
    return date(year, month, day)


def get_dashboard(divisions=None, today: Optional[date] = None) -> DomainDashboard:
    """
    `get_dashboard` gathers every dashboard widget's data in one call.

    Only employees in ``divisions`` (``None`` = all) who are employed during
    the current week are included.

    Args:
        divisions: Optional Division queryset to restrict employees to.
        today (date): Override for "today" (tests). Defaults to date.today().

    Returns:
        DomainDashboard: Vacations and birthdays this week, upcoming holidays,
        and unconfirmed overrides from the start of this week onward.
    """
    today = today or date.today()
    week_start, week_end = current_week(today)
    result = DomainDashboard(week_start=week_start, week_end=week_end)

    employees = Employee.objects.filter(
        Q(start_date__isnull=True) | Q(start_date__lte=week_end),
        Q(end_date__isnull=True) | Q(end_date__gte=today),
    )
    if divisions is not None:
        employees = employees.filter(division__in=divisions)

    # Vacations this week, one row per employee with their dates.
    by_employee = {}
    for e in (
        CalendarEntry.objects.filter(
            employee__in=employees,
            entry_type=VACATION_CODE,
            calendar_date__range=(week_start, week_end),
        )
        .select_related("employee")
        .order_by("employee__last_name", "employee__first_name", "calendar_date")
    ):
        row = by_employee.get(e.employee_id)
        if row is None:
            row = by_employee[e.employee_id] = DashboardVacation(
                employee_id=e.employee_id,
                first_name=e.employee.first_name,
                last_name=e.employee.last_name,
                dates=[],
            )
        if e.calendar_date not in row.dates:
            row.dates.append(e.calendar_date)
    result.vacations = list(by_employee.values())

    # Next few holidays from today.
    holiday_map = _holidays_for_range(
        today, today + timedelta(days=HOLIDAY_WINDOW_DAYS)
    )
    result.holidays = [
        DashboardHoliday(holiday_date=d, holiday_name=name)
        for d in sorted(holiday_map)
        for name in holiday_map[d]
    ][:HOLIDAY_LIMIT]

    # Unconfirmed overrides from the start of this week on.
    unconfirmed = CalendarEntry.objects.filter(
        employee__in=employees, confirmed=False, calendar_date__gte=week_start
    )
    result.unconfirmed_total = unconfirmed.count()
    result.unconfirmed = [
        DashboardUnconfirmed(
            calendar_entry_id=e.id,
            employee_id=e.employee_id,
            first_name=e.employee.first_name,
            last_name=e.employee.last_name,
            calendar_date=e.calendar_date,
            entry_type=e.entry_type,
        )
        for e in unconfirmed.select_related("employee").order_by(
            "calendar_date", "employee__last_name", "employee__first_name"
        )[:UNCONFIRMED_LIMIT]
    ]

    # Birthdays this week (the week can span a year boundary).
    days_by_year = {}
    current = week_start
    while current <= week_end:
        days_by_year.setdefault(current.year, []).append(current)
        current += timedelta(days=1)
    for emp in employees.filter(birth_month__isnull=False).order_by(
        "last_name", "first_name"
    ):
        for year, days in days_by_year.items():
            bday = _birthday_in_year(emp.birth_month, emp.birth_day, year)
            if bday in days:
                result.birthdays.append(
                    DashboardBirthday(
                        employee_id=emp.id,
                        first_name=emp.first_name,
                        last_name=emp.last_name,
                        birthday_date=bday,
                    )
                )
    result.birthdays.sort(key=lambda b: (b.birthday_date, b.last_name, b.first_name))

    return result
