import pytest
from groups.models import Group
from groups.factories import GroupFactory


@pytest.mark.django_db
@pytest.mark.api
def test_create_group_success(api_client):
    response = api_client.post(
        "/groups/create",
        json={"group_name": "New Group"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.django_db
@pytest.mark.api
def test_get_group_success(api_client):
    group = GroupFactory()
    response = api_client.get(
        f"/groups/get/{group.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["group_name"] == group.group_name


@pytest.mark.django_db
@pytest.mark.api
def test_get_group_not_found(api_client):
    response = api_client.get(
        "/groups/get/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_list_groups(api_client):
    GroupFactory(group_name="B Group")
    GroupFactory(group_name="A Group")

    response = api_client.get(
        "/groups/list", headers={"Authorization": "Bearer test-api-key"}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["group_name"] == "A Group"
    assert data[1]["group_name"] == "B Group"


@pytest.mark.django_db
@pytest.mark.api
def test_update_group_success(api_client):
    group = GroupFactory()
    response = api_client.put(
        f"/groups/update/{group.id}",
        json={"group_name": "Updated Name"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    group.refresh_from_db()
    assert group.group_name == "Updated Name"


@pytest.mark.django_db
@pytest.mark.api
def test_update_group_duplicate(api_client):
    group1 = GroupFactory(group_name="Group1")
    GroupFactory(group_name="Group2")

    response = api_client.put(
        f"/groups/update/{group1.id}",
        json={"group_name": "Group2"},
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Group already exists"


@pytest.mark.django_db
@pytest.mark.api
def test_delete_group_success(api_client):
    group = GroupFactory()
    response = api_client.delete(
        f"/groups/delete/{group.id}",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not Group.objects.filter(id=group.id).exists()


@pytest.mark.django_db
@pytest.mark.api
def test_delete_group_not_found(api_client):
    response = api_client.delete(
        "/groups/delete/9999",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404
