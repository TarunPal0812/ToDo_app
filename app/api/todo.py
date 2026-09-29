from uuid import UUID
from fastapi import APIRouter, Query, BackgroundTasks
from app.schemas.todo import TodoResponse, TodoCreate, TodoUpdate, TodoListParams

from app.dependencies.todo_dependendecies import TodoServiceDependency

from app.schemas.general_response_schema import SuccessResponse
from app.utils.response import success_response

from app.dependencies.secutiry_dependencies import securityDependency
from app.errors.exceptions import TodoNotFound

from typing import Annotated
import os
import json
import tempfile
from app.utils.process_mail import process_export_mail


router = APIRouter(prefix="/todos", tags=["ToDo"])


@router.get("/", response_model=SuccessResponse[list[TodoResponse]])
async def get_all_todos(service: TodoServiceDependency, current_user: securityDependency, filters: Annotated[TodoListParams, Query()]):
    user_id = current_user.id
    todos, total = await service.get_all(user_id = user_id, filters = filters)
    
    total_pages = (total + filters.limit - 1) // filters.limit
    return success_response(data=todos, message="Todos fetched successfully", meta={
        "page": filters.page,
        "limit": filters.limit,
        "total_items": total,
        "total_pages": total_pages,
        "has_next": filters.page < total_pages,
        "has_previous": filters.page > 1
    })

@router.get("/export")
async def export_as_json(
    service: TodoServiceDependency, 
    current_user: securityDependency,
    background_tasks: BackgroundTasks
):
    todos = await service.get_all_todos(user_id= current_user.id)
    
    # Serialize the sqlalchemy models to standard dicts
    todos_list = [TodoResponse.model_validate(t).model_dump(mode="json") for t in todos]
    
    # Ensure temp directory exists in the project root
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Create temp file in the project's temp directory
    fd, filepath = tempfile.mkstemp(suffix=".json", dir=temp_dir)
    with os.fdopen(fd, 'w') as f:
        json.dump(todos_list, f, indent=4)
        
    background_tasks.add_task(process_export_mail, current_user.email, filepath)
    
    return success_response(message="Export initiated. You will receive an email shortly with the JSON file.")


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

