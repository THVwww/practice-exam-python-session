from datetime import datetime
from models.project import Project
from database.database_manager import DatabaseManager


class ProjectController:
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()

    def add_project(self, name: str, description: str, start_date: datetime, end_date: datetime) -> Project:
        project = Project(name, description, start_date, end_date)
        self.db.add_project(project)
        return project

    def get_project(self, project_id: int) -> Project:
        return self.db.get_project_by_id(project_id)

    def get_all_projects(self) -> list:
        return self.db.get_all_projects()

    def update_project(self, project_id: int, **kwargs):
        self.db.update_project(project_id, **kwargs)

    def delete_project(self, project_id: int):
        self.db.delete_project(project_id)

    def update_project_status(self, project_id: int, new_status: str):
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        project.update_status(new_status)
        self.db.update_project(project_id, status=project.status)

    def get_project_progress(self, project_id: int) -> float:
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return project.get_progress()