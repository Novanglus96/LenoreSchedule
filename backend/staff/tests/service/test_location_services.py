import pytest
from staff.services.location_services import (
    create_location,
    update_location,
    get_location,
    get_ordered_list_of_locations,
    delete_location,
)
from staff.dto import DomainLocationIn, DomainLocation
from staff.exceptions import LocationAlreadyExists, LocationDoesNotExist
from staff.models import Location


@pytest.mark.django_db
@pytest.mark.service
def test_create_location_success():
    """
    Creating a location should be successful and persistent.
    """
    dto = DomainLocationIn(location_name="Admins")

    location = create_location(dto)

    assert location.location_name == "Admins"
    assert Location.objects.filter(location_name="Admins").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_location_duplicate_name_raises():
    """
    Creating a location with a duplciate location name should raise an error.
    """
    Location.objects.create(location_name="Admins")

    with pytest.raises(LocationAlreadyExists):
        create_location(DomainLocationIn(location_name="Admins"))


@pytest.mark.django_db
@pytest.mark.service
def test_create_location_dto():
    """
    Creating a location should return a DomainLocation object
    """
    location = create_location(DomainLocationIn(location_name="Admins"))
    assert isinstance(location, DomainLocation)


@pytest.mark.django_db
@pytest.mark.service
def test_update_location_success():
    """
    Updating a location should be successfull and persistent.
    """
    location = create_location(DomainLocationIn(location_name="Admins"))

    updated = update_location(
        location_id=location.id,
        dto=DomainLocationIn(location_name="Updated"),
    )

    assert updated.location_name == "Updated"
    assert Location.objects.get(id=location.id).location_name == "Updated"


@pytest.mark.django_db
@pytest.mark.service
def test_update_location_duplicate_name_raises():
    """
    Updating a location with a duplciate location name should raise an error.
    """
    location = create_location(DomainLocationIn(location_name="Admins"))
    create_location(DomainLocationIn(location_name="Test"))

    with pytest.raises(LocationAlreadyExists):
        update_location(location.id, DomainLocationIn(location_name="Test"))


@pytest.mark.django_db
@pytest.mark.service
def test_update_location_not_found():
    """
    Upading a location that doesn't exist should raise an error.
    """
    with pytest.raises(LocationDoesNotExist):
        update_location(999, DomainLocationIn(location_name="X"))


@pytest.mark.django_db
@pytest.mark.service
def test_update_location_dto():
    """
    Updaint a location should return a DomainLocation
    """
    location = create_location(DomainLocationIn(location_name="Admins"))

    updated = update_location(
        location_id=location.id,
        dto=DomainLocationIn(location_name="Updated"),
    )

    assert isinstance(updated, DomainLocation)


@pytest.mark.django_db
@pytest.mark.service
def test_get_location_dto():
    """
    Getting a location should return a DomainLocation.
    """
    created_location = create_location(DomainLocationIn(location_name="Admins"))

    location = get_location(created_location.id)
    assert isinstance(location, DomainLocation)


@pytest.mark.django_db
@pytest.mark.service
def test_get_location_not_found_raises():
    """
    Getting a location that doesn't exist should raise error.
    """
    with pytest.raises(LocationDoesNotExist):
        get_location(999)


@pytest.mark.django_db
@pytest.mark.service
def test_get_location_list():
    """
    Getting a list of locations should return a list of DomainLocations.
    """
    create_location(DomainLocationIn(location_name="Zeta"))
    create_location(DomainLocationIn(location_name="Alpha"))
    create_location(DomainLocationIn(location_name="Beta"))

    locations = get_ordered_list_of_locations()

    assert isinstance(locations, list)
    assert locations  # not empty
    assert all(isinstance(g, DomainLocation) for g in locations)


@pytest.mark.django_db
@pytest.mark.service
def test_get_location_list_is_ordered():
    """
    Getting a list of locations should return a list of DomainLocations
    sorted ascending by location_name
    """
    create_location(DomainLocationIn(location_name="Zeta"))
    create_location(DomainLocationIn(location_name="Alpha"))
    create_location(DomainLocationIn(location_name="Beta"))

    locations = get_ordered_list_of_locations()

    names = [g.location_name for g in locations]
    assert names == ["Alpha", "Beta", "Zeta"]


@pytest.mark.django_db
@pytest.mark.service
def test_delete_location_success():
    """
    Deleting the location should remove the location and return the location_name
    """
    location = create_location(DomainLocationIn(location_name="Zeta"))

    deleted_location = delete_location(location.id)

    assert not Location.objects.filter(location_name="Zeta").exists()
    assert deleted_location == "Zeta"


@pytest.mark.django_db
@pytest.mark.service
def test_delete_location_not_found_raises():
    """
    Deleting a location that does not exist should raise an error.
    """
    with pytest.raises(LocationDoesNotExist):
        delete_location(999)
