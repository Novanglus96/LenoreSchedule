from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class DomainPayrollInfo:
    id: int
    payroll_year: int
    payroll_start: date
    payroll_frequency: str
    first_day: Optional[int] = None
    second_day: Optional[int] = None
    week_start_day: str = "sun"


@dataclass(frozen=True)
class DomainPayrollInfoIn:
    payroll_year: int
    payroll_start: date
    payroll_frequency: str
    first_day: Optional[int] = None
    second_day: Optional[int] = None
    week_start_day: str = "sun"
