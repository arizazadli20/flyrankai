```markdown
# FlyRank Task API (PostgreSQL & Docker Version)

This is a complete CRUD API for managing tasks, built with FastAPI, Python, and backed by a real **PostgreSQL** database running inside a **Docker** container[cite: 8].

## Architecture & Storage
In this assignment, the storage layer was migrated from a local SQLite file to a containerized PostgreSQL server. 
- **Docker & Docker Compose**: Runs the entire stack (API + Database) with a single command, eliminating environment inconsistencies ("it works on my machine")[cite: 8].
- **Environment Secrets**: Database credentials are securely loaded from a `.env` file (git-ignored) using a template from `.env.example`[cite: 8].
- **Data Persistence**: A Docker named volume (`taskdata`) is attached to Postgres, ensuring that tasks survive container restarts and full-stack downs[cite: 8].

## How to Run
To run this project locally, follow these steps:

1. Clone the repository and copy the environment template:
   ```bash
   cp .env.example .env

```

2. Start the entire stack using Docker Compose:
```bash
docker compose up --build

```



(Note: The `tasks` table and 3 seeded example tasks are created automatically on the very first startup).

## API Endpoints

| Method | Endpoint | Description | Status Codes |
| --- | --- | --- | --- |
| **GET** | `/tasks` | Retrieve all tasks | `200 OK` |
| **GET** | `/tasks/{id}` | Retrieve a specific task by ID | `200 OK`, `404 Not Found`<br> |
| **POST** | `/tasks` | Create a new task | `201 Created`, `400 Bad Request`<br> |
| **PUT** | `/tasks/{id}` | Update an existing task | `200 OK`, `404 Not Found`<br> |
| **DELETE** | `/tasks/{id}` | Delete a task | `204 No Content`, `404 Not Found`<br> |

## Example Request (`curl`)

Here is an example test command to fetch all tasks from the running container:

```bash
curl -i http://localhost:3000/tasks

```

## Database Screenshot

Below is a screenshot showing the data inside the running PostgreSQL database container:


```

```
