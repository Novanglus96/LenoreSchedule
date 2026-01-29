import pytest
from staff.models import Department


@pytest.mark.django_db
@pytest.mark.unit
def test_department_creation():
    """
    Test department is created successfully.
    """
    department = Department.objects.create(department_name="Test Department")

    assert department.id is not None
    assert department.department_name == "Test Department"


@pytest.mark.django_db
@pytest.mark.unit
def test_department_str():
    """
    Test the string representation of the department
    """
    department = Department.objects.create(department_name="Test Department")

    expected = "Test Department"
    assert str(department) == expected
