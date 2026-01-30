import pytest
from staff.models import Employee, Group, Division, Location


@pytest.mark.django_db
@pytest.mark.unit
def test_employee_creation(today_date):
    """
    Test employee is created successfully.
    """
    group = Group.objects.create(group_name="Test Group")
    division = Division.objects.create(division_name="Test Division")
    location = Location.objects.create(location_name="Test Location")
    employee = Employee.objects.create(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division=division,
        group=group,
        location=location,
        start_date=today_date,
        end_date=today_date,
    )

    assert employee.id is not None
    assert employee.first_name == "John"
    assert employee.last_name == "Doe"
    assert employee.email == "someone@somewhere.com"
    assert employee.division.division_name == "Test Division"
    assert employee.group.group_name == "Test Group"


@pytest.mark.django_db
@pytest.mark.unit
def test_employee_creation_dates_optional():
    """
    Test employee is created successfully.
    """
    group = Group.objects.create(group_name="Test Group")
    division = Division.objects.create(division_name="Test Division")
    location = Location.objects.create(location_name="Test Location")
    employee = Employee.objects.create(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division=division,
        group=group,
        location=location,
    )

    assert employee.start_date is None
    assert employee.end_date is None


@pytest.mark.django_db
@pytest.mark.unit
def test_employee_str(today_date):
    """
    Test the string representation of the employee
    """
    group = Group.objects.create(group_name="Test Group")
    division = Division.objects.create(division_name="Test Division")
    location = Location.objects.create(location_name="Test Location")
    employee = Employee.objects.create(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division=division,
        group=group,
        location=location,
        start_date=today_date,
        end_date=today_date,
    )

    expected = "Doe, John"
    assert str(employee) == expected
