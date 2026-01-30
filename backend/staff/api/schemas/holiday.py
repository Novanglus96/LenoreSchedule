from ninja import Schema
from pydantic import ConfigDict
from typing import Optional


# The class HolidayIn is a schema for validating holidays.
class HolidayIn(Schema):
    """
    Schema to validate a Holiday object.

    Attributes:
        holiday_name (str): The name of the holiday. Unique.
    """

    holiday_name: str
    rule_type: str
    observed_rule: str = None
    month: Optional[int] = None
    day: Optional[int] = None
    weekday: Optional[int] = None
    week: Optional[int] = None


# The class HolidayOut is a schema for representing holidays.
class HolidayOut(Schema):
    """
    Schema to represent a Holiday object.

    Attributes:
        id (int): ID of the Holiday object.
        holiday_name (str): The name of the holiday. Unique.
    """

    id: int
    holiday_name: str
    rule_type: str
    observed_rule: str = None
    month: Optional[int] = None
    day: Optional[int] = None
    weekday: Optional[int] = None
    week: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
