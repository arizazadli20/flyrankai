import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
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
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"access_token": response.session.access_token, "refresh_token": response.session.refresh_token}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


# --- STAGE 4: AUTOMATED GUARD (DEPENDENCY) ---

# Bu, Swagger UI-da "Authorize" düyməsini yaradacaq sehrli alətdir
security = HTTPBearer()

# Mərkəzi yoxlanış məntəqəsi (Mühafizəçi)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # HTTPBearer avtomatik olaraq "Bearer " sözünü kəsir, bizə ancaq təmiz tokeni verir
    token = credentials.credentials
    try:
        # Tokeni Supabase-də yoxlayırıq
        user_response = supabase.auth.get_user(token)
        # Hər şey yaxşıdırsa, istifadəçi obyektini qaytarırıq
        return user_response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/public/info", status_code=200)
def get_public_info():
    # Hər kəsə açıq olan ictimai otaq
    return {"message": "Welcome stranger! This info is public."}

# Görürsən, qorunan qapının kodu necə qısaldı?
# Sadəcə "Depends(verify_token)" yazmaqla qapını bağladıq!
@app.get("/protected/profile")
def get_protected_profile(current_user = Depends(verify_token)):
    return {
        "message": "Token is valid!",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "created_at": current_user.created_at
        }
    }