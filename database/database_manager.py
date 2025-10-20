import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from models.task import Task
from models.project import Project
from models.user import User


class DatabaseManager:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Создаёт все таблицы при инициализации."""
        self.create_user_table()
        self.create_project_table()
        self.create_task_table()

    # === USERS ===

    def create_user_table(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'developer')),
                    registration_date TEXT NOT NULL
                )
            """)

    def add_user(self, user: User) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, email, role, registration_date)
                VALUES (?, ?, ?, ?)
            """, (user.username, user.email, user.role, user.registration_date.isoformat()))
            user.id = cursor.lastrowid
            return user.id

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row:
                return User(
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    user_id=row[0]
                )
            return None

    def get_all_users(self) -> List[User]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM users").fetchall()
            return [
                User(username=r[1], email=r[2], role=r[3], user_id=r[0])
                for r in rows
            ]

    def update_user(self, user_id: int, **kwargs):
        allowed_fields = {'username', 'email', 'role'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [user_id]

        with self.get_connection() as conn:
            conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)

    def delete_user(self, user_id: int):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))

    # === PROJECTS ===

    def create_project_table(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('active', 'completed', 'on_hold'))
                )
            """)

    def add_project(self, project: Project) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (name, description, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                project.name,
                project.description,
                project.start_date.isoformat(),
                project.end_date.isoformat(),
                project.status
            ))
            project.id = cursor.lastrowid
            return project.id

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
            if row:
                return Project(
                    name=row[1],
                    description=row[2],
                    start_date=datetime.fromisoformat(row[3]),
                    end_date=datetime.fromisoformat(row[4]),
                    project_id=row[0]
                )
            return None

    def get_all_projects(self) -> List[Project]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM projects").fetchall()
            return [
                Project(
                    name=r[1],
                    description=r[2],
                    start_date=datetime.fromisoformat(r[3]),
                    end_date=datetime.fromisoformat(r[4]),
                    project_id=r[0]
                )
                for r in rows
            ]

    def update_project(self, project_id: int, **kwargs):
        allowed_fields = {'name', 'description', 'start_date', 'end_date', 'status'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return

       
        for key in ['start_date', 'end_date']:
            if key in updates and isinstance(updates[key], datetime):
                updates[key] = updates[key].isoformat()

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [project_id]

        with self.get_connection() as conn:
            conn.execute(f"UPDATE projects SET {set_clause} WHERE id = ?", values)

    def delete_project(self, project_id: int):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))

    # === TASKS ===

    def create_task_table(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority INTEGER NOT NULL CHECK(priority IN (1, 2, 3)),
                    status TEXT NOT NULL CHECK(status IN ('pending', 'in_progress', 'completed')),
                    due_date TEXT NOT NULL,
                    project_id INTEGER NOT NULL,
                    assignee_id INTEGER NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
                    FOREIGN KEY(assignee_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

    def add_task(self, task: Task) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                task.title,
                task.description,
                task.priority,
                task.status,
                task.due_date.isoformat(),
                task.project_id,
                task.assignee_id
            ))
            task.id = cursor.lastrowid
            return task.id

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row:
                return Task(
                    title=row[1],
                    description=row[2],
                    priority=row[3],
                    due_date=datetime.fromisoformat(row[5]),
                    project_id=row[6],
                    assignee_id=row[7],
                    task_id=row[0]
                )
            return None

    def get_all_tasks(self) -> List[Task]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM tasks").fetchall()
            return [
                Task(
                    title=r[1],
                    description=r[2],
                    priority=r[3],
                    due_date=datetime.fromisoformat(r[5]),
                    project_id=r[6],
                    assignee_id=r[7],
                    task_id=r[0]
                )
                for r in rows
            ]

    def update_task(self, task_id: int, **kwargs):
        allowed_fields = {'title', 'description', 'priority', 'status', 'due_date', 'project_id', 'assignee_id'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return

       
        if 'due_date' in updates and isinstance(updates['due_date'], datetime):
            updates['due_date'] = updates['due_date'].isoformat()

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [task_id]

        with self.get_connection() as conn:
            conn.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)

    def delete_task(self, task_id: int):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def search_tasks(self, query: str) -> List[Task]:
        query = f"%{query}%"
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM tasks
                WHERE title LIKE ? OR description LIKE ?
            """, (query, query)).fetchall()
            return [
                Task(
                    title=r[1],
                    description=r[2],
                    priority=r[3],
                    due_date=datetime.fromisoformat(r[5]),
                    project_id=r[6],
                    assignee_id=r[7],
                    task_id=r[0]
                )
                for r in rows
            ]

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,)).fetchall()
            return [
                Task(
                    title=r[1],
                    description=r[2],
                    priority=r[3],
                    due_date=datetime.fromisoformat(r[5]),
                    project_id=r[6],
                    assignee_id=r[7],
                    task_id=r[0]
                )
                for r in rows
            ]

    def get_tasks_by_user(self, user_id: int) -> List[Task]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM tasks WHERE assignee_id = ?", (user_id,)).fetchall()
            return [
                Task(
                    title=r[1],
                    description=r[2],
                    priority=r[3],
                    due_date=datetime.fromisoformat(r[5]),
                    project_id=r[6],
                    assignee_id=r[7],
                    task_id=r[0]
                )
                for r in rows
            ]