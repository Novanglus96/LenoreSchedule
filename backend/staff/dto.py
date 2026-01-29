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
