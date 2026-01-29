from ninja import Schema
from pydantic import ConfigDict
from staff.api.schemas.department import DepartmentOut
from staff.api.schemas.group import GroupOut


# The class EmployeeIn is a schema for validating employees.
class EmployeeIn(Schema):
    """
    Schema to validate a Employee object.

    Attributes:
        first_name (str): The first name of the employee. Required. 256 Max.
        last_name (str): The last name of the employee. Required. 256 Max.
        email (str): The email of the employee. Optional. 512 max.
        department_id (int): The ID of the employee department.
        group_id (int): The ID of the employee group.
    """

    first_name: str
    last_name: str
    email: str
    department_id: int
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
        department (DepartmentOut): The department of the employee.
        group (GroupOut): The group of the employee.
    """

    id: int
    first_name: str
    last_name: str
    email: str
    department: DepartmentOut
    group: GroupOut

    model_config = ConfigDict(from_attributes=True)
