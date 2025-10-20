# main.py
from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController
from views.main_window import MainWindow

if __name__ == "__main__":
    db = DatabaseManager()
    task_ctrl = TaskController(db)
    project_ctrl = ProjectController(db)
    user_ctrl = UserController(db)

    # Дополнительно: передать task_ctrl в ProjectView, если нужно показывать задачи
    app = MainWindow(task_ctrl, project_ctrl, user_ctrl)
    app.run()