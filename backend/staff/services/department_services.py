from django.db import IntegrityError, transaction
from staff.models import Department
from staff.dto import DomainDepartment, DomainDepartmentIn
from staff.exceptions import (
    DepartmentAlreadyExists,
    DepartmentCreationError,
    DepartmentDoesNotExist,
)
from staff.mappers import domain_department_to_model, model_to_domain_department
from typing import List


def get_department_model_or_raise(department_id: int) -> Department:
    """
    `get_department_model_or_raise` gets a department or raises an error
    if not found.

    Args:
        department_id (int): The id of the department to get.

    Raises:
        DepartmentDoesNotExist: Department does not exist.

    Returns:
        Department: A department model object.
    """
    try:
        return Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        raise DepartmentDoesNotExist(department_id)


def create_department(dto: DomainDepartmentIn) -> DomainDepartment:
    """
    `create_department` creates a department if a duplicate department does
    not exist.

    Args:
        dto (DomainDepartmentIn): A domain department object.

    Raises:
        DepartmentAlreadyExists: Department already exists.
        DepartmentCreationError: Departmente creation error.

    Returns:
        DomainDepartment: A domain department object.
    """
    if Department.objects.filter(department_name=dto.department_name).exists():
        raise DepartmentAlreadyExists()

    department = domain_department_to_model(dto)

    try:
        with transaction.atomic():
            department.save()
    except IntegrityError as e:
        raise DepartmentCreationError() from e

    return model_to_domain_department(department)


def update_department(
    department_id: int, dto: DomainDepartmentIn
) -> DomainDepartment:
    """
    `update_department` updates a department

    Args:
        department_id (int): ID of the department to update.
        dto (DomainDepartmentIn): The updated domain department object.

    Raises:
        DepartmentAlreadyExists: Department already exists.

    Returns:
        DomainDepartment: A domain department object.
    """
    department = get_department_model_or_raise(department_id)

    if Department.objects.filter(department_name=dto.department_name).exists():
        raise DepartmentAlreadyExists()

    if dto.department_name is not None:
        department.department_name = dto.department_name

    department.save()

    return model_to_domain_department(department)


def get_department(department_id: int) -> DomainDepartment:
    """
    `get_department` returns a domain department object.

    Args:
        department_id (int): ID of the department to get.

    Returns:
        DomainDepartment: The domain department object.
    """
    department = get_department_model_or_raise(department_id)

    return model_to_domain_department(department)


def get_ordered_list_of_departments() -> List[DomainDepartment]:
    """
    `get_ordered_list_of_departments` gets a list of domain department objects, ordered
    by department_name ascending.

    Returns:
        List[DomainDepartment]: A list of domain department objects.
    """
    departments = Department.objects.all().order_by("department_name")

    return [model_to_domain_department(g) for g in departments]


def delete_department(department_id: int) -> str:
    """
    `delete_department` deletes a department and returns the deleted department name.

    Args:
        department_id (int): The id of the department to delete.

    Returns:
        str: The name of the deleted department.
    """
    department = get_department_model_or_raise(department_id)
    department_name = department.department_name

    department.delete()
    return department_name
