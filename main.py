from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# "Database" - yaddaşda saxlanılan task siyahısı
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Finish FlyRank task", "done": False}
]

class TaskCreate(BaseModel):
    title: str = ""

# Update (Yeniləmə) üçün yeni model (parametrlər məcburi deyil)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is missing or empty"})
    
    new_id = max(t["id"] for t in tasks) + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

# Stage 4: Taskı yeniləmək (PUT)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    # Əgər body tamamilə boşdursa 400 xətası qaytarırıq
    if task_update.title is None and task_update.done is None:
         return JSONResponse(status_code=400, content={"error": "Empty or invalid body"})
         
    for task in tasks:
        if task["id"] == task_id:
            if task_update.title is not None:
                if not task_update.title.strip():
                    return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
                task["title"] = task_update.title
            if task_update.done is not None:
                task["done"] = task_update.done
            return task
            
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

# Stage 4: Taskı silmək (DELETE)
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            # Uğurla silindikdə 204 statusu və boş gövdə (empty body) qaytarılır
            return Response(status_code=204)
            
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})