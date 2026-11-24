from ninja import Schema
from pydantic import ConfigDict
from typing import List, Optional


# The class DivisionIn is a schema for validating divisions.
class DivisionIn(Schema):
    """
    Schema to validate a Division object.

    Attributes:
        division_name (str): The name of the division. Unique.
    """

    division_name: str
    sort_order: Optional[int] = None


# The class GtroupOut is a schema for representing divisions.
class DivisionOut(Schema):
    """
    Schema to represent a Division object.

    Attributes:
        id (int): ID of the Division object.
        division_name (str): The name of the division. Unique.
    """

    id: int
    division_name: str
    sort_order: int = 0

    model_config = ConfigDict(from_attributes=True)


class DivisionReorderIn(Schema):
    """
    Schema for reordering divisions.

    Attributes:
        division_ids (List[int]): Every division ID, once each, in display order.
    """

    division_ids: List[int]
