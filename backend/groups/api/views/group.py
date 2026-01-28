from ninja import Router
from groups.api.schemas.group import GroupIn, GroupOut
from ninja.errors import HttpError
from typing import List
import logging
from groups.exceptions import (
    GroupAlreadyExists,
    GroupCreationError,
    GroupDoesNotExist,
)
from groups.mappers import schema_to_domain_group, domain_group_to_schema
from groups.services.group_services import (
    create_group,
    update_group,
    get_group,
    get_ordered_list_of_groups,
    delete_group,
)

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

group_router = Router(tags=["Groups"])


@group_router.post("/create")
def create_group_endpoint(request, payload: GroupIn):
    """
    The function `create_group_endpoint` creats a group object.

    Endpoint:
        - **Path**: `/api/v1/groups/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (GroupIn): A group schema.

    Returns:
        (dict): {'id': The ID of the created group}.
    """
    try:
        domain_in = schema_to_domain_group(payload)
        domain_group = create_group(domain_in)

        api_logger.info(
            "Group created",
            extra={
                "group_id": domain_group.id,
                "group_name": domain_group.group_name,
            },
        )

        return {"id": domain_group.id}

    except GroupAlreadyExists:
        api_logger.error(
            f"Unable to create group({domain_in.group_name}): Group already exists"
        )
        error_logger.error(
            f"Unable to create group({domain_in.group_name}): Group already exists"
        )
        raise HttpError(400, "Group already exists")

    except GroupCreationError:
        api_logger.error(
            f"Unable to create group({domain_in.group_name}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create group({domain_in.group_name}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("Group creation failed")
        error_logger.error("Group creation failed")
        raise HttpError(500, "Group creation error")


@group_router.put("/update/{group_id}")
def update_group_endpoint(request, group_id: int, payload: GroupIn):
    """
    The function `update_group_endpoint` updates the group specified by id.

    Endpoint:
        - **Path**: `/api/v1/groups/update/{group_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        grooup_id (int): the id of the group to update
        payload (GroupIn): a group object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the group with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_group(payload)
        update_group(group_id, domain_update)

        return {"success": True}

    except GroupAlreadyExists:
        api_logger.error(
            f"Group not updated : group namee xists ({payload.group_name})"
        )
        error_logger.error(
            f"Group not updated : group name exists ({payload.group_name})"
        )
        raise HttpError(400, "Group not updated: group name exists")

    except GroupDoesNotExist:
        api_logger.error(f"Group not updated : group id {group_id} not found")
        error_logger.error(f"Group not updated : group id {group_id} not found")
        raise HttpError(
            404, f"Group not updated : group id {group_id} not found"
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Group update error")


@group_router.get("/get/{group_id}", response=GroupOut)
def get_group_endpoint(request, group_id: int):
    """
    The function `get_group_endpoint` retrieves the group by id

    Endpoint:
        - **Path**: `/api/v1/groups/get/{group_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object
        group_id (int): The id of the group to retrieve.

    Returns:
        (GroupOut): the group object

    Raises:
        Http404: If the group with the specified ID does not exist.
    """
    try:
        group = get_group(group_id)

        return domain_group_to_schema(group)

    except GroupDoesNotExist:
        api_logger.error(f"Group not retreived : group id {group_id} not found")
        error_logger.error(
            f"Group not retreived : group id {group_id} not found"
        )
        raise HttpError(
            404, f"Group not retreived : group id {group_id} not found"
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group not retreived")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Group not retreived")


@group_router.get("/list", response=List[GroupOut])
def list_groups(request):
    """
    The function `list_groups` retrieves a list of groups,
    orderd by group name ascending.

    Endpoint:
        - **Path**: `/api/v1/groups/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (List[GroupOut]): a list of group objects
    """

    try:
        groups = get_ordered_list_of_groups()

        return [domain_group_to_schema(g) for g in groups]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@group_router.delete("/delete/{group_id}")
def delete_group_endpoint(request, group_id: int):
    """
    The function `delete_group_endpoint` deletes the group specified by id.

    Endpoint:
        - **Path**: `/api/v1/groups/delete/{group_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        group_id (int): the id of the group to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the group with the specified ID does not exist.
    """

    try:
        group = delete_group(group_id)
        api_logger.info(f"Group deleted : {group}")
        return {"success": True}
    except GroupDoesNotExist:
        api_logger.error(f"Group not deleted : group id {group_id} not found")
        error_logger.error(f"Group not deleted : group id {group_id} not found")
        raise HttpError(
            404, f"Group not deleted : group id {group_id} not found"
        )
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Group deletion error")
