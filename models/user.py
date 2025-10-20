from datetime import datetime


class User:
    def __init__(self, username: str, email: str, role: str, user_id: int = None):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role  # 'admin', 'manager', 'developer'
        self.registration_date = datetime.now()

    def update_info(self, username: str = None, email: str = None, role: str = None):
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if role is not None:
            valid_roles = {'admin', 'manager', 'developer'}
            if role not in valid_roles:
                raise ValueError(f"Invalid role: {role}. Must be one of {valid_roles}")
            self.role = role

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'registration_date': self.registration_date.isoformat()
        }