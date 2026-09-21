from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from sqlalchemy import select
from typing import Any

class TodoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, todo: Todo) -> Todo:
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)

        return todo

    async def get_all(self) -> list[Todo]:
        result = await self.db.execute(select(Todo).order_by(Todo.id))
        return list(result.scalars().all())

    async def get_by_id(self, todo_id: UUID) -> Todo | None:
        return await self.db.get(Todo, todo_id)

    async def update(self, todo: Todo, updated_data: dict[str, Any]) -> Todo:
        for key, value in updated_data.items():
            if hasattr(todo,key):
                setattr(todo,key,value)

        await self.db.commit()
        await self.db.refresh(todo)

        return todo

    async def delete(self, todo: Todo) -> None:
        await self.db.delete(todo)
        await self.db.commit()


    

