from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain.tasks.models import TaskStatus


class Base(DeclarativeBase):
    pass


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    description: Mapped[str] = mapped_column(
        String(10_000),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=TaskStatus.PENDING.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
