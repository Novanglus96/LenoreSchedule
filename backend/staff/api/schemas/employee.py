from ninja import Schema
from calendar import monthrange
from pydantic import ConfigDict, model_validator
from staff.api.schemas.division import DivisionOut
from staff.api.schemas.group import GroupOut
from staff.api.schemas.location import LocationOut
from typing import Optional
from datetime import date


# The class EmployeeIn is a schema for validating employees.
class EmployeeIn(Schema):
    """
    Schema to validate a Employee object.

    Attributes:
        first_name (str): The first name of the employee. Required. 256 Max.
        last_name (str): The last name of the employee. Required. 256 Max.
        email (str): The email of the employee. Optional. 512 max.
        division_id (int): The ID of the employee division.
        group_id (int): The ID of the employee group.
        location_id (int): The ID of the employee location.
        start_date (date): The start date of the employee. Optional.
        end_date (date): The end date of the employee. Optional.
        birth_month (int): Birthday month 1-12. Optional; set with birth_day.
        birth_day (int): Birthday day of month. Optional; no year is stored.
    """

    first_name: str
    last_name: str
    email: str
    division_id: int
    group_id: int
    location_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    birth_month: Optional[int] = None
    birth_day: Optional[int] = None

    @model_validator(mode="after")
    def _check_birthday(self):
        month, day = self.birth_month, self.birth_day
        if month is None and day is None:
            return self
        if month is None or day is None:
            raise ValueError("Birthday needs both a month and a day")
        if not 1 <= month <= 12:
            raise ValueError("Birthday month must be 1-12")
        # 2000 is a leap year, so Feb 29 is accepted.
        if not 1 <= day <= monthrange(2000, month)[1]:
            raise ValueError("Birthday day is not valid for that month")
        return self


# The class GtroupOut is a schema for representing employees.
class EmployeeOut(Schema):
    """
    Schema to represent a Employee object.

    Attributes:
        id (int): ID of the Employee object.
        first_name (str): The first name of the employee. Required. 256 Max.
        last_name (str): The last name of the employee. Required. 256 Max.
        email (str): The email of the employee. Optional. 512 max.
        division (DivisionOut): The division of the employee.
        group (GroupOut): The group of the employee.
    """

    id: int
    first_name: str
    last_name: str
    email: str
    division: DivisionOut
    group: GroupOut
    location: LocationOut
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    birth_month: Optional[int] = None
    birth_day: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
