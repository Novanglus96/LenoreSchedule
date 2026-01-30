import pytest
from staff.models import Holiday
from staff.factories import HolidayFactory


@pytest.mark.django_db
@pytest.mark.api
def test_create_holiday_success(api_client):
    """
    Test holiday created succssfully.
    """
    response = api_client.post(
        "/holidays/create",
        json={
            "holiday_name": "New Holiday",
            "rule_type": "fixed_day",
            "observed_rule": "none",
            "month": 1,
            "day": 1,
            "weekday": 0,
            "weel": 1,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.django_db
@pytest.mark.api
def test_get_holiday_success(api_client):
    """
    Test getting a holiday is successful.
    """
    holiday = HolidayFactory()
    response = api_client.get(
        f"/holidays/get/{holiday.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["holiday_name"] == holiday.holiday_name


@pytest.mark.django_db
@pytest.mark.api
def test_get_holiday_not_found(api_client):
    """
    Test getting a holiday that doesn't exist raises error.
    """
    response = api_client.get(
        "/holidays/get/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_list_holidays(api_client):
    """
    Test list of holidays is retrieved and ordered.
    """
    HolidayFactory(holiday_name="B Holiday")
    HolidayFactory(holiday_name="A Holiday")

    response = api_client.get(
        "/holidays/list", headers={"Authorization": "Bearer test-api-key"}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["holiday_name"] == "A Holiday"
    assert data[1]["holiday_name"] == "B Holiday"


@pytest.mark.django_db
@pytest.mark.api
def test_update_holiday_success(api_client):
    """
    Test updating a holiday is successful.
    """
    holiday = HolidayFactory()
    response = api_client.put(
        f"/holidays/update/{holiday.id}",
        json={
            "holiday_name": "Updated Name",
            "rule_type": "fixed_day",
            "observed_rule": "none",
            "month": 1,
            "day": 1,
            "weekday": 0,
            "weel": 1,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    holiday.refresh_from_db()
    assert holiday.holiday_name == "Updated Name"


@pytest.mark.django_db
@pytest.mark.api
def test_update_holiday_duplicate(api_client):
    """
    Test updating a holiday with a duplicate name raises error.
    """
    holiday1 = HolidayFactory(holiday_name="Holiday1")
    HolidayFactory(holiday_name="Holiday2")

    response = api_client.put(
        f"/holidays/update/{holiday1.id}",
        json={
            "holiday_name": "Holiday2",
            "rule_type": "fixed_day",
            "observed_rule": "none",
            "month": 1,
            "day": 1,
            "weekday": 0,
            "weel": 1,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Holiday not updated: holiday name exists"
    )


@pytest.mark.django_db
@pytest.mark.api
def test_update_holiday_not_found(api_client):
    """
    Test upraing a holiday that doesn't exist raises error.
    """
    response = api_client.put(
        "/holidays/update/999",
        json={
            "holiday_name": "New Holiday",
            "rule_type": "fixed_day",
            "observed_rule": "none",
            "month": 1,
            "day": 1,
            "weekday": 0,
            "weel": 1,
        },
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_delete_holiday_success(api_client):
    """
    Test deleting a holiday is successful.
    """
    holiday = HolidayFactory()
    response = api_client.delete(
        f"/holidays/delete/{holiday.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not Holiday.objects.filter(id=holiday.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_holiday_not_found(api_client):
    """
    Test deleting a holiday that doesn't exist raises error.
    """
    response = api_client.delete(
        "/holidays/delete/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404
