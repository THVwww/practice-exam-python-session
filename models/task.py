from datetime import datetime


class Task:
    def __init__(self, title: str, description: str, priority: int,
                 due_date: datetime, project_id: int, assignee_id: int, task_id: int = None):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority  # 1 - high, 2 - medium, 3 - low
        self.status = 'pending'  # default status
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status: str):
        valid_statuses = {'pending', 'in_progress', 'completed'}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        self.status = new_status

    def is_overdue(self) -> bool:
        return self.status != 'completed' and datetime.now() > self.due_date

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'project_id': self.project_id,
            'assignee_id': self.assignee_id
        }