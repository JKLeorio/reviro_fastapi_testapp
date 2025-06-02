import pytest

TASK_DATA = {
        "id": 1,
        "user_id": 1,
        "title": "Test Task",
        "description": "This is a test task.",
        "due_time": "2023-12-31T23:59:59",
        "status": "new"
    }

TASK_CREATE_DATA = {
        "title": "Test Task",
        "description": "This is a test task.",
        "due_time": "2023-12-31T23:59:59"
    }

TASK_UPDATE_DATA = {
        "title": "Updated Task",
        "description": "This is an updated test task.",
        "due_time": "2024-01-01T00:00:00",
        "status": "in_progress"
    }

TASK_HISTORY_DATA = {
        "id": 1,
        "task_id": 1,
        "status": "new",
        "due_time": "2023-12-31T23:59:59",
    }

TASK_HISTORY_UPDATE_DATA = {
        "id": 2,
        "task_id": 1,
        "status": "in_progress",
        "due_time": "2024-01-01T00:00:00",
    }

@pytest.mark.asyncio
async def test_task_creation(client, auth_token):
    task_data = TASK_CREATE_DATA

    response = await client.post(
        "/api/task/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == "new"
    assert data["due_time"] == task_data["due_time"]

@pytest.mark.asyncio
async def test_task_list(client, auth_token):
    response = await client.get(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_task_detail(client, auth_token):
    task_data = TASK_DATA
    response = await client.get(
        f"/api/task/{task_data['id']}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_data["id"]
    assert data["user_id"] == task_data["user_id"]
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]
    assert data["due_time"] == task_data["due_time"]

@pytest.mark.asyncio
async def test_task_history_list(client, auth_token):
    task_data = TASK_DATA
    task_history_data = TASK_HISTORY_DATA

    response = await client.get(
        f"/api/task/{task_data['id']}/history/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    task_history = data[0]
    assert task_history["id"] == task_history_data["id"]
    assert task_history["task_id"] == task_history_data["task_id"]
    assert task_history["status"] == task_history_data["status"]
    assert task_history["due_time"] == task_history_data["due_time"]



@pytest.mark.asyncio
async def test_task_update(client, auth_token):
    task_data = TASK_DATA
    update_data = TASK_UPDATE_DATA

    response = await client.put(
        f"/api/task/{task_data['id']}/",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_data["id"]
    assert data["user_id"] == task_data["user_id"]
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["status"] == update_data["status"]
    assert data["due_time"] == update_data["due_time"]

@pytest.mark.asyncio
async def test_task_history_after_task_update(client, auth_token):
    task_data = TASK_DATA
    task_history_data = TASK_HISTORY_UPDATE_DATA

    response = await client.get(
        f"/api/task/{task_data['id']}/history/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for task_history in data:
        print(task_history)
        if task_history["id"] == task_history_data["id"]:
            break
    assert task_history["id"] == task_history_data["id"]
    assert task_history["task_id"] == task_history_data["task_id"]
    assert task_history["status"] == task_history_data["status"]
    assert task_history["due_time"] == task_history_data["due_time"]

@pytest.mark.asyncio
async def test_task_history_deletion_by_id(client, auth_token):
    task_data = TASK_DATA
    task_history_data = TASK_HISTORY_DATA

    response = await client.delete(
        f"/api/task/history/{task_history_data['id']}/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204

    response = await client.get(
        f"/api/task/{task_data['id']}/history/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert not any(history["id"] == task_history_data["id"] for history in data)

@pytest.mark.asyncio
async def test_task_history_deletion_by_task_id(client, auth_token):
    task_data = TASK_DATA

    response = await client.delete(
        f"/api/task/{task_data['id']}/history/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204

    response = await client.get(
        f"/api/task/{task_data['id']}/history/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert not data


@pytest.mark.asyncio
async def test_task_deletion(client, auth_token):
    task_data = TASK_DATA

    response = await client.delete(
        f"/api/task/{task_data['id']}/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204

    response = await client.get(
        f"/api/task/{task_data['id']}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404