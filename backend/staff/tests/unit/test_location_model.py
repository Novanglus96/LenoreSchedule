import pytest
from staff.models import Location


@pytest.mark.django_db
@pytest.mark.unit
def test_location_creation():
    """
    Test location is created successfully.
    """
    location = Location.objects.create(location_name="Test Location")

    assert location.id is not None
    assert location.location_name == "Test Location"


@pytest.mark.django_db
@pytest.mark.unit
def test_location_str():
    """
    Test the string representation of the location
    """
    location = Location.objects.create(location_name="Test Location")

    expected = "Test Location"
    assert str(location) == expected
