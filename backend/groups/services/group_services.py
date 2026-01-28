from django.db import IntegrityError, transaction
from groups.models import Group
from groups.dto import DomainGroup, DomainGroupIn
from groups.exceptions import (
    GroupAlreadyExists,
    GroupCreationError,
    GroupDoesNotExist,
)
from groups.mappers import domain_group_to_model, model_to_domain_group
from typing import List


def get_group_model_or_raise(group_id: int) -> Group:
    try:
        return Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise GroupDoesNotExist(group_id)


def create_group(dto: DomainGroupIn) -> DomainGroup:
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
    group = get_group_model_or_raise(group_id)

    if Group.objects.filter(group_name=dto.group_name).exists():
        raise GroupAlreadyExists()

    if dto.group_name is not None:
        group.group_name = dto.group_name

    group.save()

    return model_to_domain_group(group)


def get_group(group_id: int) -> DomainGroup:
    group = get_group_model_or_raise(group_id)

    return model_to_domain_group(group)


def get_ordered_list_of_groups() -> List[DomainGroup]:
    groups = Group.objects.all().order_by("group_name")

    return [model_to_domain_group(g) for g in groups]


def delete_group(group_id: int) -> str:
    group = get_group_model_or_raise(group_id)
    group_name = group.group_name

    group.delete()
    return group_name
