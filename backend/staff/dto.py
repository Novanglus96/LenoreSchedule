from dataclasses import dataclass


@dataclass
class DomainGroup:
    id: int
    group_name: str


@dataclass(frozen=True)
class DomainGroupIn:
    group_name: str


@dataclass
class DomainDepartment:
    id: int
    department_name: str


@dataclass(frozen=True)
class DomainDepartmentIn:
    department_name: str


@dataclass
class DomainEmployee:
    id: int
    first_name: str
    last_name: str
    email: str
    department: DomainDepartment
    group: DomainGroup


@dataclass(frozen=True)
class DomainEmployeeIn:
    first_name: str
    last_name: str
    email: str
    department_id: int
    group_id: int
