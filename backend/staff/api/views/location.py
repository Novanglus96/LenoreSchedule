from ninja import Router
from staff.api.schemas.location import LocationIn, LocationOut
from ninja.errors import HttpError
from typing import List
import logging
from staff.exceptions import (
    LocationAlreadyExists,
    LocationCreationError,
    LocationDoesNotExist,
)
from staff.mappers import (
    schema_to_domain_location,
    domain_location_to_schema,
)
from staff.services.location_services import (
    create_location,
    update_location,
    get_location,
    get_ordered_list_of_locations,
    delete_location,
)

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

location_router = Router(tags=["Locations"])


@location_router.post("/create")
def create_location_endpoint(request, payload: LocationIn):
    """
    The function `create_location_endpoint` creats a location object.

    Endpoint:
        - **Path**: `/api/v1/locations/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (LocationIn): A location schema.

    Returns:
        (dict): {'id': The ID of the created location}.
    """
    try:
        domain_in = schema_to_domain_location(payload)
        domain_location = create_location(domain_in)

        api_logger.info(
            "Location created",
            extra={
                "location_id": domain_location.id,
                "location_name": domain_location.location_name,
            },
        )

        return {"id": domain_location.id}

    except LocationAlreadyExists:
        api_logger.error(
            f"Unable to create location({domain_in.location_name}): Location already exists"
        )
        error_logger.error(
            f"Unable to create location({domain_in.location_name}): Location already exists"
        )
        raise HttpError(400, "Location already exists")

    except LocationCreationError:
        api_logger.error(
            f"Unable to create location({domain_in.location_name}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create location({domain_in.location_name}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("Location creation failed")
        error_logger.error("Location creation failed")
        raise HttpError(500, "Location creation error")


@location_router.put("/update/{location_id}")
def update_location_endpoint(request, location_id: int, payload: LocationIn):
    """
    The function `update_location_endpoint` updates the location specified by id.

    Endpoint:
        - **Path**: `/api/v1/locations/update/{location_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        grooup_id (int): the id of the location to update
        payload (LocationIn): a location object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the location with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_location(payload)
        update_location(location_id, domain_update)

        return {"success": True}

    except LocationAlreadyExists:
        api_logger.error(
            f"Location not updated : location namee xists ({payload.location_name})"
        )
        error_logger.error(
            f"Location not updated : location name exists ({payload.location_name})"
        )
        raise HttpError(400, "Location not updated: location name exists")

    except LocationDoesNotExist:
        api_logger.error(
            f"Location not updated : location id {location_id} not found"
        )
        error_logger.error(
            f"Location not updated : location id {location_id} not found"
        )
        raise HttpError(
            404,
            f"Location not updated : location id {location_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Location not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Location update error")


@location_router.get("/get/{location_id}", response=LocationOut)
def get_location_endpoint(request, location_id: int):
    """
    The function `get_location_endpoint` retrieves the location by id

    Endpoint:
        - **Path**: `/api/v1/locations/get/{location_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object
        location_id (int): The id of the location to retrieve.

    Returns:
        (LocationOut): the location object

    Raises:
        Http404: If the location with the specified ID does not exist.
    """
    try:
        location = get_location(location_id)

        return domain_location_to_schema(location)

    except LocationDoesNotExist:
        api_logger.error(
            f"Location not retreived : location id {location_id} not found"
        )
        error_logger.error(
            f"Location not retreived : location id {location_id} not found"
        )
        raise HttpError(
            404,
            f"Location not retreived : location id {location_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Location not retreived")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Location not retreived")


@location_router.get("/list", response=List[LocationOut])
def list_locations(request):
    """
    The function `list_locations` retrieves a list of locations,
    orderd by location name ascending.

    Endpoint:
        - **Path**: `/api/v1/locations/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (List[LocationOut]): a list of location objects
    """

    try:
        locations = get_ordered_list_of_locations()

        return [domain_location_to_schema(g) for g in locations]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Location list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@location_router.delete("/delete/{location_id}")
def delete_location_endpoint(request, location_id: int):
    """
    The function `delete_location_endpoint` deletes the location specified by id.

    Endpoint:
        - **Path**: `/api/v1/locations/delete/{location_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        location_id (int): the id of the location to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the location with the specified ID does not exist.
    """

    try:
        location = delete_location(location_id)
        api_logger.info(f"Location deleted : {location}")
        return {"success": True}
    except LocationDoesNotExist:
        api_logger.error(
            f"Location not deleted : location id {location_id} not found"
        )
        error_logger.error(
            f"Location not deleted : location id {location_id} not found"
        )
        raise HttpError(
            404,
            f"Location not deleted : location id {location_id} not found",
        )
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Location not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Location deletion error")
