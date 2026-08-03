from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from repository import PostgresTaskRepository
import os

app = FastAPI()

# DATABASE_URL .env-dən oxunur.
DATABASE_URL = os.getenv("DATABASE_URL")
task_repo = PostgresTaskRepository(DATABASE_URL)

class TaskCreate(BaseModel):
    title: str
    done: bool

class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.get("/tasks")
def get_tasks():
    return task_repo.get_all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    return task_repo.create(task)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    updated = task_repo.update(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "title": task.title, "done": task.done}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = task_repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return