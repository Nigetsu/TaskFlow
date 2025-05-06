from datetime import datetime, date, timezone
from enum import Enum
from typing import List, Optional
from sqlalchemy import (
    String, Text, ForeignKey,
    Enum as SQLAlchemyEnum,
    DateTime, Date, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    authored_tasks: Mapped["Task"] = relationship(back_populates="author", foreign_keys="Task.author_id")
    assigned_tasks: Mapped["Task"] = relationship(back_populates="assignee", foreign_keys="Task.assignee_id")
    watching_tasks: Mapped[List["Task"]] = relationship(secondary="task_watchers", back_populates="watchers")
    executing_tasks: Mapped[List["Task"]] = relationship(secondary="task_executors", back_populates="executors")


class TaskStatus(str, Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(SQLAlchemyEnum(TaskStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    column_id: Mapped[Optional[int]] = mapped_column(ForeignKey("columns.id"))
    sprint_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sprints.id"))
    board_id: Mapped[Optional[int]] = mapped_column(ForeignKey("boards.id"))
    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("groups.id"))

    author: Mapped["User"] = relationship(back_populates="authored_tasks", foreign_keys=[author_id])
    assignee: Mapped[Optional["User"]] = relationship(back_populates="assigned_tasks", foreign_keys=[assignee_id])
    column: Mapped[Optional["Column"]] = relationship(back_populates="tasks")
    sprint: Mapped[Optional["Sprint"]] = relationship(back_populates="tasks")
    board: Mapped[Optional["Board"]] = relationship(back_populates="tasks")
    group: Mapped[Optional["Group"]] = relationship(back_populates="tasks")
    watchers: Mapped[List["User"]] = relationship(secondary="task_watchers", back_populates="watching_tasks")
    executors: Mapped[List["User"]] = relationship(secondary="task_executors", back_populates="executing_tasks")


class TaskWatcher(Base):
    __tablename__ ="task_watchers"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class TaskExecutor(Base):
    __tablename__ = "task_executors"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    columns: Mapped[List["Column"]] = relationship(back_populates="board", cascade="all, delete-orphan")
    tasks: Mapped[List["Task"]] = relationship(back_populates="board")


class Column(Base):
    __tablename__ = "columns"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), nullable=False)

    board: Mapped["Board"] = relationship(back_populates="columns")
    tasks: Mapped[List["Task"]] = relationship(back_populates="columns")


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)

    __table_args__ = (
        CheckConstraint('end_date > start_date', name='check_sprint_dates'),
    )

    tasks: Mapped[List["Task"]] = relationship(back_populates="sprint")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    tasks: Mapped[List["Task"]] = relationship(back_populates="group")
