import pytest
from staff.models import Division
from staff.factories import DivisionFactory


@pytest.mark.django_db
@pytest.mark.api
def test_create_division_success(api_client):
    """
    Test division created succssfully.
    """
    response = api_client.post(
        "/divisions/create",
        json={"division_name": "New Division"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.django_db
@pytest.mark.api
def test_get_division_success(api_client):
    """
    Test getting a division is successful.
    """
    division = DivisionFactory()
    response = api_client.get(
        f"/divisions/get/{division.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["division_name"] == division.division_name


@pytest.mark.django_db
@pytest.mark.api
def test_get_division_not_found(api_client):
    """
    Test getting a division that doesn't exist raises error.
    """
    response = api_client.get(
        "/divisions/get/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_list_divisions(api_client):
    """
    Test list of divisions is retrieved and ordered.
    """
    DivisionFactory(division_name="B Division")
    DivisionFactory(division_name="A Division")

    response = api_client.get(
        "/divisions/list", headers={"Authorization": "Bearer test-api-key"}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["division_name"] == "A Division"
    assert data[1]["division_name"] == "B Division"


@pytest.mark.django_db
@pytest.mark.api
def test_update_division_success(api_client):
    """
    Test updating a division is successful.
    """
    division = DivisionFactory()
    response = api_client.put(
        f"/divisions/update/{division.id}",
        json={"division_name": "Updated Name"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    division.refresh_from_db()
    assert division.division_name == "Updated Name"


@pytest.mark.django_db
@pytest.mark.api
def test_update_division_duplicate(api_client):
    """
    Test updating a division with a duplicate name raises error.
    """
    division1 = DivisionFactory(division_name="Division1")
    DivisionFactory(division_name="Division2")

    response = api_client.put(
        f"/divisions/update/{division1.id}",
        json={"division_name": "Division2"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Division not updated: division name exists"
    )


@pytest.mark.django_db
@pytest.mark.api
def test_update_division_not_found(api_client):
    """
    Test upraing a division that doesn't exist raises error.
    """
    response = api_client.put(
        "/divisions/update/999",
        json={"division_name": "Division2"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_delete_division_success(api_client):
    """
    Test deleting a division is successful.
    """
    division = DivisionFactory()
    response = api_client.delete(
        f"/divisions/delete/{division.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not Division.objects.filter(id=division.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_division_not_found(api_client):
    """
    Test deleting a division that doesn't exist raises error.
    """
    response = api_client.delete(
        "/divisions/delete/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404
