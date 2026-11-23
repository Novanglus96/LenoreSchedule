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
