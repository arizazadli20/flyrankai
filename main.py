from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# "Database" - yaddaşda saxlanılan task siyahısı (id, title, done)
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Finish FlyRank task", "done": False}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Bütün taskları qaytaran endpoint
@app.get("/tasks")
def get_tasks():
    return tasks

# Tək bir taskı ID-sinə görə qaytaran endpoint
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    # Task tapılmadıqda 404 statusu və xüsusi JSON xətası qaytarırıq
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})