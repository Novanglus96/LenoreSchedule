from ninja import Schema
from pydantic import ConfigDict
from staff.api.schemas.division import DivisionOut
from staff.api.schemas.group import GroupOut


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
    """

    first_name: str
    last_name: str
    email: str
    division_id: int
    group_id: int


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

    model_config = ConfigDict(from_attributes=True)
