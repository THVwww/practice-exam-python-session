import tkinter as tk
from tkinter import ttk
from views.task_view import TaskView
from views.project_view import ProjectView
from views.user_view import UserView


class MainWindow:
    def __init__(self, task_controller, project_controller, user_controller):
        self.root = tk.Tk()
        self.root.title("Система управления задачами")
        self.root.geometry("900x600")

        # Создаём вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Вкладка задач
        task_frame = ttk.Frame(notebook)
        notebook.add(task_frame, text="Задачи")
        self.task_view = TaskView(task_frame, task_controller)

        # Вкладка проектов
        project_frame = ttk.Frame(notebook)
        notebook.add(project_frame, text="Проекты")
        self.project_view = ProjectView(project_frame, project_controller)

        # Вкладка пользователей
        user_frame = ttk.Frame(notebook)
        notebook.add(user_frame, text="Пользователи")
        self.user_view = UserView(user_frame, user_controller)

    def run(self):
        self.root.mainloop()