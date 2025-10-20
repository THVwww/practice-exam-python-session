from datetime import datetime


class Project:
    def __init__(self, name: str, description: str, start_date: datetime, end_date: datetime, project_id: int = None):
        self.id = project_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = 'active'  # default status

    def update_status(self, new_status: str):
        valid_statuses = {'active', 'completed', 'on_hold'}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        self.status = new_status

    def get_progress(self) -> float:
                total_days = (self.end_date - self.start_date).days
        if total_days <= 0:
            return 100.0 if self.status == 'completed' else 0.0

        elapsed_days = (datetime.now() - self.start_date).days
        progress = min(100.0, max(0.0, (elapsed_days / total_days) * 100))
        if self.status == 'completed':
            progress = 100.0
        return round(progress, 2)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status
        }