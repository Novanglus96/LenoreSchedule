from ninja import Router
from planner.api.schemas.calendar_entry import (
    CalendarEntryIn,
    CalendarEntryOut,
    ConfirmWeekIn,
)
from ninja.errors import HttpError
from typing import List
import logging
from planner.exceptions import (
    CalendarEntryAlreadyExists,
    CalendarEntryCreationError,
    CalendarEntryDoesNotExist,
)
from planner.mappers import (
    schema_to_domain_calendar_entry,
    domain_calendar_entry_to_schema,
)
from planner.services.calendar_services import (
    create_calendar_entry,
    update_calendar_entry,
    get_calendar,
    delete_calendar_entry,
    confirm_week_entries,
)
from core.utils.auth import get_user_divisions

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

calendar_entry_router = Router(tags=["CalendarEntrys"])


@calendar_entry_router.post("/create_entry")
def create_calendar_entry_endpoint(request, payload: CalendarEntryIn):
    """
    The function `create_calendar_entry_endpoint` creats a calendar_entry object.

    Endpoint:
        - **Path**: `/api/v1/calendar/create_entry`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (CalendarEntryIn): A calendar_entry schema.

    Returns:
        (dict): {'id': The ID of the created calendar_entry}.
    """
    try:
        domain_in = schema_to_domain_calendar_entry(payload)
        domain_calendar_entry = create_calendar_entry(domain_in)

        api_logger.info(
            "CalendarEntry created",
            extra={
                "calendar_entry_id": domain_calendar_entry.id,
            },
        )

        return {"id": domain_calendar_entry.id}

    except CalendarEntryAlreadyExists:
        api_logger.error(
            f"Unable to create calendar_entry({domain_in.calendar_date}): CalendarEntry already exists"
        )
        error_logger.error(
            f"Unable to create calendar_entry({domain_in.calendar_date}): CalendarEntry already exists"
        )
        raise HttpError(400, "CalendarEntry already exists")

    except CalendarEntryCreationError:
        api_logger.error(
            f"Unable to create calendar_entry({domain_in.calendar_date}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create calendar_entry({domain_in.calendar_date}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("CalendarEntry creation failed")
        error_logger.error("CalendarEntry creation failed")
        raise HttpError(500, "CalendarEntry creation error")


@calendar_entry_router.put("/update_entry/{calendar_entry_id}")
def update_calendar_entry_endpoint(
    request, calendar_entry_id: int, payload: CalendarEntryIn
):
    """
    The function `update_calendar_entry_endpoint` updates the calendar_entry specified by id.

    Endpoint:
        - **Path**: `/api/v1/calendar/update_entry/{calendar_entry_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        calendar_entry_id (int): the id of the calendar_entry to update
        payload (CalendarEntryIn): a calendar_entry object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the calendar_entry with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_calendar_entry(payload)
        update_calendar_entry(calendar_entry_id, domain_update)

        return {"success": True}

    except CalendarEntryAlreadyExists:
        api_logger.error(
            "CalendarEntry not updated : calendar_entry already exists"
        )
        error_logger.error(
            "CalendarEntry not updated : calendar_entry already exists"
        )
        raise HttpError(
            400, "CalendarEntry not updated: calendar_entry already exists"
        )

    except CalendarEntryDoesNotExist:
        api_logger.error(
            f"CalendarEntry not updated : calendar_entry id {calendar_entry_id} not found"
        )
        error_logger.error(
            f"CalendarEntry not updated : calendar_entry id {calendar_entry_id} not found"
        )
        raise HttpError(
            404,
            f"CalendarEntry not updated : calendar_entry id {calendar_entry_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("CalendarEntry not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "CalendarEntry update error")


@calendar_entry_router.get("/view/{timeframe}", response=List[CalendarEntryOut])
def list_calendar_entries(request, timeframe: str):
    """
    The function `list_calendar_entries` retrieves a list of calendar_entries,
    orderd by calendar_date.

    Endpoint:
        - **Path**: `/api/v1/calendar/view/{timeframe}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.
        timeframe (str): last/current/next

    Returns:
        (List[CalendarEntryOut]): a list of calendar_entry objects
    """

    try:
        calendar_entries = get_calendar(timeframe, divisions=get_user_divisions(request))
        return [domain_calendar_entry_to_schema(g) for g in calendar_entries]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Calendar not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Calendar not retrieved")


@calendar_entry_router.get(
    "/view_by_employee/{employee_id}/{timeframe}",
    response=List[CalendarEntryOut],
)
def list_calendar_entries_by_employee(
    request, employee_id: int, timeframe: str
):
    """
    The function `list_calendar_entries_by_employee` retrieves a list of calendar_entries,
    for an employee orderd by calendar_date.

    Endpoint:
        - **Path**: `/api/v1/calendar/view_by_employee/{employee_id}/{timeframe}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.
        timeframe (str): last/current/next

    Returns:
        (List[CalendarEntryOut]): a list of calendar_entry objects
    """

    try:
        calendar_entries = get_calendar(
            timeframe, employee_id, divisions=get_user_divisions(request)
        )

        return [domain_calendar_entry_to_schema(g) for g in calendar_entries]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Employee calendar not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Employee calendar not retrieved")


@calendar_entry_router.post("/confirm_week")
def confirm_week_endpoint(request, payload: ConfirmWeekIn):
    """
    Bulk-confirms all unconfirmed calendar entries for an employee for a given
    week range.

    Endpoint:
        - **Path**: `/api/v1/calendar/confirm_week`
        - **Method**: `POST`

    Args:
        payload (ConfirmWeekIn): employee_id, week_start, week_end.

    Returns:
        (dict): {'confirmed': count of entries updated}
    """
    try:
        count = confirm_week_entries(payload.employee_id, payload.week_start, payload.week_end)
        api_logger.info(f"Confirmed {count} entries for employee {payload.employee_id}")
        return {"confirmed": count}
    except Exception as e:
        api_logger.error("Confirm week failed")
        error_logger.error(str(e))
        raise HttpError(500, "Confirm week failed")


@calendar_entry_router.delete("/delete_entry/{calendar_entry_id}")
def delete_calendar_entry_endpoint(request, calendar_entry_id: int):
    """
    The function `delete_calendar_entry_endpoint` deletes the calendar_entry specified by id.

    Endpoint:
        - **Path**: `/api/v1/calendar/delete_entry/{calendar_entry_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        calendar_entry_id (int): the id of the calendar_entry to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the calendar_entry with the specified ID does not exist.
    """

    try:
        calendar_entry = delete_calendar_entry(calendar_entry_id)
        api_logger.info(f"CalendarEntry deleted : {calendar_entry}")
        return {"success": True}
    except CalendarEntryDoesNotExist:
        api_logger.error(
            f"CalendarEntry not deleted : calendar_entry id {calendar_entry_id} not found"
        )
        error_logger.error(
            f"CalendarEntry not deleted : calendar_entry id {calendar_entry_id} not found"
        )
        raise HttpError(
            404,
            f"CalendarEntry not deleted : calendar_entry id {calendar_entry_id} not found",
        )
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("CalendarEntry not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "CalendarEntry deletion error")
