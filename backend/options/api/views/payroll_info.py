from ninja import Router
from options.api.schemas.payroll_info import PayrollInfoIn, PayrollInfoOut, PayrollWeekOut
from ninja.errors import HttpError
from typing import List
import logging
from options.exceptions import (
    PayrollInfoAlreadyExists,
    PayrollInfoCreationError,
    PayrollInfoDoesNotExist,
    PayrollInfoInvalidFirstDay,
    PayrollInfoInvalidFrequencyError,
    PayrollInfoInvalidSecondDay,
    PayrollInfoInvalidStart,
)
from options.mappers import (
    schema_to_domain_payroll_info,
    domain_payroll_info_to_schema,
)
from options.services.payroll_services import (
    create_payroll_info,
    update_payroll_info,
    get_payroll_info,
    get_ordered_list_of_payroll_infos,
    delete_payroll_info,
    get_payroll_weeks,
)

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

payroll_info_router = Router(tags=["PayrollInfos"])


@payroll_info_router.post("/create")
def create_payroll_info_endpoint(request, payload: PayrollInfoIn):
    """
    The function `create_payroll_info_endpoint` creates a payroll_info object.

    Endpoint:
        - **Path**: `/api/v1/options/payroll_infos/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (PayrollInfoIn): A payroll_info schema.

    Returns:
        (dict): {'id': The ID of the created payroll_info}.
    """
    try:
        domain_in = schema_to_domain_payroll_info(payload)
        domain_payroll_info = create_payroll_info(domain_in)

        api_logger.info(
            "PayrollInfo created",
            extra={
                "payroll_info_id": domain_payroll_info.id,
                "payroll_info_year": domain_payroll_info.payroll_year,
            },
        )

        return {"id": domain_payroll_info.id}

    except PayrollInfoAlreadyExists:
        api_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): PayrollInfo already exists"
        )
        error_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): PayrollInfo already exists"
        )
        raise HttpError(400, "PayrollInfo already exists")

    except PayrollInfoInvalidFrequencyError:
        api_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid payroll frequency"
        )
        error_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid payroll frequency"
        )
        raise HttpError(400, "Invalid payroll frequency")

    except PayrollInfoInvalidStart:
        api_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid payroll start date"
        )
        error_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid payroll start date"
        )
        raise HttpError(400, "Invalid payroll start date")

    except PayrollInfoInvalidFirstDay:
        api_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid first day"
        )
        error_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid first day"
        )
        raise HttpError(400, "Invalid first day")

    except PayrollInfoInvalidSecondDay:
        api_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid second day"
        )
        error_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): Invalid second day"
        )
        raise HttpError(400, "Invalid second day")

    except PayrollInfoCreationError:
        api_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create payroll_info({domain_in.payroll_year}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("PayrollInfo creation failed")
        error_logger.error("PayrollInfo creation failed")
        raise HttpError(500, "PayrollInfo creation error")


@payroll_info_router.put("/update/{payroll_info_id}")
def update_payroll_info_endpoint(
    request, payroll_info_id: int, payload: PayrollInfoIn
):
    """
    The function `update_payroll_info_endpoint` updates the payroll_info specified by id.

    Endpoint:
        - **Path**: `/api/v1/options/payroll_infos/update/{payroll_info_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        payroll_info_id (int): the id of the payroll_info to update
        payload (PayrollInfoIn): a payroll_info object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the payroll_info with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_payroll_info(payload)
        update_payroll_info(payroll_info_id, domain_update)

        return {"success": True}

    except PayrollInfoAlreadyExists:
        api_logger.error(
            f"PayrollInfo not updated: payroll year {payload.payroll_year} already exists"
        )
        error_logger.error(
            f"PayrollInfo not updated: payroll year {payload.payroll_year} already exists"
        )
        raise HttpError(400, "PayrollInfo not updated: payroll year already exists")

    except PayrollInfoDoesNotExist:
        api_logger.error(
            f"PayrollInfo not updated: payroll_info id {payroll_info_id} not found"
        )
        error_logger.error(
            f"PayrollInfo not updated: payroll_info id {payroll_info_id} not found"
        )
        raise HttpError(
            404,
            f"PayrollInfo not updated: payroll_info id {payroll_info_id} not found",
        )

    except PayrollInfoInvalidFirstDay:
        api_logger.error(
            f"PayrollInfo not updated: invalid first day for payroll_info id {payroll_info_id}"
        )
        error_logger.error(
            f"PayrollInfo not updated: invalid first day for payroll_info id {payroll_info_id}"
        )
        raise HttpError(400, "Invalid first day")

    except PayrollInfoInvalidSecondDay:
        api_logger.error(
            f"PayrollInfo not updated: invalid second day for payroll_info id {payroll_info_id}"
        )
        error_logger.error(
            f"PayrollInfo not updated: invalid second day for payroll_info id {payroll_info_id}"
        )
        raise HttpError(400, "Invalid second day")

    except Exception as e:
        api_logger.error("PayrollInfo not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "PayrollInfo update error")


@payroll_info_router.get("/get/{payroll_info_id}", response=PayrollInfoOut)
def get_payroll_info_endpoint(request, payroll_info_id: int):
    """
    The function `get_payroll_info_endpoint` retrieves the payroll_info by id.

    Endpoint:
        - **Path**: `/api/v1/options/payroll_infos/get/{payroll_info_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object
        payroll_info_id (int): The id of the payroll_info to retrieve.

    Returns:
        (PayrollInfoOut): the payroll_info object

    Raises:
        Http404: If the payroll_info with the specified ID does not exist.
    """
    try:
        payroll_info = get_payroll_info(payroll_info_id)

        return domain_payroll_info_to_schema(payroll_info)

    except PayrollInfoDoesNotExist:
        api_logger.error(
            f"PayrollInfo not retrieved: payroll_info id {payroll_info_id} not found"
        )
        error_logger.error(
            f"PayrollInfo not retrieved: payroll_info id {payroll_info_id} not found"
        )
        raise HttpError(
            404,
            f"PayrollInfo not retrieved: payroll_info id {payroll_info_id} not found",
        )

    except Exception as e:
        api_logger.error("PayrollInfo not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "PayrollInfo not retrieved")


@payroll_info_router.get("/list", response=List[PayrollInfoOut])
def list_payroll_infos(request):
    """
    The function `list_payroll_infos` retrieves a list of payroll_infos,
    ordered by payroll_year descending.

    Endpoint:
        - **Path**: `/api/v1/options/payroll_infos/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (List[PayrollInfoOut]): a list of payroll_info objects
    """

    try:
        payroll_infos = get_ordered_list_of_payroll_infos()

        return [domain_payroll_info_to_schema(g) for g in payroll_infos]
    except Exception as e:
        api_logger.error("PayrollInfo list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@payroll_info_router.delete("/delete/{payroll_info_id}")
def delete_payroll_info_endpoint(request, payroll_info_id: int):
    """
    The function `delete_payroll_info_endpoint` deletes the payroll_info specified by id.

    Endpoint:
        - **Path**: `/api/v1/options/payroll_infos/delete/{payroll_info_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        payroll_info_id (int): the id of the payroll_info to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the payroll_info with the specified ID does not exist.
    """

    try:
        payroll_info = delete_payroll_info(payroll_info_id)
        api_logger.info(f"PayrollInfo deleted: {payroll_info}")
        return {"success": True}
    except PayrollInfoDoesNotExist:
        api_logger.error(
            f"PayrollInfo not deleted: payroll_info id {payroll_info_id} not found"
        )
        error_logger.error(
            f"PayrollInfo not deleted: payroll_info id {payroll_info_id} not found"
        )
        raise HttpError(
            404,
            f"PayrollInfo not deleted: payroll_info id {payroll_info_id} not found",
        )
    except Exception as e:
        api_logger.error("PayrollInfo not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "PayrollInfo deletion error")


@payroll_info_router.get("/{payroll_year}/weeks", response=List[PayrollWeekOut])
def list_payroll_weeks(request, payroll_year: int):
    """
    Returns all 7-day weeks for a payroll year with labels and page indices.

    Endpoint:
        - **Path**: `/api/v1/options/payroll_infos/{payroll_year}/weeks`
        - **Method**: `GET`

    Args:
        payroll_year (int): The payroll year to list weeks for.

    Returns:
        List[PayrollWeekOut]: Ordered list of weeks with page, week_start, week_end, label.
    """
    try:
        return get_payroll_weeks(payroll_year)
    except PayrollInfoDoesNotExist:
        raise HttpError(404, f"No payroll info found for year {payroll_year}")
    except Exception as e:
        api_logger.error("Payroll weeks not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Payroll weeks not retrieved")
