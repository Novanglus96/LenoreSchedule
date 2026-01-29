import pytest
from staff.models import Employee, Group, Department


@pytest.mark.django_db
@pytest.mark.unit
def test_employee_creation():
    """
    Test employee is created successfully.
    """
    group = Group.objects.create(group_name="Test Group")
    department = Department.objects.create(department_name="Test Department")
    employee = Employee.objects.create(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        department=department,
        group=group,
    )

    assert employee.id is not None
    assert employee.first_name == "John"
    assert employee.last_name == "Doe"
    assert employee.email == "someone@somewhere.com"
    assert employee.department.department_name == "Test Department"
    assert employee.group.group_name == "Test Group"


@pytest.mark.django_db
@pytest.mark.unit
def test_employee_str():
    """
    Test the string representation of the employee
    """
    group = Group.objects.create(group_name="Test Group")
    department = Department.objects.create(department_name="Test Department")
    employee = Employee.objects.create(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        department=department,
        group=group,
    )

    expected = "Doe, John"
    assert str(employee) == expected
