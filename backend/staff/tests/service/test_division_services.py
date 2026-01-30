import pytest
from staff.services.division_services import (
    create_division,
    update_division,
    get_division,
    get_ordered_list_of_divisions,
    delete_division,
)
from staff.dto import DomainDivisionIn, DomainDivision
from staff.exceptions import DivisionAlreadyExists, DivisionDoesNotExist
from staff.models import Division


@pytest.mark.django_db
@pytest.mark.service
def test_create_division_success():
    """
    Creating a division should be successful and persistent.
    """
    dto = DomainDivisionIn(division_name="Admins")

    division = create_division(dto)

    assert division.division_name == "Admins"
    assert Division.objects.filter(division_name="Admins").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_division_duplicate_name_raises():
    """
    Creating a division with a duplciate division name should raise an error.
    """
    Division.objects.create(division_name="Admins")

    with pytest.raises(DivisionAlreadyExists):
        create_division(DomainDivisionIn(division_name="Admins"))


@pytest.mark.django_db
@pytest.mark.service
def test_create_division_dto():
    """
    Creating a division should return a DomainDivision object
    """
    division = create_division(DomainDivisionIn(division_name="Admins"))
    assert isinstance(division, DomainDivision)


@pytest.mark.django_db
@pytest.mark.service
def test_update_division_success():
    """
    Updating a division should be successfull and persistent.
    """
    division = create_division(DomainDivisionIn(division_name="Admins"))

    updated = update_division(
        division_id=division.id,
        dto=DomainDivisionIn(division_name="Updated"),
    )

    assert updated.division_name == "Updated"
    assert Division.objects.get(id=division.id).division_name == "Updated"


@pytest.mark.django_db
@pytest.mark.service
def test_update_division_duplicate_name_raises():
    """
    Updating a division with a duplciate division name should raise an error.
    """
    division = create_division(DomainDivisionIn(division_name="Admins"))
    create_division(DomainDivisionIn(division_name="Test"))

    with pytest.raises(DivisionAlreadyExists):
        update_division(division.id, DomainDivisionIn(division_name="Test"))


@pytest.mark.django_db
@pytest.mark.service
def test_update_division_not_found():
    """
    Upading a division that doesn't exist should raise an error.
    """
    with pytest.raises(DivisionDoesNotExist):
        update_division(999, DomainDivisionIn(division_name="X"))


@pytest.mark.django_db
@pytest.mark.service
def test_update_division_dto():
    """
    Updaint a division should return a DomainDivision
    """
    division = create_division(DomainDivisionIn(division_name="Admins"))

    updated = update_division(
        division_id=division.id,
        dto=DomainDivisionIn(division_name="Updated"),
    )

    assert isinstance(updated, DomainDivision)


@pytest.mark.django_db
@pytest.mark.service
def test_get_division_dto():
    """
    Getting a division should return a DomainDivision.
    """
    created_division = create_division(DomainDivisionIn(division_name="Admins"))

    division = get_division(created_division.id)
    assert isinstance(division, DomainDivision)


@pytest.mark.django_db
@pytest.mark.service
def test_get_division_not_found_raises():
    """
    Getting a division that doesn't exist should raise error.
    """
    with pytest.raises(DivisionDoesNotExist):
        get_division(999)


@pytest.mark.django_db
@pytest.mark.service
def test_get_division_list():
    """
    Getting a list of divisions should return a list of DomainDivisions.
    """
    create_division(DomainDivisionIn(division_name="Zeta"))
    create_division(DomainDivisionIn(division_name="Alpha"))
    create_division(DomainDivisionIn(division_name="Beta"))

    divisions = get_ordered_list_of_divisions()

    assert isinstance(divisions, list)
    assert divisions  # not empty
    assert all(isinstance(g, DomainDivision) for g in divisions)


@pytest.mark.django_db
@pytest.mark.service
def test_get_division_list_is_ordered():
    """
    Getting a list of divisions should return a list of DomainDivisions
    sorted ascending by division_name
    """
    create_division(DomainDivisionIn(division_name="Zeta"))
    create_division(DomainDivisionIn(division_name="Alpha"))
    create_division(DomainDivisionIn(division_name="Beta"))

    divisions = get_ordered_list_of_divisions()

    names = [g.division_name for g in divisions]
    assert names == ["Alpha", "Beta", "Zeta"]


@pytest.mark.django_db
@pytest.mark.service
def test_delete_division_success():
    """
    Deleting the division should remove the division and return the division_name
    """
    division = create_division(DomainDivisionIn(division_name="Zeta"))

    deleted_division = delete_division(division.id)

    assert not Division.objects.filter(division_name="Zeta").exists()
    assert deleted_division == "Zeta"


@pytest.mark.django_db
@pytest.mark.service
def test_delete_division_not_found_raises():
    """
    Deleting a division that does not exist should raise an error.
    """
    with pytest.raises(DivisionDoesNotExist):
        delete_division(999)
