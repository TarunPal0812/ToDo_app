from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.schemas.todo import TodoResponse, TodoCreate, TodoUpdate

from app.dependencies.todo_dependendecies import TodoServiceDependency


router = APIRouter(prefix="/todos", tags=["ToDo"])


@router.get("/", response_model=list[TodoResponse])
async def get_all_todos(service: TodoServiceDependency):
    return await service.get_all()


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo_by_id(service: TodoServiceDependency, todo_id: UUID):
    todo = await service.get_by_id(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found..!!"
        )
    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(service: TodoServiceDependency, todo_in: TodoCreate):
    return await service.create(todo_in)


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(service: TodoServiceDependency, todo_id: UUID, todo_in: TodoUpdate):
    todo = await service.update(todo_id, todo_in)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found..!!"
        )
    return todo


@router.delete("/{todo_id}")
async def delete_todo(service: TodoServiceDependency, todo_id: UUID):
    deleted = await service.delete(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found..!!"
        )
    return {"message": "Todo deleted successfully"}
