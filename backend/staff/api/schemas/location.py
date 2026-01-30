from ninja import Schema
from pydantic import ConfigDict


# The class LocationIn is a schema for validating locations.
class LocationIn(Schema):
    """
    Schema to validate a Location object.

    Attributes:
        location_name (str): The name of the location. Unique.
    """

    location_name: str


# The class GtroupOut is a schema for representing locations.
class LocationOut(Schema):
    """
    Schema to represent a Location object.

    Attributes:
        id (int): ID of the Location object.
        location_name (str): The name of the location. Unique.
    """

    id: int
    location_name: str

    model_config = ConfigDict(from_attributes=True)
