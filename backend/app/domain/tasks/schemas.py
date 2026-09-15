from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.tasks.models import TaskStatus


class TaskCreate(BaseModel):
    description: str = Field(
        min_length=1,
        max_length=10_000,
        description="Natural language description of the task.",
    )


class TaskResponse(BaseModel):
    id: UUID
    description: str
    status: TaskStatus
    created_at: datetime
