from django.db import IntegrityError, transaction
from typing import List

from planner.models import EntryType
from planner.dto import DomainEntryType, DomainEntryTypeIn
from planner.exceptions import (
    EntryTypeAlreadyExists,
    EntryTypeCreationError,
    EntryTypeDoesNotExist,
    EntryTypeCodeTooLong,
)
from planner.mappers import model_to_domain_entry_type


def get_entry_type_model_or_raise(entry_type_id: int) -> EntryType:
    try:
        return EntryType.objects.get(id=entry_type_id)
    except EntryType.DoesNotExist:
        raise EntryTypeDoesNotExist(entry_type_id)


def get_all_entry_types() -> List[DomainEntryType]:
    return [model_to_domain_entry_type(t) for t in EntryType.objects.all()]


def create_entry_type(dto: DomainEntryTypeIn) -> DomainEntryType:
    if len(dto.code) > 3:
        raise EntryTypeCodeTooLong()
    if EntryType.objects.filter(name=dto.name).exists():
        raise EntryTypeAlreadyExists()
    if EntryType.objects.filter(code=dto.code.upper()).exists():
        raise EntryTypeAlreadyExists()
    try:
        with transaction.atomic():
            obj = EntryType.objects.create(name=dto.name, code=dto.code.upper())
    except IntegrityError as e:
        raise EntryTypeCreationError() from e
    return model_to_domain_entry_type(obj)


def update_entry_type(entry_type_id: int, dto: DomainEntryTypeIn) -> DomainEntryType:
    obj = get_entry_type_model_or_raise(entry_type_id)
    if len(dto.code) > 3:
        raise EntryTypeCodeTooLong()
    if EntryType.objects.filter(name=dto.name).exclude(id=entry_type_id).exists():
        raise EntryTypeAlreadyExists()
    if EntryType.objects.filter(code=dto.code.upper()).exclude(id=entry_type_id).exists():
        raise EntryTypeAlreadyExists()
    obj.name = dto.name
    obj.code = dto.code.upper()
    obj.save()
    return model_to_domain_entry_type(obj)


def delete_entry_type(entry_type_id: int) -> str:
    obj = get_entry_type_model_or_raise(entry_type_id)
    name = obj.name
    obj.delete()
    return name
