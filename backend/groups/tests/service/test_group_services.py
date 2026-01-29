import pytest
from groups.services.group_services import (
    create_group,
    update_group,
    get_group,
    get_ordered_list_of_groups,
    delete_group,
)
from groups.dto import DomainGroupIn, DomainGroup
from groups.exceptions import GroupAlreadyExists, GroupDoesNotExist
from groups.models import Group


@pytest.mark.django_db
@pytest.mark.service
def test_create_group_success():
    """
    Creating a group should be successful and persistent.
    """
    dto = DomainGroupIn(group_name="Admins")

    group = create_group(dto)

    assert group.group_name == "Admins"
    assert Group.objects.filter(group_name="Admins").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_group_duplicate_name_raises():
    """
    Creating a group with a duplciate group name should raise an error.
    """
    Group.objects.create(group_name="Admins")

    with pytest.raises(GroupAlreadyExists):
        create_group(DomainGroupIn(group_name="Admins"))


@pytest.mark.django_db
@pytest.mark.service
def test_create_group_dto():
    """
    Creating a group should return a DomainGroup object
    """
    group = create_group(DomainGroupIn(group_name="Admins"))
    assert isinstance(group, DomainGroup)


@pytest.mark.django_db
@pytest.mark.service
def test_update_group_success():
    """
    Updating a group should be successfull and persistent.
    """
    group = create_group(DomainGroupIn(group_name="Admins"))

    updated = update_group(
        group_id=group.id,
        dto=DomainGroupIn(group_name="Updated"),
    )

    assert updated.group_name == "Updated"
    assert Group.objects.get(id=group.id).group_name == "Updated"


@pytest.mark.django_db
@pytest.mark.service
def test_update_group_duplicate_name_raises():
    """
    Updating a group with a duplciate group name should raise an error.
    """
    group = create_group(DomainGroupIn(group_name="Admins"))
    create_group(DomainGroupIn(group_name="Test"))

    with pytest.raises(GroupAlreadyExists):
        update_group(group.id, DomainGroupIn(group_name="Test"))


@pytest.mark.django_db
@pytest.mark.service
def test_update_group_not_found():
    """
    Upading a group that doesn't exist should raise an error.
    """
    with pytest.raises(GroupDoesNotExist):
        update_group(999, DomainGroupIn(group_name="X"))


@pytest.mark.django_db
@pytest.mark.service
def test_update_group_dto():
    """
    Updaint a group should return a DomainGroup
    """
    group = create_group(DomainGroupIn(group_name="Admins"))

    updated = update_group(
        group_id=group.id,
        dto=DomainGroupIn(group_name="Updated"),
    )

    assert isinstance(updated, DomainGroup)


@pytest.mark.django_db
@pytest.mark.service
def test_get_group_dto():
    """
    Getting a group should return a DomainGroup.
    """
    created_group = create_group(DomainGroupIn(group_name="Admins"))

    group = get_group(created_group.id)
    assert isinstance(group, DomainGroup)


@pytest.mark.django_db
@pytest.mark.service
def test_get_group_not_found_raises():
    """
    Getting a group that doesn't exist should raise error.
    """
    with pytest.raises(GroupDoesNotExist):
        get_group(999)


@pytest.mark.django_db
@pytest.mark.service
def test_get_group_list():
    """
    Getting a list of groups should return a list of DomainGroups.
    """
    create_group(DomainGroupIn(group_name="Zeta"))
    create_group(DomainGroupIn(group_name="Alpha"))
    create_group(DomainGroupIn(group_name="Beta"))

    groups = get_ordered_list_of_groups()

    assert isinstance(groups, list)
    assert groups  # not empty
    assert all(isinstance(g, DomainGroup) for g in groups)


@pytest.mark.django_db
@pytest.mark.service
def test_get_group_list_is_ordered():
    """
    Getting a list of groups should return a list of DomainGroups
    sorted ascending by group_name
    """
    create_group(DomainGroupIn(group_name="Zeta"))
    create_group(DomainGroupIn(group_name="Alpha"))
    create_group(DomainGroupIn(group_name="Beta"))

    groups = get_ordered_list_of_groups()

    names = [g.group_name for g in groups]
    assert names == ["Alpha", "Beta", "Zeta"]


@pytest.mark.django_db
@pytest.mark.service
def test_delete_group_success():
    """
    Deleting the group should remove the group and return the group_name
    """
    group = create_group(DomainGroupIn(group_name="Zeta"))

    deleted_group = delete_group(group.id)

    assert not Group.objects.filter(group_name="Zeta").exists()
    assert deleted_group == "Zeta"


@pytest.mark.django_db
@pytest.mark.service
def test_delete_group_not_found_raises():
    """
    Deleting a group that does not exist should raise an error.
    """
    with pytest.raises(GroupDoesNotExist):
        delete_group(999)
