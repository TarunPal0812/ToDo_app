import time
from fastapi import FastAPI, Request
from app.api.todo import router as todo_router
from app.api.user import router as user_router

from contextlib import asynccontextmanager
from app.db.database import creat_table, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await creat_table()
    yield
    await engine.dispose()
    

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def calculate_request_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    total_time = time.perf_counter() - start_time
    print(f"Request: {request.method} {request.url.path} | Time taken: {total_time:.4f}s")
    response.headers["X-Process-Time"] = str(total_time)
    return response


@app.get("/")
async def root():
    return {
        "message": "Ok"
    }

app.include_router(todo_router, prefix="/api/v1")
app.include_router(user_router, prefix= "/api/v1")