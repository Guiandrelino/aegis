from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.tasks.models import Task, TaskStatus
from app.domain.tasks.schemas import TaskCreate


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def create_task(self, data: TaskCreate) -> Task:
        task = Task(
            id=uuid4(),
            description=data.description,
            status=TaskStatus.PENDING,
            created_at=datetime.now(UTC),
        )

        self._tasks[task.id] = task

        return task

    def get_task(self, task_id: UUID) -> Task | None:
        return self._tasks.get(task_id)