from ninja import Schema
from pydantic import ConfigDict


# The class GroupIn is a schema for validating groups.
class GroupIn(Schema):
    group_name: str


# The class GtroupOut is a schema for representing groups.
class GroupOut(Schema):
    id: int
    group_name: str

    model_config = ConfigDict(from_attributes=True)
