from fastapi import FastAPI
from app.api.todo import router as todo_router

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Ok"
    }

app.include_router(todo_router, prefix="/api/todo")