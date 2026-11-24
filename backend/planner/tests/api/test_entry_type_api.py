import pytest

from planner.models import EntryType

AUTH = {"Authorization": "Bearer test-api-key"}


@pytest.mark.django_db
@pytest.mark.api
def test_create_entry_type_success(api_client):
    response = api_client.post(
        "/entry_types/create",
        json={"name": "Jury Duty", "code": "jry"},
        headers=AUTH,
    )

    assert response.status_code == 200
    assert EntryType.objects.filter(name="Jury Duty", code="JRY").exists()


@pytest.mark.django_db
@pytest.mark.api
def test_list_update_delete_entry_type(api_client):
    et = EntryType.objects.create(name="Training", code="TRN")

    listed = api_client.get("/entry_types/list", headers=AUTH)
    assert listed.status_code == 200
    assert any(t["id"] == et.id for t in listed.json())

    updated = api_client.put(
        f"/entry_types/update/{et.id}",
        json={"name": "Training Day", "code": "TRD"},
        headers=AUTH,
    )
    assert updated.status_code == 200
    et.refresh_from_db()
    assert (et.name, et.code) == ("Training Day", "TRD")

    deleted = api_client.delete(f"/entry_types/delete/{et.id}", headers=AUTH)
    assert deleted.status_code == 200
    assert not EntryType.objects.filter(id=et.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_create_entry_type_duplicate_code(api_client):
    EntryType.objects.create(name="Vacation Plus", code="VCP")
    response = api_client.post(
        "/entry_types/create",
        json={"name": "Something Else", "code": "VCP"},
        headers=AUTH,
    )
    assert response.status_code == 400
