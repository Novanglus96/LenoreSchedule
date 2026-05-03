from django.db import IntegrityError, transaction
from staff.models import Division
from staff.dto import DomainDivision, DomainDivisionIn
from staff.exceptions import (
    DivisionAlreadyExists,
    DivisionCreationError,
    DivisionDoesNotExist,
)
from staff.mappers import domain_division_to_model, model_to_domain_division
from typing import List


def get_division_model_or_raise(division_id: int) -> Division:
    """
    `get_division_model_or_raise` gets a division or raises an error
    if not found.

    Args:
        division_id (int): The id of the division to get.

    Raises:
        DivisionDoesNotExist: Division does not exist.

    Returns:
        Division: A division model object.
    """
    try:
        return Division.objects.get(id=division_id)
    except Division.DoesNotExist:
        raise DivisionDoesNotExist(division_id)


def create_division(dto: DomainDivisionIn) -> DomainDivision:
    """
    `create_division` creates a division if a duplicate division does
    not exist.

    Args:
        dto (DomainDivisionIn): A domain division object.

    Raises:
        DivisionAlreadyExists: Division already exists.
        DivisionCreationError: Divisione creation error.

    Returns:
        DomainDivision: A domain division object.
    """
    if Division.objects.filter(division_name=dto.division_name).exists():
        raise DivisionAlreadyExists()

    division = domain_division_to_model(dto)

    try:
        with transaction.atomic():
            division.save()
    except IntegrityError as e:
        raise DivisionCreationError() from e

    return model_to_domain_division(division)


def update_division(division_id: int, dto: DomainDivisionIn) -> DomainDivision:
    """
    `update_division` updates a division

    Args:
        division_id (int): ID of the division to update.
        dto (DomainDivisionIn): The updated domain division object.

    Raises:
        DivisionAlreadyExists: Division already exists.

    Returns:
        DomainDivision: A domain division object.
    """
    division = get_division_model_or_raise(division_id)

    if Division.objects.filter(division_name=dto.division_name).exists():
        raise DivisionAlreadyExists()

    if dto.division_name is not None:
        division.division_name = dto.division_name

    division.save()

    return model_to_domain_division(division)


def get_division(division_id: int) -> DomainDivision:
    """
    `get_division` returns a domain division object.

    Args:
        division_id (int): ID of the division to get.

    Returns:
        DomainDivision: The domain division object.
    """
    division = get_division_model_or_raise(division_id)

    return model_to_domain_division(division)


def get_ordered_list_of_divisions() -> List[DomainDivision]:
    """
    `get_ordered_list_of_divisions` gets a list of domain division objects, ordered
    by division_name ascending.

    Returns:
        List[DomainDivision]: A list of domain division objects.
    """
    divisions = Division.objects.all().order_by("division_name")

    return [model_to_domain_division(g) for g in divisions]


def delete_division(division_id: int) -> str:
    """
    `delete_division` deletes a division and returns the deleted division name.

    Args:
        division_id (int): The id of the division to delete.

    Returns:
        str: The name of the deleted division.
    """
    division = get_division_model_or_raise(division_id)
    division_name = division.division_name

    division.delete()
    return division_name
