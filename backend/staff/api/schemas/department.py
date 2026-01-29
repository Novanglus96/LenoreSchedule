from ninja import Schema
from pydantic import ConfigDict


# The class DepartmentIn is a schema for validating departments.
class DepartmentIn(Schema):
    """
    Schema to validate a Department object.

    Attributes:
        department_name (str): The name of the department. Unique.
    """

    department_name: str


# The class GtroupOut is a schema for representing departments.
class DepartmentOut(Schema):
    """
    Schema to represent a Department object.

    Attributes:
        id (int): ID of the Department object.
        department_name (str): The name of the department. Unique.
    """

    id: int
    department_name: str

    model_config = ConfigDict(from_attributes=True)
