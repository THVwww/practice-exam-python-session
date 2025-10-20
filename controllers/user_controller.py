from models.user import User
from database.database_manager import DatabaseManager


class UserController:
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()

    def add_user(self, username: str, email: str, role: str) -> User:
        user = User(username, email, role)
        self.db.add_user(user)
        return user

    def get_user(self, user_id: int) -> User:
        return self.db.get_user_by_id(user_id)

    def get_all_users(self) -> list:
        return self.db.get_all_users()

    def update_user(self, user_id: int, **kwargs):
        self.db.update_user(user_id, **kwargs)

    def delete_user(self, user_id: int):
        self.db.delete_user(user_id)

    def get_user_tasks(self, user_id: int) -> list:
       
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return self.db.get_tasks_by_user(user_id)