import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client

from repository import TaskRepository

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url=url, supabase_key=key)

DATABASE_URL = os.getenv("DATABASE_URL")
repo = TaskRepository(DATABASE_URL)

app = FastAPI(title="FlyRank Auth API")
security = HTTPBearer()


class TaskCreate(BaseModel):
    title: str
    done: bool


class TaskUpdate(BaseModel):
    title: str
    done: bool


class UserCredentials(BaseModel):
    email: str
    password: str


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/")
def health_check():
    return {"message": "Server running and connected to Supabase"}


@app.get("/tasks")
def read_tasks():
    return repo.get_tasks()


@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = repo.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    return repo.add_task(task)


@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: TaskUpdate):
    updated = repo.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "title": task.title, "done": task.done}


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    deleted = repo.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return


@app.post("/auth/signup", status_code=201)
def signup(credentials: UserCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.
