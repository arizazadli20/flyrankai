import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

# Öz yazdığın repository faylından import edirik
from repository import PostgresTaskRepository

# just reading the .env file and loading the things to main project. We are doing it for Security.
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# these codes making a bridge for our server and supabase server.
supabase: Client = create_client(supabase_url=url, supabase_key=key)

#these codes for starting server and show what we ll see on main page.
app = FastAPI(title="FlyRank Auth API")

@app.get("/")
def read_root():
    return {"message": "Server running and connected to Supabase"}


# these codes reading .env for our PostreSql base
DATABASE_URL = os.getenv("DATABASE_URL")
task_repo = PostgresTaskRepository(DATABASE_URL)

class TaskCreate(BaseModel):
    title: str
    done: bool

class TaskUpdate(BaseModel):
    title: str
    done: bool

#these codes gives all tasks from task_repo and give it to user as JSON
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

    # İstifadəçidən gələn giriş məlumatlarını yoxlamaq üçün Pydantic modeli
class UserCredentials(BaseModel):
    email: str
    password: str

@app.post("/auth/signup", status_code=201)
def signup(credentials: UserCredentials):
    # Əgər e-poçt və ya parol boşdursa, 400 xətası veririk
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    try:
        # Məlumatları Supabase-ə göndəririk ki, istifadəçini qeydiyyatdan keçirsin
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return response.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", status_code=200)
def login(credentials: UserCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    try:
        # Supabase bu e-poçt və parolun doğruluğunu yoxlayır
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        # Parol doğrudursa, bizə Access Token (giriş vəsiqəsi) qaytarır
        return {"access_token": response.session.access_token, "refresh_token": response.session.refresh_token}
    except Exception as e:
        # Supabase parolu səhv tapsa, 401 xətası veririk
        raise HTTPException(status_code=401, detail="Invalid login credentials")

        # --- STAGE 2: THE PUBLIC & PROTECTED GATES ---

@app.get("/public/info", status_code=200)
def get_public_info():
    # Hər kəsə açıq olan ictimai otaq
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def get_protected_profile(request: Request):
    # 1. Vəsiqəni başlıqlardan axtarırıq (Köhnə məntiq)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    
    token = auth_header.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Access token required")
        
    # 2. YENİ: Vəsiqəni (token) Supabase-ə yoxlatdırırıq
    try:
        # Supabase-ə şəbəkə sorğusu gedir, əgər token saxtadırsa xəta (Exception) atacaq
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        
        # Hər şey qaydasındadırsa, istifadəçinin id və email kimi icazə verilən məlumatlarını qaytarırıq
        return {
            "message": "Token is valid!",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at
            }
        }
    except Exception as e:
        # Token saxtadırsa, dəyişdirilibsə və ya vaxtı keçibsə dərhal 401 qovulma xətası veririk
        raise HTTPException(status_code=401, detail="Invalid or expired token")