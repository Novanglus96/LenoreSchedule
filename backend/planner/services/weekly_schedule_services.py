from datetime import date, timedelta
from django.db.models import Q

from planner.models import CalendarEntry, ScheduleTemplate, Holiday
from planner.dto import (
    DomainDayEntry,
    DomainEmployeeDay,
    DomainEmployeeWeekSchedule,
    DomainDivisionWeekSchedule,
    DomainWeeklySchedule,
)
from planner.services.holiday_services import get_holiday_date_for_year
from staff.models import Division, Employee
from staff.mappers import model_to_domain_location
from options.services.payroll_services import get_payroll_weeks


def _holidays_for_range(week_start: date, week_end: date) -> dict:
    """
    Returns {date: [holiday_name, ...]} for all configured holidays that
    fall within the given date range, accounting for observed rules.
    """
    years = {week_start.year, week_end.year}
    result = {}
    for holiday in Holiday.objects.all():
        for year in years:
            info = get_holiday_date_for_year(holiday.id, year)
            h_date = info["holiday_date"]
            if h_date and week_start <= h_date <= week_end:
                result.setdefault(h_date, []).append(info["holiday_name"])
    return result


def get_weekly_division_schedule(
    page: int,
    payroll_year: int,
    divisions,
) -> DomainWeeklySchedule:
    """
    `get_weekly_division_schedule` returns a merged weekly schedule for all
    employees in the user's accessible divisions.

    Each employee's days contain entries from three sources merged together:
      - "template" — their recurring ScheduleTemplate blocks for that weekday
      - "calendar" — CalendarEntry overrides/additions for that date
      - "holiday"  — any configured holidays that fall on that date

    Args:
        page (int): 0-based week index within the payroll year.
        payroll_year (int): The payroll year to look up weeks for.
        divisions: Django queryset of Division objects the user can access,
                   or None for unrestricted access.

    Raises:
        PayrollInfoDoesNotExist: No PayrollInfo for the given year.
        IndexError: page is out of range for the generated week list.

    Returns:
        DomainWeeklySchedule: The full weekly schedule grouped by division.
    """
    weeks = get_payroll_weeks(payroll_year)
    total_pages = len(weeks)

    if page < 0 or page >= total_pages:
        raise IndexError(f"Page {page} out of range (0–{total_pages - 1})")

    week = weeks[page]
    week_start: date = week["week_start"]
    week_end: date = week["week_end"]
    week_label: str = week["label"]

    today = date.today()
    current_page = next(
        (w["page"] for w in weeks if w["week_start"] <= today <= w["week_end"]),
        0,
    )

    holiday_map = _holidays_for_range(week_start, week_end)

    # Resolve which divisions to query
    if divisions is None:
        division_qs = Division.objects.all().order_by("division_name")
    else:
        division_qs = divisions.order_by("division_name")

    divisions_out = []

    for division in division_qs:
        employees = (
            Employee.objects.filter(
                division=division,
                start_date__lte=week_end,
            )
            .filter(Q(end_date__isnull=True) | Q(end_date__gte=week_start))
            .order_by("last_name", "first_name")
            .select_related("location", "division", "group")
        )

        employee_schedules = []

        for employee in employees:
            # Build day-of-week → template blocks mapping (0=Mon … 6=Sun)
            templates = ScheduleTemplate.objects.filter(
                employee=employee
            ).select_related("location")
            template_by_dow: dict = {}
            for t in templates:
                template_by_dow.setdefault(t.day_of_week, []).append(t)

            # Build date → calendar entries mapping
            calendar_entries = (
                CalendarEntry.objects.filter(
                    employee=employee,
                    calendar_date__gte=week_start,
                    calendar_date__lte=week_end,
                )
                .select_related("location")
                .order_by("calendar_date", "start_time")
            )
            entries_by_date: dict = {}
            for e in calendar_entries:
                entries_by_date.setdefault(e.calendar_date, []).append(e)

            days = []
            for i in range(7):
                current_date = week_start + timedelta(days=i)
                dow = current_date.weekday()  # 0=Mon, matches ScheduleTemplate
                day_entries = []

                for t in template_by_dow.get(dow, []):
                    day_entries.append(
                        DomainDayEntry(
                            source="template",
                            entry_type="scheduled",
                            start_time=t.start_time,
                            end_time=t.end_time,
                            location=model_to_domain_location(t.location) if t.location else None,
                        )
                    )

                for e in entries_by_date.get(current_date, []):
                    day_entries.append(
                        DomainDayEntry(
                            source="calendar",
                            entry_type=e.entry_type,
                            start_time=e.start_time,
                            end_time=e.end_time,
                            location=model_to_domain_location(e.location) if e.location else None,
                            confirmed=e.confirmed,
                            notes=e.notes,
                            calendar_entry_id=e.id,
                        )
                    )

                for holiday_name in holiday_map.get(current_date, []):
                    day_entries.append(
                        DomainDayEntry(
                            source="holiday",
                            entry_type="holiday",
                            holiday_name=holiday_name,
                        )
                    )

                days.append(DomainEmployeeDay(date=current_date, entries=day_entries))

            employee_schedules.append(
                DomainEmployeeWeekSchedule(
                    employee_id=employee.id,
                    first_name=employee.first_name,
                    last_name=employee.last_name,
                    group_name=employee.group.group_name,
                    days=days,
                )
            )

        if employee_schedules:
            divisions_out.append(
                DomainDivisionWeekSchedule(
                    division_id=division.id,
                    division_name=division.division_name,
                    employees=employee_schedules,
                )
            )

    return DomainWeeklySchedule(
        week_label=week_label,
        week_start=week_start,
        week_end=week_end,
        page=page,
        total_pages=total_pages,
        current_page=current_page,
        divisions=divisions_out,
    )
