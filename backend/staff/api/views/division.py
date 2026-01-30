from ninja import Router
from staff.api.schemas.division import DivisionIn, DivisionOut
from ninja.errors import HttpError
from typing import List
import logging
from staff.exceptions import (
    DivisionAlreadyExists,
    DivisionCreationError,
    DivisionDoesNotExist,
)
from staff.mappers import (
    schema_to_domain_division,
    domain_division_to_schema,
)
from staff.services.division_services import (
    create_division,
    update_division,
    get_division,
    get_ordered_list_of_divisions,
    delete_division,
)

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

division_router = Router(tags=["Divisions"])


@division_router.post("/create")
def create_division_endpoint(request, payload: DivisionIn):
    """
    The function `create_division_endpoint` creats a division object.

    Endpoint:
        - **Path**: `/api/v1/divisions/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (DivisionIn): A division schema.

    Returns:
        (dict): {'id': The ID of the created division}.
    """
    try:
        domain_in = schema_to_domain_division(payload)
        domain_division = create_division(domain_in)

        api_logger.info(
            "Division created",
            extra={
                "division_id": domain_division.id,
                "division_name": domain_division.division_name,
            },
        )

        return {"id": domain_division.id}

    except DivisionAlreadyExists:
        api_logger.error(
            f"Unable to create division({domain_in.division_name}): Division already exists"
        )
        error_logger.error(
            f"Unable to create division({domain_in.division_name}): Division already exists"
        )
        raise HttpError(400, "Division already exists")

    except DivisionCreationError:
        api_logger.error(
            f"Unable to create division({domain_in.division_name}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create division({domain_in.division_name}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("Division creation failed")
        error_logger.error("Division creation failed")
        raise HttpError(500, "Division creation error")


@division_router.put("/update/{division_id}")
def update_division_endpoint(request, division_id: int, payload: DivisionIn):
    """
    The function `update_division_endpoint` updates the division specified by id.

    Endpoint:
        - **Path**: `/api/v1/divisions/update/{division_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        grooup_id (int): the id of the division to update
        payload (DivisionIn): a division object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the division with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_division(payload)
        update_division(division_id, domain_update)

        return {"success": True}

    except DivisionAlreadyExists:
        api_logger.error(
            f"Division not updated : division namee xists ({payload.division_name})"
        )
        error_logger.error(
            f"Division not updated : division name exists ({payload.division_name})"
        )
        raise HttpError(400, "Division not updated: division name exists")

    except DivisionDoesNotExist:
        api_logger.error(
            f"Division not updated : division id {division_id} not found"
        )
        error_logger.error(
            f"Division not updated : division id {division_id} not found"
        )
        raise HttpError(
            404,
            f"Division not updated : division id {division_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Division not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Division update error")


@division_router.get("/get/{division_id}", response=DivisionOut)
def get_division_endpoint(request, division_id: int):
    """
    The function `get_division_endpoint` retrieves the division by id

    Endpoint:
        - **Path**: `/api/v1/divisions/get/{division_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object
        division_id (int): The id of the division to retrieve.

    Returns:
        (DivisionOut): the division object

    Raises:
        Http404: If the division with the specified ID does not exist.
    """
    try:
        division = get_division(division_id)

        return domain_division_to_schema(division)

    except DivisionDoesNotExist:
        api_logger.error(
            f"Division not retreived : division id {division_id} not found"
        )
        error_logger.error(
            f"Division not retreived : division id {division_id} not found"
        )
        raise HttpError(
            404,
            f"Division not retreived : division id {division_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Division not retreived")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Division not retreived")


@division_router.get("/list", response=List[DivisionOut])
def list_divisions(request):
    """
    The function `list_divisions` retrieves a list of divisions,
    orderd by division name ascending.

    Endpoint:
        - **Path**: `/api/v1/divisions/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (List[DivisionOut]): a list of division objects
    """

    try:
        divisions = get_ordered_list_of_divisions()

        return [domain_division_to_schema(g) for g in divisions]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Division list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@division_router.delete("/delete/{division_id}")
def delete_division_endpoint(request, division_id: int):
    """
    The function `delete_division_endpoint` deletes the division specified by id.

    Endpoint:
        - **Path**: `/api/v1/divisions/delete/{division_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        division_id (int): the id of the division to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the division with the specified ID does not exist.
    """

    try:
        division = delete_division(division_id)
        api_logger.info(f"Division deleted : {division}")
        return {"success": True}
    except DivisionDoesNotExist:
        api_logger.error(
            f"Division not deleted : division id {division_id} not found"
        )
        error_logger.error(
            f"Division not deleted : division id {division_id} not found"
        )
        raise HttpError(
            404,
            f"Division not deleted : division id {division_id} not found",
        )
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Division not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Division deletion error")
