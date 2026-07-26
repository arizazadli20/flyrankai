Markdown
# FlyRank Task API (SQLite Version)

This is a complete CRUD API for managing tasks, built with FastAPI and Python. In this assignment, the storage layer was migrated from an in-memory list to a real SQLite database.

## Why SQLite?
SQLite was chosen because it requires zero setup, runs seamlessly without a dedicated server, and stores the entire database in a single `tasks.db` file. Most importantly, it provides data persistence, meaning our tasks now survive server restarts!

## How to Run
To run this project locally, simply execute the following command in your terminal:
```bash
uvicorn main:app --reload
Note: The tasks.db database, the tasks table, and 3 seeded example tasks are created automatically on the very first run.

Example SQL Query
Here is one of the queries I ran directly in DB Browser to verify the data:

SQL
SELECT * FROM tasks;
Result: This returned all 3 seeded tasks from the database, proving that the Python API and the DB Browser are reading from the exact same source of truth.

Database Screenshot
Below is a screenshot of the database open in DB Browser for SQLite, showing the executed query and the persistent data:

