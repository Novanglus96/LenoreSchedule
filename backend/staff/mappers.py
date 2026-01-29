from staff.dto import DomainGroup, DomainGroupIn
from staff.api.schemas.group import GroupOut, GroupIn
from staff.models import Group


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
