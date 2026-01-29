from ninja import Router
from staff.api.schemas.department import DepartmentIn, DepartmentOut
from ninja.errors import HttpError
from typing import List
import logging
from staff.exceptions import (
    DepartmentAlreadyExists,
    DepartmentCreationError,
    DepartmentDoesNotExist,
)
from staff.mappers import (
    schema_to_domain_department,
    domain_department_to_schema,
)
from staff.services.department_services import (
    create_department,
    update_department,
    get_department,
    get_ordered_list_of_departments,
    delete_department,
)

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

department_router = Router(tags=["Departments"])


@department_router.post("/create")
def create_department_endpoint(request, payload: DepartmentIn):
    """
    The function `create_department_endpoint` creats a department object.

    Endpoint:
        - **Path**: `/api/v1/departments/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (DepartmentIn): A department schema.

    Returns:
        (dict): {'id': The ID of the created department}.
    """
    try:
        domain_in = schema_to_domain_department(payload)
        domain_department = create_department(domain_in)

        api_logger.info(
            "Department created",
            extra={
                "department_id": domain_department.id,
                "department_name": domain_department.department_name,
            },
        )

        return {"id": domain_department.id}

    except DepartmentAlreadyExists:
        api_logger.error(
            f"Unable to create department({domain_in.department_name}): Department already exists"
        )
        error_logger.error(
            f"Unable to create department({domain_in.department_name}): Department already exists"
        )
        raise HttpError(400, "Department already exists")

    except DepartmentCreationError:
        api_logger.error(
            f"Unable to create department({domain_in.department_name}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create department({domain_in.department_name}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("Department creation failed")
        error_logger.error("Department creation failed")
        raise HttpError(500, "Department creation error")


@department_router.put("/update/{department_id}")
def update_department_endpoint(
    request, department_id: int, payload: DepartmentIn
):
    """
    The function `update_department_endpoint` updates the department specified by id.

    Endpoint:
        - **Path**: `/api/v1/departments/update/{department_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        grooup_id (int): the id of the department to update
        payload (DepartmentIn): a department object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the department with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_department(payload)
        update_department(department_id, domain_update)

        return {"success": True}

    except DepartmentAlreadyExists:
        api_logger.error(
            f"Department not updated : department namee xists ({payload.department_name})"
        )
        error_logger.error(
            f"Department not updated : department name exists ({payload.department_name})"
        )
        raise HttpError(400, "Department not updated: department name exists")

    except DepartmentDoesNotExist:
        api_logger.error(
            f"Department not updated : department id {department_id} not found"
        )
        error_logger.error(
            f"Department not updated : department id {department_id} not found"
        )
        raise HttpError(
            404,
            f"Department not updated : department id {department_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Department not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Department update error")


@department_router.get("/get/{department_id}", response=DepartmentOut)
def get_department_endpoint(request, department_id: int):
    """
    The function `get_department_endpoint` retrieves the department by id

    Endpoint:
        - **Path**: `/api/v1/departments/get/{department_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object
        department_id (int): The id of the department to retrieve.

    Returns:
        (DepartmentOut): the department object

    Raises:
        Http404: If the department with the specified ID does not exist.
    """
    try:
        department = get_department(department_id)

        return domain_department_to_schema(department)

    except DepartmentDoesNotExist:
        api_logger.error(
            f"Department not retreived : department id {department_id} not found"
        )
        error_logger.error(
            f"Department not retreived : department id {department_id} not found"
        )
        raise HttpError(
            404,
            f"Department not retreived : department id {department_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Department not retreived")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Department not retreived")


@department_router.get("/list", response=List[DepartmentOut])
def list_departments(request):
    """
    The function `list_departments` retrieves a list of departments,
    orderd by department name ascending.

    Endpoint:
        - **Path**: `/api/v1/departments/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (List[DepartmentOut]): a list of department objects
    """

    try:
        departments = get_ordered_list_of_departments()

        return [domain_department_to_schema(g) for g in departments]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Department list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@department_router.delete("/delete/{department_id}")
def delete_department_endpoint(request, department_id: int):
    """
    The function `delete_department_endpoint` deletes the department specified by id.

    Endpoint:
        - **Path**: `/api/v1/departments/delete/{department_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        department_id (int): the id of the department to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the department with the specified ID does not exist.
    """

    try:
        department = delete_department(department_id)
        api_logger.info(f"Department deleted : {department}")
        return {"success": True}
    except DepartmentDoesNotExist:
        api_logger.error(
            f"Department not deleted : department id {department_id} not found"
        )
        error_logger.error(
            f"Department not deleted : department id {department_id} not found"
        )
        raise HttpError(
            404,
            f"Department not deleted : department id {department_id} not found",
        )
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Department not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Department deletion error")
