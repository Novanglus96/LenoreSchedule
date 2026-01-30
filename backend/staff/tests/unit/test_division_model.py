import pytest
from staff.models import Division


@pytest.mark.django_db
@pytest.mark.unit
def test_division_creation():
    """
    Test division is created successfully.
    """
    division = Division.objects.create(division_name="Test Division")

    assert division.id is not None
    assert division.division_name == "Test Division"


@pytest.mark.django_db
@pytest.mark.unit
def test_division_str():
    """
    Test the string representation of the division
    """
    division = Division.objects.create(division_name="Test Division")

    expected = "Test Division"
    assert str(division) == expected
