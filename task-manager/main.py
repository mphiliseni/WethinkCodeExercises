from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import json
import os

# ==== FastAPI App Config ====
app = FastAPI(
    title="Task Manager API",
    description="A FastAPI-powered web version of the Task Manager CLI app.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# ==== Storage ====
TASKS_FILE = "tasks.json"

# ==== Models ====
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    priority: int = Field(ge=1, le=5)
    due: Optional[str] = None  # ISO 8601 date string
    tags: List[str] = []
    status: str = "todo"
    created_at: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: int = Field(ge=1, le=5)
    due: Optional[str] = None
    tags: List[str] = []

# ==== Utility ====
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def generate_id(tasks):
    if not tasks:
        return "1"
    max_id = max(int(task["id"]) for task in tasks)
    return str(max_id + 1)

# ==== Routes ====

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return load_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task_data: TaskCreate):
    tasks = load_tasks()
    task = {
        "id": generate_id(tasks),
        "title": task_data.title,
        "description": task_data.description,
        "priority": task_data.priority,
        "due": task_data.due,
        "tags": task_data.tags,
        "status": "todo",
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}/status", response_model=Task)
def update_status(task_id: str, new_status: str):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/stats")
def get_statistics():
    tasks = load_tasks()
    now = datetime.now()
    return {
        "total": len(tasks),
        "todo": len([t for t in tasks if t["status"] == "todo"]),
        "in_progress": len([t for t in tasks if t["status"] == "in_progress"]),
        "review": len([t for t in tasks if t["status"] == "review"]),
        "done": len([t for t in tasks if t["status"] == "done"]),
        "overdue": len([
            t for t in tasks
            if t["due"] and datetime.fromisoformat(t["due"]) < now and t["status"] != "done"
        ])
    }
