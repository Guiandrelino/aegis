from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.domain.tasks.schemas import TaskCreate, TaskResponse
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

task_service = TaskService()


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(data: TaskCreate) -> TaskResponse:
    task = task_service.create_task(data)

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
async def get_task(task_id: UUID) -> TaskResponse:
    task = task_service.get_task(task_id)

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