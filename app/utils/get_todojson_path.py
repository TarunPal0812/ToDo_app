from app.schemas.todo import TodoResponse
import os
import tempfile
import json


def get_todojson_file_path(todos):
    # Serialize the sqlalchemy models to standard dicts
    todos_list = [TodoResponse.model_validate(t).model_dump(mode="json") for t in todos]
    
    # Ensure temp directory exists in the project root
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Create temp file in the project's temp directory
    fd, filepath = tempfile.mkstemp(suffix=".json", dir=temp_dir)
    with os.fdopen(fd, 'w') as f:
        json.dump(todos_list, f, indent=4)

    return filepath