from django.db import IntegrityError, transaction
from staff.models import Employee
from staff.dto import DomainEmployee, DomainEmployeeIn
from staff.exceptions import (
    EmployeeAlreadyExists,
    EmployeeCreationError,
    EmployeeDoesNotExist,
)
from staff.mappers import domain_employee_to_model, model_to_domain_employee
from typing import List


def get_employee_model_or_raise(employee_id: int) -> Employee:
    """
    `get_employee_model_or_raise` gets a employee or raises an error
    if not found.

    Args:
        employee_id (int): The id of the employee to get.

    Raises:
        EmployeeDoesNotExist: Employee does not exist.

    Returns:
        Employee: A employee model object.
    """
    try:
        return Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        raise EmployeeDoesNotExist(employee_id)


def create_employee(dto: DomainEmployeeIn) -> DomainEmployee:
    """
    `create_employee` creates a employee if a duplicate employee does
    not exist.

    Args:
        dto (DomainEmployeeIn): A domain employee object.

    Raises:
        EmployeeAlreadyExists: Employee already exists.
        EmployeeCreationError: Employeee creation error.

    Returns:
        DomainEmployee: A domain employee object.
    """
    if Employee.objects.filter(email=dto.email).exists():
        raise EmployeeAlreadyExists()

    employee = domain_employee_to_model(dto)

    try:
        with transaction.atomic():
            employee.save()
    except IntegrityError as e:
        raise EmployeeCreationError() from e

    return model_to_domain_employee(employee)


def update_employee(employee_id: int, dto: DomainEmployeeIn) -> DomainEmployee:
    """
    `update_employee` updates a employee

    Args:
        employee_id (int): ID of the employee to update.
        dto (DomainEmployeeIn): The updated domain employee object.

    Raises:
        EmployeeAlreadyExists: Employee already exists.

    Returns:
        DomainEmployee: A domain employee object.
    """
    employee = get_employee_model_or_raise(employee_id)

    if (
        Employee.objects.filter(email=dto.email)
        .exclude(id=employee_id)
        .exists()
    ):
        raise EmployeeAlreadyExists()

    if dto.first_name is not None:
        employee.first_name = dto.first_name

    if dto.last_name is not None:
        employee.last_name = dto.last_name

    if dto.email is not None:
        employee.email = dto.email

    if dto.group_id is not None:
        employee.group_id = dto.group_id

    if dto.department_id is not None:
        employee.department_id = dto.department_id

    employee.save()

    return model_to_domain_employee(employee)


def get_employee(employee_id: int) -> DomainEmployee:
    """
    `get_employee` returns a domain employee object.

    Args:
        employee_id (int): ID of the employee to get.

    Returns:
        DomainEmployee: The domain employee object.
    """
    employee = get_employee_model_or_raise(employee_id)

    return model_to_domain_employee(employee)


def get_ordered_list_of_employees() -> List[DomainEmployee]:
    """
    `get_ordered_list_of_employees` gets a list of domain employee objects, ordered
    by last_name ascending, first_name ascending, id ascending.

    Returns:
        List[DomainEmployee]: A list of domain employee objects.
    """
    employees = Employee.objects.all().order_by("last_name", "first_name", "id")

    return [model_to_domain_employee(g) for g in employees]


def delete_employee(employee_id: int) -> str:
    """
    `delete_employee` deletes a employee and returns the deleted employee name.

    Args:
        employee_id (int): The id of the employee to delete.

    Returns:
        str: The name of the deleted employee.
    """
    employee = get_employee_model_or_raise(employee_id)
    employee_name = f"{employee.last_name}, {employee.first_name}"

    employee.delete()
    return employee_name
