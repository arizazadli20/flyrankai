import psycopg
import time

class PostgresTaskRepository:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self._init_db()

    def _init_db(self):
        # Bazanın tam oyanmasını gözləmək üçün yoxlama (retry) məntiqi
        retries = 5
        while retries > 0:
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
                            seed_tasks = [("Learn Docker", True), ("Setup Postgres", False), ("Write YAML", False)]
                            cur.executemany("INSERT INTO tasks (title, done) VALUES (%s, %s)", seed_tasks)
                        conn.commit()
                # Hər şey uğurludursa dövrdən çıxır
                break 
            except psycopg.OperationalError:
                print(f"Database hələ hazır deyil, 2 saniyə gözlənilir... ({retries} cəhd qaldı)")
                time.sleep(2)
                retries -= 1
        else:
            print("XƏTA: Verilənlər bazasına qoşulmaq mümkün olmadı.")

    def get_all(self):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks")
                return [{"id": row[0], "title": row[1], "done": row[2]} for row in cur.fetchall()]

    def get_by_id(self, task_id):
        # Təhlükəsizlik üçün %s parametri istifadə olunur.
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
                row = cur.fetchone()
                if row:
                    return {"id": row[0], "title": row[1], "done": row[2]}
                return None

    def create(self, task):
        # RETURNING bölməsi vasitəsilə yeni yaradılan id-ni geri alırıq.
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id", 
                    (task.title, task.done)
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"id": new_id, "title": task.title, "done": task.done}

    def update(self, task_id, task):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id", 
                    (task.title, task.done, task_id)
                )
                updated_row = cur.fetchone()
                conn.commit()
                return updated_row

    def delete(self, task_id):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
                deleted_row = cur.fetchone()
                conn.commit()
                return deleted_row