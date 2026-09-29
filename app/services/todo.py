from uuid import UUID
from fastapi import status

from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate, TodoListParams
from app.models.todo import Todo
from app.errors.exceptions import TodoAlreadyExist



class TodoService:
    def __init__(self, repo: TodoRepository) -> None:
        self.repo = repo

    async def create(self, todo_in: TodoCreate, user_id: UUID) -> Todo:
        try:
            return await self.repo.create(Todo(**todo_in.model_dump(),user_id = user_id))
        except:
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT,
            #     detail=f"Todo with name '{todo_in.name}' already exists."
            # )
            raise TodoAlreadyExist()

    async def get_all(self,user_id: UUID, filters: TodoListParams) -> tuple[list[Todo], int]:
        return await self.repo.get_all(user_id, filters)

    async def get_by_id(self, todo_id: UUID) -> Todo | None:
        return await self.repo.get_by_id(todo_id)

    async def update(self, todo_id: UUID, todo_in: TodoUpdate) -> Todo | None:
        todo_to_update = await self.repo.get_by_id(todo_id)
        if not todo_to_update:
            return None

        update_data = todo_in.model_dump(exclude_unset=True)

        if not update_data:
            return todo_to_update

        try:
            return await self.repo.update(todo_to_update, update_data)
        except:
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT,
            #     detail=f"Todo with name '{todo_in.name}' already exists."
            # )
            raise TodoAlreadyExist()

    async def delete(self, todo_id: UUID) -> bool:
        todo_to_delete = await self.repo.get_by_id(todo_id)
        if not todo_to_delete:
            return False

        await self.repo.delete(todo_to_delete)
        return True
