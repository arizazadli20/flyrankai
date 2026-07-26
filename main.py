from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM tasks')
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
            INSERT INTO tasks (title, done) VALUES 
            ('Buy milk', 0),
            ('Learn FastAPI', 1),
            ('Finish FlyRank task', 0)
        ''')
    
    conn.commit()
    conn.close()

init_db()

class TaskCreate(BaseModel):
    title: str = ""

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
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    return [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        
    return {"id": row[0], "title": row[1], "done": bool(row[2])}

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is missing or empty"})
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, 0))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return {
        "id": new_id,
        "title": task.title,
        "done": False
    }

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    if task_update.title is None and task_update.done is None:
         return JSONResponse(status_code=400, content={"error": "Empty or invalid body"})
         
    if task_update.title is not None and not task_update.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        
    new_title = task_update.title if task_update.title is not None else row[1]
    new_done = task_update.done if task_update.done is not None else bool(row[2])
    
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (new_title, int(new_done), task_id))
    conn.commit()
    conn.close()
    
    return {"id": task_id, "title": new_title, "done": bool(new_done)}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return Response(status_code=204)