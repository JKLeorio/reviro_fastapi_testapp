from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import delete, select
from db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Task, User, TaskHistory
from db.schemas import TaskHistoryResponse
from typing import List
from .auth import current_user


router = APIRouter()

@router.get("/task/{task_id}/history/", response_model=List[TaskHistoryResponse])
async def get_task_history(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    """Get the history of a specific task.
    Ensure the task belongs to the current user."""
    
    task = await session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    history = await session.execute(
        select(TaskHistory).where(TaskHistory.task_id == task_id)
    )
    
    return history.scalars().all()

# @router.post("/task/history/",
#               response_model=TaskHistoryResponse,
#               status_code=status.HTTP_201_CREATED
#               )
# async def create_task_history(
#     task_history_data: TaskHistoryCreate,
#     session: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(current_user)
# ):
#     task = await session.get(Task, task_history_data.task_id)
#     if not task or task.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
#     new_history = TaskHistory(
#         task_id=task_history_data.task_id,
#         status=task_history_data.status,
#         due_time=task.due_time
#     )
    
#     session.add(new_history)
#     await session.commit()
#     await session.refresh(new_history)
    
#     return new_history

@router.delete("/task/{task_id}/history/",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_history(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    """Delete all history entries for a specific task.
    Ensure the task belongs to the current user."""

    task = await session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or you do not have permission to delete this history")
    
    history = await session.execute(
        select(TaskHistory).where(TaskHistory.task_id == task_id)
    )
    
    if not history.scalars().all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="history not found for this task")
    
    await session.execute(delete(TaskHistory).where(TaskHistory.task_id == task_id))
    
    await session.commit()


@router.delete("/task/history/{history_id}/",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_history_by_id(
    history_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    """Delete a specific task history by its ID.
    Ensure the task belongs to the current user."""

    history = await session.get(TaskHistory, history_id)
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task history not found")
    
    task = await session.get(Task, history.task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or you do not have permission to delete this history")
    
    await session.delete(history)
    await session.commit()

