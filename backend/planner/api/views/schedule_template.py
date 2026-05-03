from ninja import Router
from planner.api.schemas.schedule_template import ScheduleTemplateIn, ScheduleTemplateOut
from ninja.errors import HttpError
from typing import List
import logging
from planner.exceptions import (
    ScheduleTemplateCreationError,
    ScheduleTemplateDoesNotExist,
    ScheduleTemplateInvalidDayOfWeek,
    ScheduleTemplateInvalidTimeRange,
)
from planner.mappers import (
    schema_to_domain_schedule_template,
    domain_schedule_template_to_schema,
)
from planner.services.schedule_template_services import (
    create_schedule_template,
    update_schedule_template,
    get_schedule_template,
    get_schedule_templates_for_employee,
    get_all_schedule_templates,
    delete_schedule_template,
)
from staff.services.employee_services import get_employee
from staff.exceptions import EmployeeDoesNotExist
from core.utils.auth import get_user_divisions

api_logger = logging.getLogger("api")
error_logger = logging.getLogger("error")

schedule_template_router = Router(tags=["ScheduleTemplates"])


@schedule_template_router.post("/create")
def create_schedule_template_endpoint(request, payload: ScheduleTemplateIn):
    """
    The function `create_schedule_template_endpoint` creates a schedule_template object.

    Endpoint:
        - **Path**: `/api/v1/schedule_templates/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (ScheduleTemplateIn): A schedule_template schema.

    Returns:
        (dict): {'id': The ID of the created schedule_template}.
    """
    try:
        domain_in = schema_to_domain_schedule_template(payload)
        domain_template = create_schedule_template(domain_in)

        api_logger.info(
            "ScheduleTemplate created",
            extra={"schedule_template_id": domain_template.id},
        )

        return {"id": domain_template.id}

    except ScheduleTemplateInvalidDayOfWeek:
        api_logger.error("Unable to create schedule_template: invalid day_of_week")
        error_logger.error("Unable to create schedule_template: invalid day_of_week")
        raise HttpError(400, "Invalid day_of_week: must be 0 (Monday) through 6 (Sunday)")

    except ScheduleTemplateInvalidTimeRange:
        api_logger.error("Unable to create schedule_template: start_time must be before end_time")
        error_logger.error("Unable to create schedule_template: start_time must be before end_time")
        raise HttpError(400, "Invalid time range: start_time must be before end_time")

    except ScheduleTemplateCreationError:
        api_logger.error("Unable to create schedule_template: DB integrity error")
        error_logger.error("Unable to create schedule_template: DB integrity error")
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("ScheduleTemplate creation failed")
        error_logger.error("ScheduleTemplate creation failed")
        raise HttpError(500, "ScheduleTemplate creation error")


@schedule_template_router.put("/update/{schedule_template_id}")
def update_schedule_template_endpoint(
    request, schedule_template_id: int, payload: ScheduleTemplateIn
):
    """
    The function `update_schedule_template_endpoint` updates the schedule_template
    specified by id.

    Endpoint:
        - **Path**: `/api/v1/schedule_templates/update/{schedule_template_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        schedule_template_id (int): The id of the schedule_template to update.
        payload (ScheduleTemplateIn): A schedule_template schema.

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the schedule_template with the specified ID does not exist.
    """
    try:
        domain_update = schema_to_domain_schedule_template(payload)
        update_schedule_template(schedule_template_id, domain_update)

        return {"success": True}

    except ScheduleTemplateDoesNotExist:
        api_logger.error(
            f"ScheduleTemplate not updated: id {schedule_template_id} not found"
        )
        error_logger.error(
            f"ScheduleTemplate not updated: id {schedule_template_id} not found"
        )
        raise HttpError(
            404,
            f"ScheduleTemplate not updated: id {schedule_template_id} not found",
        )

    except ScheduleTemplateInvalidDayOfWeek:
        api_logger.error(
            f"ScheduleTemplate not updated: invalid day_of_week for id {schedule_template_id}"
        )
        error_logger.error(
            f"ScheduleTemplate not updated: invalid day_of_week for id {schedule_template_id}"
        )
        raise HttpError(400, "Invalid day_of_week: must be 0 (Monday) through 6 (Sunday)")

    except ScheduleTemplateInvalidTimeRange:
        api_logger.error(
            f"ScheduleTemplate not updated: invalid time range for id {schedule_template_id}"
        )
        error_logger.error(
            f"ScheduleTemplate not updated: invalid time range for id {schedule_template_id}"
        )
        raise HttpError(400, "Invalid time range: start_time must be before end_time")

    except Exception as e:
        api_logger.error("ScheduleTemplate not updated")
        error_logger.error(str(e))
        raise HttpError(500, "ScheduleTemplate update error")


@schedule_template_router.get("/get/{schedule_template_id}", response=ScheduleTemplateOut)
def get_schedule_template_endpoint(request, schedule_template_id: int):
    """
    The function `get_schedule_template_endpoint` retrieves the schedule_template by id.

    Endpoint:
        - **Path**: `/api/v1/schedule_templates/get/{schedule_template_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.
        schedule_template_id (int): The id of the schedule_template to retrieve.

    Returns:
        (ScheduleTemplateOut): The schedule_template object.

    Raises:
        Http404: If the schedule_template with the specified ID does not exist.
    """
    try:
        template = get_schedule_template(schedule_template_id)
        return domain_schedule_template_to_schema(template)

    except ScheduleTemplateDoesNotExist:
        api_logger.error(
            f"ScheduleTemplate not retrieved: id {schedule_template_id} not found"
        )
        error_logger.error(
            f"ScheduleTemplate not retrieved: id {schedule_template_id} not found"
        )
        raise HttpError(
            404,
            f"ScheduleTemplate not retrieved: id {schedule_template_id} not found",
        )

    except Exception as e:
        api_logger.error("ScheduleTemplate not retrieved")
        error_logger.error(str(e))
        raise HttpError(500, "ScheduleTemplate not retrieved")


@schedule_template_router.get("/list", response=List[ScheduleTemplateOut])
def list_all_schedule_templates(request):
    """
    Returns all schedule templates ordered by employee name, day, and time.

    Endpoint:
        - **Path**: `/api/v1/schedule_templates/list`
        - **Method**: `GET`
    """
    try:
        templates = get_all_schedule_templates()
        return [domain_schedule_template_to_schema(t) for t in templates]
    except Exception as e:
        api_logger.error("ScheduleTemplates not retrieved")
        error_logger.error(str(e))
        raise HttpError(500, "ScheduleTemplates not retrieved")


@schedule_template_router.get(
    "/employee/{employee_id}", response=List[ScheduleTemplateOut]
)
def list_schedule_templates_for_employee(request, employee_id: int):
    """
    The function `list_schedule_templates_for_employee` retrieves all schedule
    template blocks for an employee, ordered by day_of_week then start_time.

    Endpoint:
        - **Path**: `/api/v1/schedule_templates/employee/{employee_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.
        employee_id (int): The id of the employee.

    Returns:
        (List[ScheduleTemplateOut]): A list of schedule_template objects.
    """
    try:
        get_employee(employee_id, divisions=get_user_divisions(request))
        templates = get_schedule_templates_for_employee(employee_id)
        return [domain_schedule_template_to_schema(t) for t in templates]

    except EmployeeDoesNotExist:
        api_logger.error(
            f"ScheduleTemplates not retrieved: employee {employee_id} not found"
        )
        error_logger.error(
            f"ScheduleTemplates not retrieved: employee {employee_id} not found"
        )
        raise HttpError(404, f"Employee {employee_id} not found")

    except Exception as e:
        api_logger.error(f"ScheduleTemplates for employee {employee_id} not retrieved")
        error_logger.error(str(e))
        raise HttpError(500, "ScheduleTemplates not retrieved")


@schedule_template_router.delete("/delete/{schedule_template_id}")
def delete_schedule_template_endpoint(request, schedule_template_id: int):
    """
    The function `delete_schedule_template_endpoint` deletes the schedule_template
    specified by id.

    Endpoint:
        - **Path**: `/api/v1/schedule_templates/delete/{schedule_template_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        schedule_template_id (int): The id of the schedule_template to delete.

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the schedule_template with the specified ID does not exist.
    """
    try:
        deleted = delete_schedule_template(schedule_template_id)
        api_logger.info(f"ScheduleTemplate deleted: {deleted}")
        return {"success": True}

    except ScheduleTemplateDoesNotExist:
        api_logger.error(
            f"ScheduleTemplate not deleted: id {schedule_template_id} not found"
        )
        error_logger.error(
            f"ScheduleTemplate not deleted: id {schedule_template_id} not found"
        )
        raise HttpError(
            404,
            f"ScheduleTemplate not deleted: id {schedule_template_id} not found",
        )

    except Exception as e:
        api_logger.error("ScheduleTemplate not deleted")
        error_logger.error(str(e))
        raise HttpError(500, "ScheduleTemplate deletion error")
