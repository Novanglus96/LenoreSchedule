from staff.dto import (
    DomainGroup,
    DomainGroupIn,
    DomainDepartment,
    DomainDepartmentIn,
    DomainEmployee,
    DomainEmployeeIn,
)
from staff.api.schemas.group import GroupOut, GroupIn
from staff.api.schemas.department import DepartmentIn, DepartmentOut
from staff.api.schemas.employee import EmployeeIn, EmployeeOut
from staff.models import Group, Department, Employee


def domain_group_to_schema(
    group: DomainGroup,
) -> GroupOut:
    return GroupOut(id=group.id, group_name=group.group_name)


def schema_to_domain_group(schema: GroupIn) -> DomainGroupIn:
    return DomainGroupIn(
        group_name=schema.group_name,
    )


def domain_group_to_model(dto: DomainGroupIn) -> Group:
    return Group(
        group_name=dto.group_name,
    )


def model_to_domain_group(model: Group) -> DomainGroup:
    return DomainGroup(
        id=model.id,
        group_name=model.group_name,
    )


def domain_department_to_schema(
    department: DomainDepartment,
) -> DepartmentOut:
    return DepartmentOut(
        id=department.id, department_name=department.department_name
    )


def schema_to_domain_department(schema: DepartmentIn) -> DomainDepartmentIn:
    return DomainDepartmentIn(
        department_name=schema.department_name,
    )


def domain_department_to_model(dto: DomainDepartmentIn) -> Department:
    return Department(
        department_name=dto.department_name,
    )


def model_to_domain_department(model: Department) -> DomainDepartment:
    return DomainDepartment(
        id=model.id,
        department_name=model.department_name,
    )


def domain_employee_to_schema(
    employee: DomainEmployee,
) -> EmployeeOut:
    return EmployeeOut(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        department=domain_department_to_schema(employee.department),
        group=domain_group_to_schema(employee.group),
    )


def schema_to_domain_employee(schema: EmployeeIn) -> DomainEmployeeIn:
    return DomainEmployeeIn(
        first_name=schema.first_name,
        last_name=schema.last_name,
        email=schema.email,
        department_id=schema.department_id,
        group_id=schema.group_id,
    )


def domain_employee_to_model(dto: DomainEmployeeIn) -> Employee:
    return Employee(
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        department_id=dto.department_id,
        group_id=dto.group_id,
    )


def model_to_domain_employee(model: Employee) -> DomainEmployee:
    return DomainEmployee(
        id=model.id,
        first_name=model.first_name,
        last_name=model.last_name,
        email=model.email,
        department=model_to_domain_department(model.department),
        group=model_to_domain_group(model.group),
    )
