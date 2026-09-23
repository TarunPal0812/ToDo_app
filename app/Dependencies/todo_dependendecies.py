from app.db.database import get_db
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.todo import TodoService
from app.repositories.todo import TodoRepository


def get_todo_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = TodoRepository(db)
    return TodoService(repo)


TodoServiceDependency = Annotated[TodoService, Depends(get_todo_service)]