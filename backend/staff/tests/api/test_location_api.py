import pytest
from staff.models import Location
from staff.factories import LocationFactory


@pytest.mark.django_db
@pytest.mark.api
def test_create_location_success(api_client):
    """
    Test location created succssfully.
    """
    response = api_client.post(
        "/locations/create",
        json={"location_name": "New Location"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.django_db
@pytest.mark.api
def test_get_location_success(api_client):
    """
    Test getting a location is successful.
    """
    location = LocationFactory()
    response = api_client.get(
        f"/locations/get/{location.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["location_name"] == location.location_name


@pytest.mark.django_db
@pytest.mark.api
def test_get_location_not_found(api_client):
    """
    Test getting a location that doesn't exist raises error.
    """
    response = api_client.get(
        "/locations/get/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_list_locations(api_client):
    """
    Test list of locations is retrieved and ordered.
    """
    LocationFactory(location_name="B Location")
    LocationFactory(location_name="A Location")

    response = api_client.get(
        "/locations/list", headers={"Authorization": "Bearer test-api-key"}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["location_name"] == "A Location"
    assert data[1]["location_name"] == "B Location"


@pytest.mark.django_db
@pytest.mark.api
def test_update_location_success(api_client):
    """
    Test updating a location is successful.
    """
    location = LocationFactory()
    response = api_client.put(
        f"/locations/update/{location.id}",
        json={"location_name": "Updated Name"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    location.refresh_from_db()
    assert location.location_name == "Updated Name"


@pytest.mark.django_db
@pytest.mark.api
def test_update_location_duplicate(api_client):
    """
    Test updating a location with a duplicate name raises error.
    """
    location1 = LocationFactory(location_name="Location1")
    LocationFactory(location_name="Location2")

    response = api_client.put(
        f"/locations/update/{location1.id}",
        json={"location_name": "Location2"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Location not updated: location name exists"
    )


@pytest.mark.django_db
@pytest.mark.api
def test_update_location_not_found(api_client):
    """
    Test upraing a location that doesn't exist raises error.
    """
    response = api_client.put(
        "/locations/update/999",
        json={"location_name": "Location2"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_delete_location_success(api_client):
    """
    Test deleting a location is successful.
    """
    location = LocationFactory()
    response = api_client.delete(
        f"/locations/delete/{location.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not Location.objects.filter(id=location.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_location_not_found(api_client):
    """
    Test deleting a location that doesn't exist raises error.
    """
    response = api_client.delete(
        "/locations/delete/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404
