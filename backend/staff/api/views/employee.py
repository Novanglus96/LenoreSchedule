from ninja import Router
from staff.api.schemas.employee import EmployeeIn, EmployeeOut
from ninja.errors import HttpError
from typing import List
import logging
from staff.exceptions import (
    EmployeeAlreadyExists,
    EmployeeCreationError,
    EmployeeDoesNotExist,
)
from staff.mappers import (
    schema_to_domain_employee,
    domain_employee_to_schema,
)
from staff.services.employee_services import (
    create_employee,
    update_employee,
    get_employee,
    get_ordered_list_of_employees,
    delete_employee,
)

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

employee_router = Router(tags=["Employees"])


@employee_router.post("/create")
def create_employee_endpoint(request, payload: EmployeeIn):
    """
    The function `create_employee_endpoint` creats a employee object.

    Endpoint:
        - **Path**: `/api/v1/employees/create`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (EmployeeIn): A employee schema.

    Returns:
        (dict): {'id': The ID of the created employee}.
    """
    try:
        domain_in = schema_to_domain_employee(payload)
        domain_employee = create_employee(domain_in)

        api_logger.info(
            "Employee created",
            extra={
                "employee_id": domain_employee.id,
                "last_name": domain_employee.last_name,
                "first_name": domain_employee.first_name,
            },
        )

        return {"id": domain_employee.id}

    except EmployeeAlreadyExists:
        api_logger.error(
            f"Unable to create employee({domain_in.email}): Employee already exists"
        )
        error_logger.error(
            f"Unable to create employee({domain_in.email}): Employee already exists"
        )
        raise HttpError(400, "Employee already exists")

    except EmployeeCreationError:
        api_logger.error(
            f"Unable to create employee({domain_in.email}): DB integrity error"
        )
        error_logger.error(
            f"Unable to create employee({domain_in.email}): DB integrity error"
        )
        raise HttpError(400, "DB integrity error")

    except Exception:
        api_logger.error("Employee creation failed")
        error_logger.error("Employee creation failed")
        raise HttpError(500, "Employee creation error")


@employee_router.put("/update/{employee_id}")
def update_employee_endpoint(request, employee_id: int, payload: EmployeeIn):
    """
    The function `update_employee_endpoint` updates the employee specified by id.

    Endpoint:
        - **Path**: `/api/v1/employees/update/{employee_id}`
        - **Method**: `PUT`

    Args:
        request (HttpRequest): The HTTP request object.
        employee_id (int): the id of the employee to update
        payload (EmployeeIn): a employee object

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the employee with the specified ID does not exist.
    """

    try:
        domain_update = schema_to_domain_employee(payload)
        update_employee(employee_id, domain_update)

        return {"success": True}

    except EmployeeAlreadyExists:
        api_logger.error(
            f"Employee not updated : employee email exists ({payload.email})"
        )
        error_logger.error(
            f"Employee not updated : employee email exists ({payload.email})"
        )
        raise HttpError(400, "Employee not updated: employee email exists")

    except EmployeeDoesNotExist:
        api_logger.error(
            f"Employee not updated : employee id {employee_id} not found"
        )
        error_logger.error(
            f"Employee not updated : employee id {employee_id} not found"
        )
        raise HttpError(
            404,
            f"Employee not updated : employee id {employee_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Employee not updated")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Employee update error")


@employee_router.get("/get/{employee_id}", response=EmployeeOut)
def get_employee_endpoint(request, employee_id: int):
    """
    The function `get_employee_endpoint` retrieves the employee by id

    Endpoint:
        - **Path**: `/api/v1/employees/get/{employee_id}`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object
        employee_id (int): The id of the employee to retrieve.

    Returns:
        (EmployeeOut): the employee object

    Raises:
        Http404: If the employee with the specified ID does not exist.
    """
    try:
        employee = get_employee(employee_id)

        return domain_employee_to_schema(employee)

    except EmployeeDoesNotExist:
        api_logger.error(
            f"Employee not retreived : employee id {employee_id} not found"
        )
        error_logger.error(
            f"Employee not retreived : employee id {employee_id} not found"
        )
        raise HttpError(
            404,
            f"Employee not retreived : employee id {employee_id} not found",
        )

    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Employee not retreived")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Employee not retreived")


@employee_router.get("/list", response=List[EmployeeOut])
def list_employees(request):
    """
    The function `list_employees` retrieves a list of employees,
    orderd by employee name ascending.

    Endpoint:
        - **Path**: `/api/v1/employees/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (List[EmployeeOut]): a list of employee objects
    """

    try:
        employees = get_ordered_list_of_employees()

        return [domain_employee_to_schema(g) for g in employees]
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Employee list not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")


@employee_router.delete("/delete/{employee_id}")
def delete_employee_endpoint(request, employee_id: int):
    """
    The function `delete_employee_endpoint` deletes the employee specified by id.

    Endpoint:
        - **Path**: `/api/v1/employees/delete/{employee_id}`
        - **Method**: `DELETE`

    Args:
        request (HttpRequest): The HTTP request object.
        employee_id (int): the id of the employee to delete

    Returns:
        (dict): {'success': True}

    Raises:
        Http404: If the employee with the specified ID does not exist.
    """

    try:
        employee = delete_employee(employee_id)
        api_logger.info(f"Employee deleted : {employee}")
        return {"success": True}
    except EmployeeDoesNotExist:
        api_logger.error(
            f"Employee not deleted : employee id {employee_id} not found"
        )
        error_logger.error(
            f"Employee not deleted : employee id {employee_id} not found"
        )
        raise HttpError(
            404,
            f"Employee not deleted : employee id {employee_id} not found",
        )
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Employee not deleted")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Employee deletion error")
