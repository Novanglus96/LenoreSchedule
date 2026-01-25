from ninja import Schema
from pydantic import ConfigDict


# The class GroupIn is a schema for validating groups.
class GroupIn(Schema):
    """
    Schema to validate a Group object.

    Attributes:
        group_name (str): The name of the group. Unique.
    """

    group_name: str


# The class GtroupOut is a schema for representing groups.
class GroupOut(Schema):
    """
    Schema to represent a Group object.

    Attributes:
        id (int): ID of the Group object.
        group_name (str): The name of the group. Unique.
    """

    id: int
    group_name: str

    model_config = ConfigDict(from_attributes=True)
