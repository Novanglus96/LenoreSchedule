from staff.dto import (
    DomainGroup,
    DomainGroupIn,
    DomainDepartment,
    DomainDepartmentIn,
)
from staff.api.schemas.group import GroupOut, GroupIn
from staff.api.schemas.department import DepartmentIn, DepartmentOut
from staff.models import Group, Department


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
