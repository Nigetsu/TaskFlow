from datetime import datetime, date, timezone
from enum import Enum
from typing import List
from sqlalchemy import (
    String, Text, ForeignKey,
    Enum as SQLAlchemyEnum,
    DateTime, Date, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    authored_tasks: Mapped["Task"] = relationship(back_populates="author", foreign_keys="Task.author_id")
    assigned_tasks: Mapped["Task"] = relationship(back_populates="assignee", foreign_keys="Task.assignee_id")
    watching_tasks: Mapped[List["Task"]] = relationship(secondary="TaskWatcher", back_populates="watchers")
    executing_tasks: Mapped[List["Task"]] = relationship(secondary="TaskExecutor", back_populates="executors")


class TaskStatus(str, Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class Task(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(SQLAlchemyEnum(TaskStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    column_id: Mapped[int | None] = mapped_column(ForeignKey("columns.id"))
    sprint_id: Mapped[int | None] = mapped_column(ForeignKey("sprints.id"))
    board_id: Mapped[int | None] = mapped_column(ForeignKey("boards.id"))
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"))

    author: Mapped["User"] = relationship(back_populates="authored_tasks", foreign_keys=[author_id])
    assignee: Mapped["User"] = relationship(back_populates="assigned_tasks", foreign_keys=[assignee_id])
    column: Mapped["Column"] = relationship(back_populates="tasks")
    sprint: Mapped["Sprint"] = relationship(back_populates="tasks")
    board: Mapped["Board"] = relationship(back_populates="tasks")
    group: Mapped["Group"] = relationship(back_populates="tasks")
    watchers: Mapped[List["User"]] = relationship(secondary="TaskWatcher", back_populates="watching_tasks")
    executors: Mapped[List["User"]] = relationship(secondary="TaskExecutor", back_populates="executing_tasks")


class TaskWatcher(Base):
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class TaskExecutor(Base):
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Board(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    columns: Mapped[List["Column"]] = relationship(back_populates="board", cascade="all, delete-orphan")
    tasks: Mapped[List["Task"]] = relationship(back_populates="board")


class Column(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), nullable=False)

    board: Mapped["Board"] = relationship(back_populates="columns")
    tasks: Mapped[List["Task"]] = relationship(back_populates="columns")


class Sprint(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)

    __table_args__ = (
        CheckConstraint('end_date > start_date', name='check_sprint_dates'),
    )

    tasks: Mapped[List["Task"]] = relationship(back_populates="sprint")


class Group(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    tasks: Mapped[List["Task"]] = relationship(back_populates="group")
