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
    assert "id" in data
    assert "created_at" in data


def test_create_task_rejects_empty_description() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "description": "",
        },
    )

    assert response.status_code == 422