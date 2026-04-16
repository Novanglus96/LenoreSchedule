import pytest
from options.factories import PayrollInfoFactory
from options.models import PayrollInfo

AUTH = {"Authorization": "Bearer test-api-key"}
BASE = "/options/payroll_infos"


# ---------------------------------------------------------------------------
# POST /create
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_create_payroll_info_success(api_client):
    """Test that a payroll_info is created successfully."""
    response = api_client.post(
        f"{BASE}/create",
        json={
            "payroll_year": 2025,
            "payroll_start": "2025-01-01",
            "payroll_frequency": "weekly",
        },
        headers=AUTH,
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert PayrollInfo.objects.filter(payroll_year=2025).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_create_payroll_info_duplicate_year_returns_400(api_client):
    """Test that creating a payroll_info with a duplicate year returns 400."""
    PayrollInfoFactory(payroll_year=2025)

    response = api_client.post(
        f"{BASE}/create",
        json={
            "payroll_year": 2025,
            "payroll_start": "2025-01-01",
            "payroll_frequency": "weekly",
        },
        headers=AUTH,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "PayrollInfo already exists"


@pytest.mark.django_db
@pytest.mark.api
def test_create_payroll_info_invalid_start_returns_400(api_client):
    """Test that a start date two years before the payroll year returns 400."""
    response = api_client.post(
        f"{BASE}/create",
        json={
            "payroll_year": 2025,
            "payroll_start": "2023-01-01",
            "payroll_frequency": "weekly",
        },
        headers=AUTH,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid payroll start date"


@pytest.mark.django_db
@pytest.mark.api
def test_create_payroll_info_monthly_without_first_day_returns_400(api_client):
    """Test that a monthly payroll_info without first_day returns 400."""
    response = api_client.post(
        f"{BASE}/create",
        json={
            "payroll_year": 2025,
            "payroll_start": "2025-01-01",
            "payroll_frequency": "monthly",
        },
        headers=AUTH,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid first day"


@pytest.mark.django_db
@pytest.mark.api
def test_create_payroll_info_semi_monthly_without_second_day_returns_400(api_client):
    """Test that a semi-monthly payroll_info without second_day returns 400."""
    response = api_client.post(
        f"{BASE}/create",
        json={
            "payroll_year": 2025,
            "payroll_start": "2025-01-01",
            "payroll_frequency": "semi-monthly",
            "first_day": 1,
        },
        headers=AUTH,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid second day"


# ---------------------------------------------------------------------------
# PUT /update/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_update_payroll_info_success(api_client):
    """Test that a payroll_info is updated successfully."""
    existing = PayrollInfoFactory(payroll_year=2024)

    response = api_client.put(
        f"{BASE}/update/{existing.id}",
        json={
            "payroll_year": 2025,
            "payroll_start": "2025-01-01",
            "payroll_frequency": "biweekly",
        },
        headers=AUTH,
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}


@pytest.mark.django_db
@pytest.mark.api
def test_update_payroll_info_not_found_returns_404(api_client):
    """Test that updating a non-existent payroll_info returns 404."""
    response = api_client.put(
        f"{BASE}/update/99999",
        json={
            "payroll_year": 2025,
            "payroll_start": "2025-01-01",
            "payroll_frequency": "weekly",
        },
        headers=AUTH,
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_update_payroll_info_duplicate_year_returns_400(api_client):
    """Test that updating a payroll_info to an existing year returns 400."""
    PayrollInfoFactory(payroll_year=2025)
    existing = PayrollInfoFactory(payroll_year=2024)

    response = api_client.put(
        f"{BASE}/update/{existing.id}",
        json={
            "payroll_year": 2025,
            "payroll_start": "2025-01-01",
            "payroll_frequency": "weekly",
        },
        headers=AUTH,
    )

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# GET /get/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_get_payroll_info_success(api_client):
    """Test that a payroll_info is retrieved successfully."""
    existing = PayrollInfoFactory(payroll_year=2025)

    response = api_client.get(
        f"{BASE}/get/{existing.id}",
        headers=AUTH,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == existing.id
    assert data["payroll_year"] == 2025
    assert "payroll_start" in data
    assert "payroll_frequency" in data


@pytest.mark.django_db
@pytest.mark.api
def test_get_payroll_info_not_found_returns_404(api_client):
    """Test that getting a non-existent payroll_info returns 404."""
    response = api_client.get(
        f"{BASE}/get/99999",
        headers=AUTH,
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /list
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_list_payroll_infos_success(api_client):
    """Test that payroll_infos are listed successfully."""
    PayrollInfoFactory(payroll_year=2024)
    PayrollInfoFactory(payroll_year=2025)

    response = api_client.get(f"{BASE}/list", headers=AUTH)

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
@pytest.mark.api
def test_list_payroll_infos_ordered_descending(api_client):
    """Test that payroll_infos are returned in descending year order."""
    PayrollInfoFactory(payroll_year=2023)
    PayrollInfoFactory(payroll_year=2025)
    PayrollInfoFactory(payroll_year=2024)

    response = api_client.get(f"{BASE}/list", headers=AUTH)

    years = [item["payroll_year"] for item in response.json()]
    assert years == [2025, 2024, 2023]


@pytest.mark.django_db
@pytest.mark.api
def test_list_payroll_infos_empty(api_client):
    """Test that listing payroll_infos returns an empty list when none exist."""
    response = api_client.get(f"{BASE}/list", headers=AUTH)

    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# DELETE /delete/{id}
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.api
def test_delete_payroll_info_success(api_client):
    """Test that a payroll_info is deleted successfully."""
    existing = PayrollInfoFactory(payroll_year=2025)

    response = api_client.delete(
        f"{BASE}/delete/{existing.id}",
        headers=AUTH,
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert not PayrollInfo.objects.filter(id=existing.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_payroll_info_not_found_returns_404(api_client):
    """Test that deleting a non-existent payroll_info returns 404."""
    response = api_client.delete(
        f"{BASE}/delete/99999",
        headers=AUTH,
    )

    assert response.status_code == 404
