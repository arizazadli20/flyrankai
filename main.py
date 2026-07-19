from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# "Database" - yaddaşda saxlanılan task siyahısı
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Finish FlyRank task", "done": False}
]

# Müştəridən gələn datanın strukturunu müəyyən edən model
class TaskCreate(BaseModel):
    title: str = ""

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

# Stage 3: Yeni task yaratmaq (POST)
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    # Validation: title boşdursa 400 qaytarırıq
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is missing or empty"})
    
    # Növbəti boş ID-ni tapırıq
    new_id = max(t["id"] for t in tasks) + 1 if tasks else 1
    
    # Yeni taskı formalaşdırıb siyahıya əlavə edirik
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    
    return new_task