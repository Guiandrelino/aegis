from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_task() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "description": "Analyze the AI agent market.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["description"] == "Analyze the AI agent market."
    assert data["status"] == "pending"
    assert UUID(data["id"])
    assert "created_at" in data


def test_create_task_rejects_empty_description() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "description": "",
        },
    )

    assert response.status_code == 422


def test_get_task() -> None:
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "description": "Persist task in PostgreSQL.",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["description"] == "Persist task in PostgreSQL."
    assert data["status"] == "pending"


def test_get_task_not_found() -> None:
    response = client.get(
        "/api/v1/tasks/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
