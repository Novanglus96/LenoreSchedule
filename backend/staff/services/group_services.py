from django.db import IntegrityError, transaction
from staff.models import Group
from staff.dto import DomainGroup, DomainGroupIn
from staff.exceptions import (
    GroupAlreadyExists,
    GroupCreationError,
    GroupDoesNotExist,
)
from staff.mappers import domain_group_to_model, model_to_domain_group
from typing import List


def get_group_model_or_raise(group_id: int) -> Group:
    """
    `get_group_model_or_raise` gets a group or raises an error
    if not found.

    Args:
        group_id (int): The id of the group to get.

    Raises:
        GroupDoesNotExist: Group does not exist.

    Returns:
        Group: A group model object.
    """
    try:
        return Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise GroupDoesNotExist(group_id)


def create_group(dto: DomainGroupIn) -> DomainGroup:
    """
    `create_group` creates a group if a duplicate group does
    not exist.

    Args:
        dto (DomainGroupIn): A domain group object.

    Raises:
        GroupAlreadyExists: Group already exists.
        GroupCreationError: Groupe creation error.

    Returns:
        DomainGroup: A domain group object.
    """
    if Group.objects.filter(group_name=dto.group_name).exists():
        raise GroupAlreadyExists()

    group = domain_group_to_model(dto)

    try:
        with transaction.atomic():
            group.save()
    except IntegrityError as e:
        raise GroupCreationError() from e

    return model_to_domain_group(group)


def update_group(group_id: int, dto: DomainGroupIn) -> DomainGroup:
    """
    `update_group` updates a group

    Args:
        group_id (int): ID of the group to update.
        dto (DomainGroupIn): The updated domain group object.

    Raises:
        GroupAlreadyExists: Group already exists.

    Returns:
        DomainGroup: A domain group object.
    """
    group = get_group_model_or_raise(group_id)

    if Group.objects.filter(group_name=dto.group_name).exists():
        raise GroupAlreadyExists()

    if dto.group_name is not None:
        group.group_name = dto.group_name

    group.save()

    return model_to_domain_group(group)


def get_group(group_id: int) -> DomainGroup:
    """
    `get_group` returns a domain group object.

    Args:
        group_id (int): ID of the group to get.

    Returns:
        DomainGroup: The domain group object.
    """
    group = get_group_model_or_raise(group_id)

    return model_to_domain_group(group)


def get_ordered_list_of_groups() -> List[DomainGroup]:
    """
    `get_ordered_list_of_groups` gets a list of domain group objects, ordered
    by group_name ascending.

    Returns:
        List[DomainGroup]: A list of domain group objects.
    """
    groups = Group.objects.all().order_by("group_name")

    return [model_to_domain_group(g) for g in groups]


def delete_group(group_id: int) -> str:
    """
    `delete_group` deletes a group and returns the deleted group name.

    Args:
        group_id (int): The id of the group to delete.

    Returns:
        str: The name of the deleted group.
    """
    group = get_group_model_or_raise(group_id)
    group_name = group.group_name

    group.delete()
    return group_name
