# FlyRank Task API - CRUD API

This is a simple in-memory CRUD API for managing a to-do list, built with Python and FastAPI for the FlyRank Internship Backend Track (W2 - A1).

## How to run

To start the server locally, simply run the following command in your terminal:

uvicorn main:app --reload

The API will be available at `http://localhost:8000`.

## Endpoints

| CRUD Operation | HTTP Method | Endpoint | Meaning |
| --- | --- | --- | --- |
| **Read** | GET | `/` | Get API info |
| **Read** | GET | `/health` | Check if server is alive |
| **Read** | GET | `/tasks` | List all tasks |
| **Read** | GET | `/tasks/{task_id}` | Get a specific task by ID |
| **Create** | POST | `/tasks` | Add a new task |
| **Update** | PUT | `/tasks/{task_id}` | Change an existing task |
| **Delete** | DELETE | `/tasks/{task_id}` | Remove a task |

## Example `curl` Output

Here is the output of testing the `GET /tasks` endpoint:

$ curl -i http://localhost:8000/tasks
HTTP/1.1 200 OK
date: Sun, 19 Jul 2026 19:51:33 GMT
server: uvicorn
content-length: 139
content-type: application/json

[{"id":1,"title":"Buy milk","done":false},{"id":2,"title":"Learn FastAPI","done":true},{"id":3,"title":"Finish FlyRank task","done":false}]

## Swagger UI

Interactive API documentation is generated automatically by FastAPI and is available at `/docs`.

---

## Bonus Stage 7: The AI Rematch

**My Original Prompt:**

> "Act as a senior backend developer. Build a CRUD API using Python and FastAPI. It must manage a to-do list in-memory (no database). Implement endpoints: GET /, GET /health, GET /tasks, GET /tasks/{id}, POST /tasks, PUT /tasks/{id}, and DELETE /tasks/{id}. Return status 201 on creation, 204 on deletion. Unknown IDs should return 404. Invalid/empty bodies should return 400."

**1. What did the AI do better?**
The AI utilized advanced Pydantic validation by using `Field(min_length=1)` directly inside the model. This is much cleaner than writing manual validation logic inside my route functions.

**2. What did it get wrong or quietly ignore?**
I asked for a 400 status on validation errors and 404 on missing items. The AI used FastAPI's built-in `HTTPException`, which returns the error message under the key `{"detail": "..."}` instead of the `{"error": "..."}` JSON format I explicitly used in my hand-built version.

**3. What did my prompt forget to specify?**
I forgot to specify the exact data structure of a "task" (id, title, done) and how the IDs should be generated. Because of this, the AI silently decided to use `UUID` strings for the `id` instead of simple integers (1, 2, 3), and it added extra timestamp fields like `created_at` that I didn't actually ask for.

**The Rematch:**
I improved my prompt by explicitly defining the `Task` model shape (integer IDs starting at 1, title string, done boolean) and requiring custom `JSONResponse` objects with an `"error"` key, which finally resulted in an AI version identical to my hand-built requirements.
