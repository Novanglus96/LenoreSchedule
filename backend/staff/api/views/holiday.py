from ninja import Router
from staff.api.schemas.holiday import HolidayIn, HolidayOut
from ninja.errors import HttpError
from typing import List
import logging
from staff.exceptions import (
    HolidayAlreadyExists,
    HolidayCreationError,
    HolidayDoesNotExist,
)
from staff.mappers import (
    schema_to_domain_holiday,
    domain_holiday_to_schema,
)
from staff.services.holiday_services import (
    create_holiday,
    update_holiday,
    get_holiday,
    get_ordered_list_of_holidays,
    delete_holiday,
)

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

holiday_router = Router(tags=["Holidays"])


@holiday_router.post("/create")
def create_holiday_endpoint(request, payload: HolidayIn):
    """
    The function `create_holiday_endpoint` creats a holiday object.

    Endpoint:
        - **Path**: `/api/v1/holidays/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (HolidayIn): A holiday schema.

    Returns:
        (dict): {'id': The ID of the created holiday}.
    """
    try:
        domain_in = schema_to_domain_holiday(payload)
        domain_holiday = create_holiday(domain_in)

        api_logger.info(
            "Holiday created",
            extra={
                "holiday_id": domain_holiday.id,
                "holiday_name": domain_holiday.holiday_name,
            },
        )

        return {"id": domain_holiday.id}

    except HolidayAlreadyExists:
        api_logger.error(
            f"Unable to create holiday({domain_in.holiday_name}): Holiday already exists"
        )
        error_logger.error(
            f"Unable to create holiday({domain_in.holiday_name}): Holiday already exists"
        )
        raise HttpError(400, "Holiday already exists")

    except HolidayCreationError:
        api_logger.error(
            f"Unable to create holiday({domain_in.holiday_name}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create holiday({domain_in.holiday_name}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("Holiday creation failed")
        error_logger.error("Holiday creation failed")
        raise HttpError(500, "Holiday creation error")


@holiday_router.put("/update/{holiday_id}")
def update_holiday_endpoint(request, holiday_id: int, payload: HolidayIn):
    """
    The function `update_holiday_endpoint` updates the holiday specified by id.

    Endpoint:
        - **Path**: `/api/v1/holidays/update/{holiday_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        grooup_id (int): the id of the holiday to update
        payload (HolidayIn): a holiday object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the holiday with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_holiday(payload)
        update_holiday(holiday_id, domain_update)

        return {"success": True}

    except HolidayAlreadyExists:
        api_logger.error(
            f"Holiday not updated : holiday namee xists ({payload.holiday_name})"
        )
        error_logger.error(
            f"Holiday not updated : holiday name exists ({payload.holiday_name})"
        )
        raise HttpError(400, "Holiday not updated: holiday name exists")

    except HolidayDoesNotExist:
        api_logger.error(
            f"Holiday not updated : holiday id {holiday_id} not found"
        )
        error_logger.error(
            f"Holiday not updated : holiday id {holiday_id} not found"
        )
        raise HttpError(
            404,
            f"Holiday not updated : holiday id {holiday_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Holiday not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Holiday update error")


@holiday_router.get("/get/{holiday_id}", response=HolidayOut)
def get_holiday_endpoint(request, holiday_id: int):
    """
    The function `get_holiday_endpoint` retrieves the holiday by id

    Endpoint:
        - **Path**: `/api/v1/holidays/get/{holiday_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object
        holiday_id (int): The id of the holiday to retrieve.

    Returns:
        (HolidayOut): the holiday object

    Raises:
        Http404: If the holiday with the specified ID does not exist.
    """
    try:
        holiday = get_holiday(holiday_id)

        return domain_holiday_to_schema(holiday)

    except HolidayDoesNotExist:
        api_logger.error(
            f"Holiday not retreived : holiday id {holiday_id} not found"
        )
        error_logger.error(
            f"Holiday not retreived : holiday id {holiday_id} not found"
        )
        raise HttpError(
            404,
            f"Holiday not retreived : holiday id {holiday_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Holiday not retreived")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Holiday not retreived")


@holiday_router.get("/list", response=List[HolidayOut])
def list_holidays(request):
    """
    The function `list_holidays` retrieves a list of holidays,
    orderd by holiday name ascending.

    Endpoint:
        - **Path**: `/api/v1/holidays/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (List[HolidayOut]): a list of holiday objects
    """

    try:
        holidays = get_ordered_list_of_holidays()

        return [domain_holiday_to_schema(g) for g in holidays]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Holiday list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@holiday_router.delete("/delete/{holiday_id}")
def delete_holiday_endpoint(request, holiday_id: int):
    """
    The function `delete_holiday_endpoint` deletes the holiday specified by id.

    Endpoint:
        - **Path**: `/api/v1/holidays/delete/{holiday_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        holiday_id (int): the id of the holiday to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the holiday with the specified ID does not exist.
    """

    try:
        holiday = delete_holiday(holiday_id)
        api_logger.info(f"Holiday deleted : {holiday}")
        return {"success": True}
    except HolidayDoesNotExist:
        api_logger.error(
            f"Holiday not deleted : holiday id {holiday_id} not found"
        )
        error_logger.error(
            f"Holiday not deleted : holiday id {holiday_id} not found"
        )
        raise HttpError(
            404,
            f"Holiday not deleted : holiday id {holiday_id} not found",
        )
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Holiday not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Holiday deletion error")
