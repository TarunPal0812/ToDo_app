from uuid import UUID
from fastapi import APIRouter, status
from app.schemas.todo import TodoResponse, TodoCreate, TodoUpdate

from app.dependencies.todo_dependendecies import TodoServiceDependency

from app.schemas.general_response_schema import SuccessResponse
from app.utils.response import success_response

from app.dependencies.secutiry_dependencies import securityDependency
from app.errors.exceptions import TodoNotFound


router = APIRouter(prefix="/todos", tags=["ToDo"])


@router.get("/", response_model=SuccessResponse[list[TodoResponse]])
async def get_all_todos(service: TodoServiceDependency, current_user: securityDependency):
    todos = await service.get_all()
    return success_response(
        data= todos,
        message= f"Getting all the todos"
    )


@router.get("/{todo_id}", response_model=SuccessResponse[TodoResponse])
async def get_todo_by_id(service: TodoServiceDependency, todo_id: UUID):
    todo = await service.get_by_id(todo_id)
    if todo is None:
        raise TodoNotFound()
    return success_response(
        data= todo,
        message="Get the todo successfully..!!"
    )


@router.post("/", response_model=SuccessResponse[TodoResponse])
async def create_todo(service: TodoServiceDependency, todo_in: TodoCreate, current_user: securityDependency):
    user_id = current_user.id
    created_todo =  await service.create(todo_in, user_id)
    return success_response(
        # data= created_todo,
        message= "Todo created successfully"
    )

@router.patch("/{todo_id}", response_model=SuccessResponse[TodoResponse])
async def update_todo(service: TodoServiceDependency, todo_id: UUID, todo_in: TodoUpdate):
    todo = await service.update(todo_id, todo_in)
    if todo is None:
        raise TodoNotFound()
    return success_response(
        data= todo,
        message="successfully update the todo..!!"
    )


@router.delete("/{todo_id}")
async def delete_todo(service: TodoServiceDependency, todo_id: UUID):
    deleted = await service.delete(todo_id)
    if not deleted:
        raise TodoNotFound()
    return success_response(message= "Todo deleted successfully")
