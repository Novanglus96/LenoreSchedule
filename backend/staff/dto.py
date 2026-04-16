from dataclasses import dataclass
from datetime import date
from typing import Optional


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
class DomainLocation:
    id: int
    location_name: str


@dataclass(frozen=True)
class DomainLocationIn:
    location_name: str


@dataclass
class DomainEmployee:
    id: int
    first_name: str
    last_name: str
    email: str
    division: DomainDivision
    group: DomainGroup
    location: DomainLocation
    start_date: Optional[date] = None
    end_date: Optional[date] = None


@dataclass(frozen=True)
class DomainEmployeeIn:
    first_name: str
    last_name: str
    email: str
    division_id: int
    group_id: int
    location_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
