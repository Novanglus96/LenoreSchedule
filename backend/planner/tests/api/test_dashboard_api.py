import pytest


@pytest.mark.django_db
@pytest.mark.api
def test_dashboard_summary_shape(api_client):
    response = api_client.get(
        "/dashboard/summary", headers={"Authorization": "Bearer test-api-key"}
    )

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {
        "week_start",
        "week_end",
        "vacations",
        "holidays",
        "unconfirmed",
        "unconfirmed_total",
        "birthdays",
    }
