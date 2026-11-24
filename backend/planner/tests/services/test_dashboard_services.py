import pytest
from datetime import date

from options.factories import PayrollInfoFactory
from planner.factories import CalendarEntryFactory, HolidayFactory
from planner.services.dashboard_services import current_week, get_dashboard
from staff.factories import DivisionFactory, EmployeeFactory

# Wednesday inside the payroll week Mon Jan 6 – Sun Jan 12, 2025.
TODAY = date(2025, 1, 8)


@pytest.fixture
def payroll():
    return PayrollInfoFactory(payroll_year=2025, payroll_start=date(2025, 1, 6))


@pytest.mark.django_db
@pytest.mark.service
def test_current_week_uses_payroll_week(payroll):
    assert current_week(TODAY) == (date(2025, 1, 6), date(2025, 1, 12))


@pytest.mark.django_db
@pytest.mark.service
def test_current_week_falls_back_to_monday_sunday():
    # No payroll info at all; Sat Mar 15 2025 → Mon Mar 10 – Sun Mar 16
    assert current_week(date(2025, 3, 15)) == (date(2025, 3, 10), date(2025, 3, 16))


@pytest.mark.django_db
@pytest.mark.service
def test_current_week_early_january_uses_previous_payroll_year():
    PayrollInfoFactory(payroll_year=2025, payroll_start=date(2024, 12, 30))
    PayrollInfoFactory(payroll_year=2026, payroll_start=date(2026, 1, 5))
    # Jan 2 2026 is in 2025's last week (Dec 29 – Jan 4)
    assert current_week(date(2026, 1, 2)) == (date(2025, 12, 29), date(2026, 1, 4))


@pytest.mark.django_db
@pytest.mark.service
def test_vacations_grouped_by_employee_this_week_only(payroll):
    emp = EmployeeFactory(last_name="Able")
    other = EmployeeFactory(last_name="Baker")
    CalendarEntryFactory(employee=emp, calendar_date=date(2025, 1, 7), entry_type="VAC")
    CalendarEntryFactory(employee=emp, calendar_date=date(2025, 1, 9), entry_type="VAC")
    CalendarEntryFactory(employee=other, calendar_date=date(2025, 1, 10), entry_type="VAC")
    # Not vacation / not this week
    CalendarEntryFactory(employee=other, calendar_date=date(2025, 1, 8), entry_type="SCH")
    CalendarEntryFactory(employee=other, calendar_date=date(2025, 1, 14), entry_type="VAC")

    vac = get_dashboard(today=TODAY).vacations

    assert [(v.last_name, v.dates) for v in vac] == [
        ("Able", [date(2025, 1, 7), date(2025, 1, 9)]),
        ("Baker", [date(2025, 1, 10)]),
    ]


@pytest.mark.django_db
@pytest.mark.service
def test_upcoming_holidays_sorted_limited_and_windowed(payroll):
    for month, day in [(1, 20), (1, 9), (2, 17), (3, 1), (3, 15), (3, 20), (12, 25)]:
        HolidayFactory(month=month, day=day)
    HolidayFactory(month=1, day=1)  # already passed

    holidays = get_dashboard(today=TODAY).holidays

    assert [h.holiday_date for h in holidays] == [
        date(2025, 1, 9),
        date(2025, 1, 20),
        date(2025, 2, 17),
        date(2025, 3, 1),
        date(2025, 3, 15),
    ]


@pytest.mark.django_db
@pytest.mark.service
def test_unconfirmed_from_week_start_with_total(payroll):
    emp = EmployeeFactory()
    CalendarEntryFactory(employee=emp, calendar_date=date(2025, 1, 3))  # before week
    CalendarEntryFactory(employee=emp, calendar_date=date(2025, 1, 6))
    CalendarEntryFactory(employee=emp, calendar_date=date(2025, 2, 1))
    CalendarEntryFactory(employee=emp, calendar_date=date(2025, 1, 7), confirmed=True)
    for d in range(12, 24):
        CalendarEntryFactory(employee=emp, calendar_date=date(2025, 3, d))

    dash = get_dashboard(today=TODAY)

    assert dash.unconfirmed_total == 14
    assert len(dash.unconfirmed) == 10
    assert dash.unconfirmed[0].calendar_date == date(2025, 1, 6)


@pytest.mark.django_db
@pytest.mark.service
def test_birthdays_this_week_and_feb29_in_non_leap_year():
    # Week Mon Feb 24 – Sun Mar 2, 2025 (no payroll info → Mon–Sun)
    EmployeeFactory(last_name="Leap", birth_month=2, birth_day=29)
    EmployeeFactory(last_name="March", birth_month=3, birth_day=2)
    EmployeeFactory(last_name="Later", birth_month=3, birth_day=3)
    EmployeeFactory(last_name="None")

    birthdays = get_dashboard(today=date(2025, 2, 26)).birthdays

    assert [(b.last_name, b.birthday_date) for b in birthdays] == [
        ("Leap", date(2025, 2, 28)),
        ("March", date(2025, 3, 2)),
    ]


@pytest.mark.django_db
@pytest.mark.service
def test_birthdays_across_year_boundary():
    # Mon Dec 29 2025 – Sun Jan 4 2026
    EmployeeFactory(last_name="Dec", birth_month=12, birth_day=31)
    EmployeeFactory(last_name="Jan", birth_month=1, birth_day=2)

    birthdays = get_dashboard(today=date(2025, 12, 30)).birthdays

    assert [(b.last_name, b.birthday_date) for b in birthdays] == [
        ("Dec", date(2025, 12, 31)),
        ("Jan", date(2026, 1, 2)),
    ]


@pytest.mark.django_db
@pytest.mark.service
def test_excludes_departed_employees_and_other_divisions(payroll):
    from staff.models import Division

    mine = DivisionFactory()
    theirs = DivisionFactory()
    gone = EmployeeFactory(division=mine, end_date=date(2025, 1, 7), birth_month=1, birth_day=9)
    other_div = EmployeeFactory(division=theirs, birth_month=1, birth_day=9)
    keep = EmployeeFactory(division=mine, birth_month=1, birth_day=9)
    for emp in (gone, other_div, keep):
        CalendarEntryFactory(employee=emp, calendar_date=date(2025, 1, 10), entry_type="VAC")

    dash = get_dashboard(divisions=Division.objects.filter(id=mine.id), today=TODAY)

    assert [b.employee_id for b in dash.birthdays] == [keep.id]
    assert [v.employee_id for v in dash.vacations] == [keep.id]
    assert [u.employee_id for u in dash.unconfirmed] == [keep.id]
