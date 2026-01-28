import pytest
from groups.services.group_services import create_group
from groups.dto import DomainGroupIn
from groups.exceptions import GroupAlreadyExists
from groups.models import Group


@pytest.mark.django_db
@pytest.mark.service
def test_create_group_success():
    dto = DomainGroupIn(group_name="Admins")

    group = create_group(dto)

    assert group.group_name == "Admins"
    assert Group.objects.filter(group_name="Admins").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_group_duplicate_name_raises():
    Group.objects.create(group_name="Admins")

    with pytest.raises(GroupAlreadyExists):
        create_group(DomainGroupIn(group_name="Admins"))
