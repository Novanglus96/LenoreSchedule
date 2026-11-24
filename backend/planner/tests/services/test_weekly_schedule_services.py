import pytest
from datetime import date, time

from options.factories import PayrollInfoFactory
from planner.factories import CalendarEntryFactory, ScheduleTemplateFactory
from planner.services.weekly_schedule_services import get_weekly_division_schedule
from staff.factories import EmployeeFactory

MONDAY = date(2025, 1, 6)


def _employee_days(schedule, employee_id):
    for div in schedule.divisions:
        for grp in div.groups:
            for emp in grp.employees:
                if emp.employee_id == employee_id:
                    return emp.days
    raise AssertionError("employee not in schedule")


@pytest.mark.django_db
@pytest.mark.service
def test_template_entries_present_even_when_override_supersedes():
    PayrollInfoFactory(payroll_year=2025, payroll_start=MONDAY)
    emp = EmployeeFactory()
    ScheduleTemplateFactory(
        employee=emp, day_of_week=0, start_time=time(8, 0), end_time=time(16, 0)
    )
    CalendarEntryFactory(employee=emp, calendar_date=MONDAY, entry_type="VAC")

    days = _employee_days(get_weekly_division_schedule(0, 2025, None), emp.id)
    monday = days[0]

    assert [e.source for e in monday.entries] == ["calendar"]
    assert len(monday.template_entries) == 1
    assert monday.template_entries[0].start_time == time(8, 0)
    assert monday.template_entries[0].end_time == time(16, 0)
    # Tuesday has no template
    assert days[1].template_entries == []


@pytest.mark.django_db
@pytest.mark.service
def test_accept_default_week_creates_confirmed_entries_for_template_days_only():
    from planner.factories import HolidayFactory
    from planner.models import CalendarEntry
    from planner.services.weekly_schedule_services import accept_default_week

    emp = EmployeeFactory(end_date=date(2025, 1, 10))  # leaves Friday
    for dow in range(7):  # template every day incl. weekend
        ScheduleTemplateFactory(
            employee=emp, day_of_week=dow, start_time=time(8, 0), end_time=time(16, 0),
            break_minutes=30,
        )
    # Mon: existing override → untouched
    CalendarEntryFactory(employee=emp, calendar_date=MONDAY, entry_type="VAC")
    # Wed Jan 8: holiday → skipped
    HolidayFactory(month=1, day=8)

    created = accept_default_week(emp.id, MONDAY, date(2025, 1, 12))

    new = CalendarEntry.objects.filter(employee=emp, entry_type="SCH")
    # Tue, Thu, Fri only (Sat/Sun are after end_date)
    assert created == 3
    assert sorted(e.calendar_date.day for e in new) == [7, 9, 10]
    assert all(e.confirmed for e in new)
    assert all(e.break_minutes == 30 for e in new)
    # Template had no location → employee default location
    assert all(e.location_id == emp.location_id for e in new)
    # Running again is a no-op
    assert accept_default_week(emp.id, MONDAY, date(2025, 1, 12)) == 0
