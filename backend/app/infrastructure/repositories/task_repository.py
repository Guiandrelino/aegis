from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tasks.models import Task, TaskStatus
from app.infrastructure.persistence.models.task import TaskORM


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, task: Task) -> Task:
        task_model = TaskORM(
            id=task.id,
            description=task.description,
            status=task.status.value,
            created_at=task.created_at,
        )

        self._session.add(task_model)
        await self._session.commit()
        await self._session.refresh(task_model)

        return self._to_domain(task_model)

    async def get_by_id(self, task_id: UUID) -> Task | None:
        result = await self._session.execute(
            select(TaskORM).where(TaskORM.id == task_id)
        )

        task_model = result.scalar_one_or_none()

        if task_model is None:
            return None

        return self._to_domain(task_model)

    async def list_all(self) -> Sequence[Task]:
        result = await self._session.execute(
            select(TaskORM).order_by(TaskORM.created_at.desc())
        )

        return [
            self._to_domain(task_model)
            for task_model in result.scalars().all()
        ]

    @staticmethod
    def _to_domain(task_model: TaskORM) -> Task:
        return Task(
            id=task_model.id,
            description=task_model.description,
            status=TaskStatus(task_model.status),
            created_at=task_model.created_at,
        )
