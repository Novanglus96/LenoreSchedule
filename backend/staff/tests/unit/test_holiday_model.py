import pytest
from staff.models import Holiday


@pytest.mark.django_db
@pytest.mark.unit
def test_holiday_creation():
    """
    Test holiday is created successfully.
    """
    holiday = Holiday.objects.create(holiday_name="Test Holiday")

    assert holiday.id is not None
    assert holiday.holiday_name == "Test Holiday"


@pytest.mark.django_db
@pytest.mark.unit
def test_holiday_str():
    """
    Test the string representation of the holiday
    """
    holiday = Holiday.objects.create(holiday_name="Test Holiday")

    expected = "Test Holiday"
    assert str(holiday) == expected
