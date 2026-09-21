from fastapi import FastAPI
from app.api.todo import router as todo_router

from contextlib import asynccontextmanager
from app.db.database import creat_table,engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await creat_table()
    yield
    await engine.dispose()
    

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {
        "message": "Ok"
    }

app.include_router(todo_router, prefix="/api/v1")