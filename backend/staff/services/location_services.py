from django.db import IntegrityError, transaction
from staff.models import Location
from staff.dto import DomainLocation, DomainLocationIn
from staff.exceptions import (
    LocationAlreadyExists,
    LocationCreationError,
    LocationDoesNotExist,
)
from staff.mappers import domain_location_to_model, model_to_domain_location
from typing import List


def get_location_model_or_raise(location_id: int) -> Location:
    """
    `get_location_model_or_raise` gets a location or raises an error
    if not found.

    Args:
        location_id (int): The id of the location to get.

    Raises:
        LocationDoesNotExist: Location does not exist.

    Returns:
        Location: A location model object.
    """
    try:
        return Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        raise LocationDoesNotExist(location_id)


def create_location(dto: DomainLocationIn) -> DomainLocation:
    """
    `create_location` creates a location if a duplicate location does
    not exist.

    Args:
        dto (DomainLocationIn): A domain location object.

    Raises:
        LocationAlreadyExists: Location already exists.
        LocationCreationError: Locatione creation error.

    Returns:
        DomainLocation: A domain location object.
    """
    if Location.objects.filter(location_name=dto.location_name).exists():
        raise LocationAlreadyExists()

    location = domain_location_to_model(dto)

    try:
        with transaction.atomic():
            location.save()
    except IntegrityError as e:
        raise LocationCreationError() from e

    return model_to_domain_location(location)


def update_location(location_id: int, dto: DomainLocationIn) -> DomainLocation:
    """
    `update_location` updates a location

    Args:
        location_id (int): ID of the location to update.
        dto (DomainLocationIn): The updated domain location object.

    Raises:
        LocationAlreadyExists: Location already exists.

    Returns:
        DomainLocation: A domain location object.
    """
    location = get_location_model_or_raise(location_id)

    if Location.objects.filter(location_name=dto.location_name).exists():
        raise LocationAlreadyExists()

    if dto.location_name is not None:
        location.location_name = dto.location_name

    location.save()

    return model_to_domain_location(location)


def get_location(location_id: int) -> DomainLocation:
    """
    `get_location` returns a domain location object.

    Args:
        location_id (int): ID of the location to get.

    Returns:
        DomainLocation: The domain location object.
    """
    location = get_location_model_or_raise(location_id)

    return model_to_domain_location(location)


def get_ordered_list_of_locations() -> List[DomainLocation]:
    """
    `get_ordered_list_of_locations` gets a list of domain location objects, ordered
    by location_name ascending.

    Returns:
        List[DomainLocation]: A list of domain location objects.
    """
    locations = Location.objects.all().order_by("location_name")

    return [model_to_domain_location(g) for g in locations]


def delete_location(location_id: int) -> str:
    """
    `delete_location` deletes a location and returns the deleted location name.

    Args:
        location_id (int): The id of the location to delete.

    Returns:
        str: The name of the deleted location.
    """
    location = get_location_model_or_raise(location_id)
    location_name = location.location_name

    location.delete()
    return location_name
