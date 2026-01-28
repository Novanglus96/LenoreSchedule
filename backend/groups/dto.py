from dataclasses import dataclass


@dataclass
class DomainGroup:
    id: int
    group_name: str


@dataclass(frozen=True)
class DomainGroupIn:
    group_name: str
