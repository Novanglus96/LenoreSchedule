from dataclasses import dataclass


@dataclass
class DomainGroup:
    id: int
    group_name: str


@dataclass(frozen=True)
class DomainGroupIn:
    group_name: str


@dataclass
class DomainDivision:
    id: int
    division_name: str


@dataclass(frozen=True)
class DomainDivisionIn:
    division_name: str


@dataclass
class DomainEmployee:
    id: int
    first_name: str
    last_name: str
    email: str
    division: DomainDivision
    group: DomainGroup


@dataclass(frozen=True)
class DomainEmployeeIn:
    first_name: str
    last_name: str
    email: str
    division_id: int
    group_id: int
