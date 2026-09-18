from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.tasks.models import Task, TaskStatus
from app.domain.tasks.schemas import TaskCreate
from app.infrastructure.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def create_task(self, data: TaskCreate) -> Task:
        task = Task(
            id=uuid4(),
            description=data.description,
            status=TaskStatus.PENDING,
            created_at=datetime.now(UTC),
        )

        return await self._repository.create(task)

    async def get_task(self, task_id: UUID) -> Task | None:
        return await self._repository.get_by_id(task_id)
