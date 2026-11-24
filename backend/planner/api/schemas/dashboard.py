from datetime import date
from typing import List

from ninja import Schema


class DashboardVacationOut(Schema):
    employee_id: int
    first_name: str
    last_name: str
    dates: List[date]


class DashboardHolidayOut(Schema):
    holiday_date: date
    holiday_name: str


class DashboardUnconfirmedOut(Schema):
    calendar_entry_id: int
    employee_id: int
    first_name: str
    last_name: str
    calendar_date: date
    entry_type: str


class DashboardBirthdayOut(Schema):
    employee_id: int
    first_name: str
    last_name: str
    birthday_date: date


class DashboardOut(Schema):
    """
    Schema for the home-page dashboard.

    Attributes:
        week_start / week_end (date): The week "this week" refers to.
        vacations: Employees with vacation entries this week.
        holidays: The next few holidays from today.
        unconfirmed: The first few unconfirmed overrides from this week on.
        unconfirmed_total (int): How many unconfirmed overrides there are.
        birthdays: Employee birthdays this week.
    """

    week_start: date
    week_end: date
    vacations: List[DashboardVacationOut]
    holidays: List[DashboardHolidayOut]
    unconfirmed: List[DashboardUnconfirmedOut]
    unconfirmed_total: int
    birthdays: List[DashboardBirthdayOut]
