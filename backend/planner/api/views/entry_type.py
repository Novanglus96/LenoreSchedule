from ninja import Router
from ninja.errors import HttpError
from typing import List
import logging

from planner.api.schemas.entry_type import EntryTypeIn, EntryTypeOut
from planner.exceptions import (
    EntryTypeAlreadyExists,
    EntryTypeCreationError,
    EntryTypeDoesNotExist,
    EntryTypeCodeTooLong,
)
from planner.mappers import domain_entry_type_to_schema, schema_to_domain_entry_type
from planner.services.entry_type_services import (
    get_all_entry_types,
    create_entry_type,
    update_entry_type,
    delete_entry_type,
)

api_logger = logging.getLogger("api")
error_logger = logging.getLogger("error")

entry_type_router = Router(tags=["EntryTypes"])


@entry_type_router.get("", response=List[EntryTypeOut])
def list_entry_types(request):
    return [domain_entry_type_to_schema(t) for t in get_all_entry_types()]


@entry_type_router.post("")
def create_entry_type_endpoint(request, payload: EntryTypeIn):
    try:
        dto = schema_to_domain_entry_type(payload)
        result = create_entry_type(dto)
        return {"id": result.id}
    except EntryTypeCodeTooLong:
        raise HttpError(400, "Code must be 3 characters or fewer")
    except EntryTypeAlreadyExists:
        raise HttpError(400, "An entry type with that name or code already exists")
    except EntryTypeCreationError:
        raise HttpError(400, "DB integrity error")
    except Exception as e:
        error_logger.error(str(e))
        raise HttpError(500, "EntryType creation error")


@entry_type_router.put("/{entry_type_id}")
def update_entry_type_endpoint(request, entry_type_id: int, payload: EntryTypeIn):
    try:
        dto = schema_to_domain_entry_type(payload)
        update_entry_type(entry_type_id, dto)
        return {"success": True}
    except EntryTypeCodeTooLong:
        raise HttpError(400, "Code must be 3 characters or fewer")
    except EntryTypeAlreadyExists:
        raise HttpError(400, "An entry type with that name or code already exists")
    except EntryTypeDoesNotExist:
        raise HttpError(404, f"EntryType {entry_type_id} not found")
    except Exception as e:
        error_logger.error(str(e))
        raise HttpError(500, "EntryType update error")


@entry_type_router.delete("/{entry_type_id}")
def delete_entry_type_endpoint(request, entry_type_id: int):
    try:
        delete_entry_type(entry_type_id)
        return {"success": True}
    except EntryTypeDoesNotExist:
        raise HttpError(404, f"EntryType {entry_type_id} not found")
    except Exception as e:
        error_logger.error(str(e))
        raise HttpError(500, "EntryType deletion error")
