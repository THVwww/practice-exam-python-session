from datetime import datetime
from models.task import Task
from database.database_manager import DatabaseManager


class TaskController:
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()

    def add_task(self, title: str, description: str, priority: int,
                 due_date: datetime, project_id: int, assignee_id: int) -> Task:
        task = Task(title, description, priority, due_date, project_id, assignee_id)
        self.db.add_task(task)
        return task

    def get_task(self, task_id: int) -> Task:
        return self.db.get_task_by_id(task_id)

    def get_all_tasks(self) -> list:
        return self.db.get_all_tasks()

    def update_task(self, task_id: int, **kwargs):
        self.db.update_task(task_id, **kwargs)

    def delete_task(self, task_id: int):
        self.db.delete_task(task_id)

    def search_tasks(self, query: str) -> list:
        return self.db.search_tasks(query)

    def update_task_status(self, task_id: int, new_status: str):
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        task.update_status(new_status)
        self.db.update_task(task_id, status=task.status)

    def get_overdue_tasks(self) -> list:
        tasks = self.get_all_tasks()
        return [task for task in tasks if task.is_overdue()]

    def get_tasks_by_project(self, project_id: int) -> list:
        return self.db.get_tasks_by_project(project_id)

    def get_tasks_by_user(self, user_id: int) -> list:
        return self.db.get_tasks_by_user(user_id)