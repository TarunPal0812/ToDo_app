from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from sqlalchemy import select, func
from typing import Any

from app.schemas.todo import TodoListParams

class TodoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, todo: Todo) -> Todo:
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)

        return todo

    async def get_all(self,user_id: UUID, filters: TodoListParams) -> tuple[list[Todo],int]:

        conditions = [Todo.user_id == user_id]

        if filters.is_completed is not None:
            conditions.append(Todo.is_completed == filters.is_completed)
            

        count_stmt = select(func.count(Todo.id)).select_from(Todo).where(*conditions)
        total_count_result = await self.db.execute(count_stmt)

        total = total_count_result.scalar_one()

        sort_columns = {"created_at": Todo.created_at, "name": Todo.name}

        sort_column = sort_columns[filters.sort_by]

        ordering = (
            sort_column.asc() if filters.sort_order == "asc" else sort_column.desc()
        )

        offset = (filters.page - 1) * filters.limit
        limit = filters.limit

        todos_stmt = (
            select(Todo)
            .where(*conditions)
            .order_by(ordering)
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(todos_stmt)

        return list(result.scalars().all()), total
    
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


    

