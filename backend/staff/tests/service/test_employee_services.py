import pytest
from staff.services.employee_services import (
    create_employee,
    update_employee,
    get_employee,
    get_ordered_list_of_employees,
    delete_employee,
)
from staff.dto import DomainEmployeeIn, DomainEmployee
from staff.exceptions import EmployeeAlreadyExists, EmployeeDoesNotExist
from staff.models import Employee
from staff.factories import DivisionFactory, GroupFactory, EmployeeFactory


@pytest.mark.django_db
@pytest.mark.service
def test_create_employee_success():
    """
    Creating a employee should be successful and persistent.
    """
    group = GroupFactory()
    division = DivisionFactory()
    dto = DomainEmployeeIn(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division_id=division.id,
        group_id=group.id,
    )

    employee = create_employee(dto)

    assert employee.first_name == "John"
    assert employee.last_name == "Doe"
    assert employee.email == "someone@somewhere.com"
    assert employee.division.id == division.id
    assert employee.group.id == group.id
    assert Employee.objects.filter(email="someone@somewhere.com").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_employee_duplicate_email_raises():
    """
    Creating a employee with a duplciate employee email should raise an error.
    """
    group = GroupFactory()
    division = DivisionFactory()
    dto = DomainEmployeeIn(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division_id=division.id,
        group_id=group.id,
    )

    create_employee(dto)

    with pytest.raises(EmployeeAlreadyExists):
        create_employee(
            DomainEmployeeIn(
                first_name="John",
                last_name="Smith",
                email="someone@somewhere.com",
                division_id=division.id,
                group_id=group.id,
            )
        )


@pytest.mark.django_db
@pytest.mark.service
def test_create_employee_dto():
    """
    Creating a employee should return a DomainEmployee object
    """
    group = GroupFactory()
    division = DivisionFactory()
    dto = DomainEmployeeIn(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division_id=division.id,
        group_id=group.id,
    )

    employee = create_employee(dto)

    assert isinstance(employee, DomainEmployee)


@pytest.mark.django_db
@pytest.mark.service
def test_update_employee_success():
    """
    Updating a employee should be successfull and persistent.
    """
    group = GroupFactory()
    division = DivisionFactory()
    dto = DomainEmployeeIn(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division_id=division.id,
        group_id=group.id,
    )

    employee = create_employee(dto)

    updated = update_employee(
        employee_id=employee.id,
        dto=DomainEmployeeIn(
            first_name="Updated",
            last_name="Name",
            email="someone@somewhere.com",
            division_id=division.id,
            group_id=group.id,
        ),
    )

    assert updated.first_name == "Updated"
    assert updated.last_name == "Name"
    assert Employee.objects.get(id=employee.id).first_name == "Updated"
    assert Employee.objects.get(id=employee.id).last_name == "Name"


@pytest.mark.django_db
@pytest.mark.service
def test_update_employee_duplicate_email_raises():
    """
    Updating a employee with a duplciate employee email should raise an error.
    """
    group = GroupFactory()
    division = DivisionFactory()
    dto = DomainEmployeeIn(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division_id=division.id,
        group_id=group.id,
    )

    employee = create_employee(dto)
    create_employee(
        DomainEmployeeIn(
            first_name="Jane",
            last_name="Smith",
            email="jsmith@somewhere.com",
            division_id=division.id,
            group_id=group.id,
        )
    )

    with pytest.raises(EmployeeAlreadyExists):
        update_employee(
            employee.id,
            DomainEmployeeIn(
                first_name="John",
                last_name="Doe",
                email="jsmith@somewhere.com",
                division_id=division.id,
                group_id=group.id,
            ),
        )


@pytest.mark.django_db
@pytest.mark.service
def test_update_employee_not_found():
    """
    Upading a employee that doesn't exist should raise an error.
    """
    with pytest.raises(EmployeeDoesNotExist):
        group = GroupFactory()
        division = DivisionFactory()
        update_employee(
            999,
            DomainEmployeeIn(
                first_name="John",
                last_name="Doe",
                email="jsmith@somewhere.com",
                division_id=division.id,
                group_id=group.id,
            ),
        )


@pytest.mark.django_db
@pytest.mark.service
def test_update_employee_dto():
    """
    Updating an employee should return a DomainEmployee
    """
    group = GroupFactory()
    division = DivisionFactory()
    dto = DomainEmployeeIn(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division_id=division.id,
        group_id=group.id,
    )

    employee = create_employee(dto)

    updated = update_employee(
        employee_id=employee.id,
        dto=DomainEmployeeIn(
            first_name="Updated",
            last_name="Name",
            email="someone@somewhere.com",
            division_id=division.id,
            group_id=group.id,
        ),
    )

    assert isinstance(updated, DomainEmployee)


@pytest.mark.django_db
@pytest.mark.service
def test_get_employee_dto():
    """
    Getting a employee should return a DomainEmployee.
    """
    group = GroupFactory()
    division = DivisionFactory()
    dto = DomainEmployeeIn(
        first_name="John",
        last_name="Doe",
        email="someone@somewhere.com",
        division_id=division.id,
        group_id=group.id,
    )

    created_employee = create_employee(dto)

    employee = get_employee(created_employee.id)
    assert isinstance(employee, DomainEmployee)


@pytest.mark.django_db
@pytest.mark.service
def test_get_employee_not_found_raises():
    """
    Getting a employee that doesn't exist should raise error.
    """
    with pytest.raises(EmployeeDoesNotExist):
        get_employee(999)


@pytest.mark.django_db
@pytest.mark.service
def test_get_employee_list():
    """
    Getting a list of employees should return a list of DomainEmployees.
    """
    EmployeeFactory(last_name="Adams")
    EmployeeFactory(last_name="Smith")
    EmployeeFactory(last_name="Cooke")
    employees = get_ordered_list_of_employees()

    assert isinstance(employees, list)
    assert employees  # not empty
    assert all(isinstance(g, DomainEmployee) for g in employees)


@pytest.mark.django_db
@pytest.mark.service
def test_get_employee_list_is_ordered():
    """
    Getting a list of employees should return a list of DomainEmployees
    sorted ascending by employee_name
    """
    EmployeeFactory(last_name="Adams")
    EmployeeFactory(last_name="Smith")
    EmployeeFactory(last_name="Cooke")

    employees = get_ordered_list_of_employees()

    names = [g.last_name for g in employees]
    assert names == ["Adams", "Cooke", "Smith"]


@pytest.mark.django_db
@pytest.mark.service
def test_delete_employee_success():
    """
    Deleting the employee should remove the employee and return the employee_name
    """
    employee = EmployeeFactory()

    deleted_employee = delete_employee(employee.id)

    assert not Employee.objects.filter(email=employee.email).exists()
    assert deleted_employee == f"{employee.last_name}, {employee.first_name}"


@pytest.mark.django_db
@pytest.mark.service
def test_delete_employee_not_found_raises():
    """
    Deleting a employee that does not exist should raise an error.
    """
    with pytest.raises(EmployeeDoesNotExist):
        delete_employee(999)
