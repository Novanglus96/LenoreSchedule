from django.db import IntegrityError, transaction
from groups.models import Group
from groups.dto import DomainGroup, DomainGroupIn
from groups.exceptions import (
    GroupAlreadyExists,
    GroupCreationError,
    GroupDoesNotExist,
)
from groups.mappers import domain_group_to_model, model_to_domain_group


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
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise GroupDoesNotExist(group_id)

    if Group.objects.filter(group_name=dto.group_name).exists():
        raise GroupAlreadyExists()

    if dto.group_name is not None:
        group.group_name = dto.group_name

    group.save()

    return model_to_domain_group(group)
