import time
import psycopg


class TaskRepository:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.setup_db()

    def setup_db(self):
        attempts = 5
        while attempts > 0:
            try:
                with psycopg.connect(self.db_url) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS tasks (
                                id SERIAL PRIMARY KEY,
                                title TEXT NOT NULL,
                                done BOOLEAN NOT NULL
                            )
                        """)
                        cur.execute("SELECT COUNT(*) FROM tasks")
                        if cur.fetchone()[0] == 0:
                            initial_tasks = [
                                ("Learn Docker", True),
                                ("Setup Postgres", False),
                                ("Write YAML", False),
                            ]
                            cur.executemany(
                                "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                                initial_tasks,
                            )
                        conn.commit()
                break
            except psycopg.OperationalError:
                print(f"Database not ready yet, retrying in 2s... ({attempts} attempts left)")
                time.sleep(2)
                attempts -= 1
        else:
            print("Error: Could not connect to the database.")

    def get_tasks(self):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks")
                rows = cur.fetchall()
                return [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]

    def get_task(self, task_id: int):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
                row = cur.fetchone()
                if not row:
                    return None
                return {"id": row[0], "title": row[1], "done": row[2]}

    def add_task(self, task):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
                    (task.title, task.done),
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"id": new_id, "title": task.title, "done": task.done}

    def update_task(self, task_id: int, task):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id",
                    (task.title, task.done, task_id),
                )
                updated = cur.fetchone()
                conn.commit()
                return updated

    def delete_task(self, task_id: int):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
                deleted = cur.fetchone()
                conn.commit()
                return deleted
