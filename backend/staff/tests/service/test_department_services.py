import pytest
from staff.services.department_services import (
    create_department,
    update_department,
    get_department,
    get_ordered_list_of_departments,
    delete_department,
)
from staff.dto import DomainDepartmentIn, DomainDepartment
from staff.exceptions import DepartmentAlreadyExists, DepartmentDoesNotExist
from staff.models import Department


@pytest.mark.django_db
@pytest.mark.service
def test_create_department_success():
    """
    Creating a department should be successful and persistent.
    """
    dto = DomainDepartmentIn(department_name="Admins")

    department = create_department(dto)

    assert department.department_name == "Admins"
    assert Department.objects.filter(department_name="Admins").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_department_duplicate_name_raises():
    """
    Creating a department with a duplciate department name should raise an error.
    """
    Department.objects.create(department_name="Admins")

    with pytest.raises(DepartmentAlreadyExists):
        create_department(DomainDepartmentIn(department_name="Admins"))


@pytest.mark.django_db
@pytest.mark.service
def test_create_department_dto():
    """
    Creating a department should return a DomainDepartment object
    """
    department = create_department(DomainDepartmentIn(department_name="Admins"))
    assert isinstance(department, DomainDepartment)


@pytest.mark.django_db
@pytest.mark.service
def test_update_department_success():
    """
    Updating a department should be successfull and persistent.
    """
    department = create_department(DomainDepartmentIn(department_name="Admins"))

    updated = update_department(
        department_id=department.id,
        dto=DomainDepartmentIn(department_name="Updated"),
    )

    assert updated.department_name == "Updated"
    assert Department.objects.get(id=department.id).department_name == "Updated"


@pytest.mark.django_db
@pytest.mark.service
def test_update_department_duplicate_name_raises():
    """
    Updating a department with a duplciate department name should raise an error.
    """
    department = create_department(DomainDepartmentIn(department_name="Admins"))
    create_department(DomainDepartmentIn(department_name="Test"))

    with pytest.raises(DepartmentAlreadyExists):
        update_department(
            department.id, DomainDepartmentIn(department_name="Test")
        )


@pytest.mark.django_db
@pytest.mark.service
def test_update_department_not_found():
    """
    Upading a department that doesn't exist should raise an error.
    """
    with pytest.raises(DepartmentDoesNotExist):
        update_department(999, DomainDepartmentIn(department_name="X"))


@pytest.mark.django_db
@pytest.mark.service
def test_update_department_dto():
    """
    Updaint a department should return a DomainDepartment
    """
    department = create_department(DomainDepartmentIn(department_name="Admins"))

    updated = update_department(
        department_id=department.id,
        dto=DomainDepartmentIn(department_name="Updated"),
    )

    assert isinstance(updated, DomainDepartment)


@pytest.mark.django_db
@pytest.mark.service
def test_get_department_dto():
    """
    Getting a department should return a DomainDepartment.
    """
    created_department = create_department(
        DomainDepartmentIn(department_name="Admins")
    )

    department = get_department(created_department.id)
    assert isinstance(department, DomainDepartment)


@pytest.mark.django_db
@pytest.mark.service
def test_get_department_not_found_raises():
    """
    Getting a department that doesn't exist should raise error.
    """
    with pytest.raises(DepartmentDoesNotExist):
        get_department(999)


@pytest.mark.django_db
@pytest.mark.service
def test_get_department_list():
    """
    Getting a list of departments should return a list of DomainDepartments.
    """
    create_department(DomainDepartmentIn(department_name="Zeta"))
    create_department(DomainDepartmentIn(department_name="Alpha"))
    create_department(DomainDepartmentIn(department_name="Beta"))

    departments = get_ordered_list_of_departments()

    assert isinstance(departments, list)
    assert departments  # not empty
    assert all(isinstance(g, DomainDepartment) for g in departments)


@pytest.mark.django_db
@pytest.mark.service
def test_get_department_list_is_ordered():
    """
    Getting a list of departments should return a list of DomainDepartments
    sorted ascending by department_name
    """
    create_department(DomainDepartmentIn(department_name="Zeta"))
    create_department(DomainDepartmentIn(department_name="Alpha"))
    create_department(DomainDepartmentIn(department_name="Beta"))

    departments = get_ordered_list_of_departments()

    names = [g.department_name for g in departments]
    assert names == ["Alpha", "Beta", "Zeta"]


@pytest.mark.django_db
@pytest.mark.service
def test_delete_department_success():
    """
    Deleting the department should remove the department and return the department_name
    """
    department = create_department(DomainDepartmentIn(department_name="Zeta"))

    deleted_department = delete_department(department.id)

    assert not Department.objects.filter(department_name="Zeta").exists()
    assert deleted_department == "Zeta"


@pytest.mark.django_db
@pytest.mark.service
def test_delete_department_not_found_raises():
    """
    Deleting a department that does not exist should raise an error.
    """
    with pytest.raises(DepartmentDoesNotExist):
        delete_department(999)
