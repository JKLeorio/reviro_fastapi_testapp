from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter
from db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Task, User, TaskHistory
from db.schemas import TaskCreate, TaskUpdate, TaskResponse
from typing import List, Optional
from .auth import current_user
from db.types import TaskStatus
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter





class TaskFilter(Filter):
    status: Optional[TaskStatus] = None
    due_time__gte: Optional[datetime] = None
    due_time__lte: Optional[datetime] = None
    class Constants(Filter.Constants):
        model = Task


router = APIRouter()


@router.get("/all_tasks/", response_model=List[TaskResponse])
async def get_task_list(
    task_filter: TaskFilter = FilterDepends(TaskFilter),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    '''Get a list of all tasks.
    Return a list of tasks filtered by optional filters.'''
    
    tasks = select(Task)
    query = task_filter.filter(tasks)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/tasks/", response_model=List[TaskResponse])
async def get_user_task_list(
    task_filter: TaskFilter = FilterDepends(TaskFilter),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    '''Get a list of tasks for the current user.
    Return a list of tasks filtered by the current user and optional filters.'''

    tasks = select(Task).where(Task.user_id == current_user.id)
    query = task_filter.filter(tasks)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    '''Get a task by its ID.
    Return exception if the task does not exist or does not belong to the current user.'''

    task = await session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or does not belong to the user")
    return task


@router.post("/task/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    '''Create a new task.
    Return the created task.'''

    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        due_time=task_data.due_time,
        status=task_data.status
    )
    session.add(new_task)
    await session.flush() 

    task_history = TaskHistory(
        task_id=new_task.id,
        status=new_task.status,
        due_time=new_task.due_time
    )
    session.add(task_history)

    await session.commit()
    await session.refresh(new_task)
    return new_task



@router.put("/task/{task_id}/", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    '''Update a task by its ID.
    Return exception if the task does not exist or does not belong to the current user.
    '''

    task = await session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    task_history = TaskHistory(task_id=task.id, status=task.status, due_time=task.due_time)
    session.add(task)
    session.add(task_history)
    await session.commit()
    await session.refresh(task)
    return task


@router.delete("/task/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    '''Delete a task by its ID.
    Return Exception if the task does not exist or does not belong to the current user.
    '''
    task = await session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    await session.delete(task)
    await session.commit()
    return {"detail": "Task deleted successfully"}

