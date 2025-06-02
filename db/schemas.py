from pydantic import BaseModel, EmailStr
from typing import Optional

from .types import TaskStatus
from datetime import datetime

from fastapi_users import schemas

class User(schemas.BaseUser[int]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserResponse(BaseModel):
    email: EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str


class baseTask(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    title: str
    description: str
    due_time: datetime
    status: TaskStatus

class TaskCreate(BaseModel):
    title: str
    description: str
    due_time: datetime
    status: TaskStatus = TaskStatus.NEW

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_time: Optional[datetime] = None
    status: Optional[TaskStatus] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    title: str
    description: str
    due_time: datetime
    status: TaskStatus
    

class TaskHistoryCreate(BaseModel):
    task_id: int
    status: TaskStatus


class TaskHistoryResponse(BaseModel):
    id: int
    task_id: int
    status: TaskStatus
    due_time: datetime
    created_at: datetime