from ninja import Schema
from typing import Optional
from datetime import date


class PayrollWeekOut(Schema):
    page: int
    week_start: date
    week_end: date
    label: str


# The class PayrollInfoIn is a schema for validating holidays.
class PayrollInfoIn(Schema):
    """
    Schema to validate a PayrollInfo object.

    Attributes:
        payroll_year (int): The year of the payroll. Unique.
        payroll_start (date): The date the payroll year starts.
        payroll_frequency (str): The frequencey of paychecks for a payroll.
        first_day (int): The first day of a fixed date / multi-pay month. Optional.
        seond_day (int): The scond day of a multi-pay month. Optional.
    """

    payroll_year: int
    payroll_start: date
    payroll_frequency: str
    first_day: Optional[int] = None
    second_day: Optional[int] = None
    week_start_day: str = "sun"


# The class VersionOut is a schema for representing version information.
class PayrollInfoOut(Schema):
    """
    Schema to represent a PayrollInfo object.

    Attributes:
        id (int): The id of the payroll object.
        payroll_year (int): The year of the payroll. Unique.
        payroll_start (date): The date the payroll year starts.
        payroll_frequency (str): The frequencey of paychecks for a payroll.
        first_day (int): The first day of a fixed date / multi-pay month. Optional.
        seond_day (int): The scond day of a multi-pay month. Optional.
        week_start_day (str): The day weeks start on (sun/mon). Default sun.
    """

    id: int
    payroll_year: int
    payroll_start: date
    payroll_frequency: str
    first_day: Optional[int] = None
    second_day: Optional[int] = None
    week_start_day: str = "sun"
