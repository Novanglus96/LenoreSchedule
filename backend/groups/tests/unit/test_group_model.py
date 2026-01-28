import pytest
from groups.models import Group


@pytest.mark.django_db
@pytest.mark.unit
def test_group_creation():
    group = Group.objects.create(group_name="Test Group")

    assert group.id is not None
    assert group.group_name == "Test Group"


@pytest.mark.django_db
@pytest.mark.unit
def test_group_str():
    group = Group.objects.create(group_name="Test Group")

    expected = "Test Group"
    assert str(group) == expected
