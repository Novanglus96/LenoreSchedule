from ninja import Router
from groups.models import Group
from groups.api.schemas.group import GroupIn, GroupOut
from django.db import IntegrityError
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from typing import List
import logging
from django.http import Http404

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

group_router = Router(tags=["Groups"])


@group_router.post("/create")
def create_group(request, payload: GroupIn):
    """
    The function `create_group` creats a group object.

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
        group = Group.objects.create(**payload.dict())
        api_logger.info(f"Group created : {group.group_name}")
        return {"id": group.id}
    except IntegrityError as integrity_error:
        # Check if the integrity error is due to a duplicate
        if "unique constraint" in str(integrity_error).lower():
            api_logger.error(
                f"Group not created : group exists ({payload.group_name})"
            )
            error_logger.error(
                f"Group not created : group exists ({payload.group_name})"
            )
            raise HttpError(400, "Group already exists")
        else:
            # Log other types of integry errors
            api_logger.error("Group not created : db integrity error")
            error_logger.error("Group not created : db integrity error")
            raise HttpError(400, "DB integrity error")
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group not created")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record creation error")


@group_router.put("/update/{group_id}")
def update_group(request, group_id: int, payload: GroupIn):
    """
    The function `update_group` updates the group specified by id.

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
        group = get_object_or_404(Group, id=group_id)
        group.group_name = payload.group_name
        group.save()
        api_logger.info(f"Group updated : {group.group_name}")
        return {"success": True}
    except IntegrityError as integrity_error:
        # Check if the integrity error is due to a duplicate
        if "unique constraint" in str(integrity_error).lower():
            api_logger.error(
                f"Group not updated : group exists ({payload.group_name})"
            )
            error_logger.error(
                f"Group not updated : group exists ({payload.group_name})"
            )
            raise HttpError(400, "Group already exists")
        else:
            # Log other types of integry errors
            api_logger.error("Group not updated : db integrity error")
            error_logger.error("Group not updated : db integrity error")
            raise HttpError(400, "DB integrity error")
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record update error")


@group_router.get("/get/{group_id}", response=GroupOut)
def get_group(request, group_id: int):
    """
    The function `get_group` retrieves the group by id

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
        group = get_object_or_404(Group, id=group_id)
        api_logger.debug(f"Group retrieved : {group.group_name}")
        return group
    except Http404:
        raise
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


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
        qs = Group.objects.all().order_by("group_name")
        api_logger.debug("Group list retrieved")
        return qs
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@group_router.delete("/delete/{group_id}")
def delete_group(request, group_id: int):
    """
    The function `delete_group` deletes the group specified by id.

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
        group = get_object_or_404(Group, id=group_id)
        group_name = group.group_name
        group.delete()
        api_logger.info(f"Group deleted : {group_name}")
        return {"success": True}
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Group not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")
