from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.domain.tasks.schemas import TaskCreate, TaskResponse
from app.infrastructure.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def get_task_service(
    session: AsyncSession = Depends(get_db_session),
) -> TaskService:
    repository = TaskRepository(session)

    return TaskService(repository)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = await service.create_task(data)

    return TaskResponse(
        id=task.id,
        description=task.description,
        status=task.status,
        created_at=task.created_at,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = await service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse(
        id=task.id,
        description=task.description,
        status=task.status,
        created_at=task.created_at,
    )
