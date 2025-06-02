from sqlalchemy import Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from fastapi_users.db import SQLAlchemyBaseUserTable
from .types import TaskStatus
from .utils.time_utils import get_datetime_now
from datetime import datetime



class Base(AsyncAttrs,DeclarativeBase):
    __abstract__ = True

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")



class Task(Base, AsyncAttrs):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    status : Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False, default=TaskStatus.NEW)
    due_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=get_datetime_now)
    history: Mapped[list["TaskHistory"]] = relationship("TaskHistory", back_populates="task", cascade="all, delete-orphan")
    owner: Mapped["User"] = relationship("User", back_populates="tasks")


class TaskHistory(Base, AsyncAttrs):
    __tablename__ = "task_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=get_datetime_now)
    due_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    task: Mapped["Task"] = relationship("Task", back_populates="history")