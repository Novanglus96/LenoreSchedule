from staff.dto import (
    DomainGroup,
    DomainGroupIn,
    DomainDivision,
    DomainDivisionIn,
    DomainEmployee,
    DomainEmployeeIn,
    DomainLocation,
    DomainLocationIn,
)
from staff.api.schemas.group import GroupOut, GroupIn
from staff.api.schemas.division import DivisionIn, DivisionOut
from staff.api.schemas.employee import EmployeeIn, EmployeeOut
from staff.api.schemas.location import LocationIn, LocationOut
from staff.models import Group, Division, Employee, Location


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


def domain_division_to_schema(
    division: DomainDivision,
) -> DivisionOut:
    return DivisionOut(id=division.id, division_name=division.division_name)


def schema_to_domain_division(schema: DivisionIn) -> DomainDivisionIn:
    return DomainDivisionIn(
        division_name=schema.division_name,
    )


def domain_division_to_model(dto: DomainDivisionIn) -> Division:
    return Division(
        division_name=dto.division_name,
    )


def model_to_domain_division(model: Division) -> DomainDivision:
    return DomainDivision(
        id=model.id,
        division_name=model.division_name,
    )


def domain_employee_to_schema(
    employee: DomainEmployee,
) -> EmployeeOut:
    return EmployeeOut(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        division=domain_division_to_schema(employee.division),
        group=domain_group_to_schema(employee.group),
    )


def schema_to_domain_employee(schema: EmployeeIn) -> DomainEmployeeIn:
    return DomainEmployeeIn(
        first_name=schema.first_name,
        last_name=schema.last_name,
        email=schema.email,
        division_id=schema.division_id,
        group_id=schema.group_id,
    )


def domain_employee_to_model(dto: DomainEmployeeIn) -> Employee:
    return Employee(
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        division_id=dto.division_id,
        group_id=dto.group_id,
    )


def model_to_domain_employee(model: Employee) -> DomainEmployee:
    return DomainEmployee(
        id=model.id,
        first_name=model.first_name,
        last_name=model.last_name,
        email=model.email,
        division=model_to_domain_division(model.division),
        group=model_to_domain_group(model.group),
    )


def domain_location_to_schema(
    location: DomainLocation,
) -> LocationOut:
    return LocationOut(id=location.id, location_name=location.location_name)


def schema_to_domain_location(schema: LocationIn) -> DomainLocationIn:
    return DomainLocationIn(
        location_name=schema.location_name,
    )


def domain_location_to_model(dto: DomainLocationIn) -> Location:
    return Location(
        location_name=dto.location_name,
    )


def model_to_domain_location(model: Location) -> DomainLocation:
    return DomainLocation(
        id=model.id,
        location_name=model.location_name,
    )
