from fastapi import APIRouter

router = APIRouter(tags=["ToDo"])

@router.get("/todos")
async def get_all_todos():
    return {
        "message": "all todos are returnd.."
    }

@router.get("/todo/{todo_id}")
async def get_todo():
    pass

@router.post("/create")
async def create_todo():
    pass

@router.patch("/update/{todo_id}")
async def update_todo():
    pass

@router.delete("/delete/{toto_id}")
async def delete_todo():
    pass



