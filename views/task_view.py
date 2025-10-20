import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class TaskView:
    def __init__(self, parent, task_controller):
        self.controller = task_controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Форма добавления/редактирования ===
        form_frame = ttk.LabelFrame(self.frame, text="Задача")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.title_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Описание:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.desc_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.desc_var, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Приоритет (1-3):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.priority_var = tk.IntVar(value=2)
        ttk.Spinbox(form_frame, from_=1, to=3, textvariable=self.priority_var, width=5).grid(row=2, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(form_frame, text="Срок (ГГГГ-ММ-ДД):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.due_date_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.due_date_var, width=15).grid(row=3, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(form_frame, text="ID проекта:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.project_id_var = tk.IntVar()
        ttk.Spinbox(form_frame, from_=1, to=999, textvariable=self.project_id_var, width=5).grid(row=4, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(form_frame, text="ID исполнителя:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.assignee_id_var = tk.IntVar()
        ttk.Spinbox(form_frame, from_=1, to=999, textvariable=self.assignee_id_var, width=5).grid(row=5, column=1, sticky="w", padx=5, pady=2)

        ttk.Button(form_frame, text="Добавить задачу", command=self.add_task).grid(row=6, column=0, columnspan=2, pady=10)

        # === Поиск и фильтрация ===
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill="x", pady=5)

        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Поиск", command=self.search_tasks).pack(side="left", padx=5)

        # === Таблица задач ===
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = ("ID", "Название", "Приоритет", "Статус", "Срок", "Проект", "Исполнитель")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Обновить", command=self.load_tasks).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить выбранное", command=self.delete_selected_task).pack(side="left", padx=5)

        self.load_tasks()

    def parse_date(self, date_str):
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return None

    def add_task(self):
        due_date = self.parse_date(self.due_date_var.get())
        if due_date is None:
            return
        try:
            self.controller.add_task(
                title=self.title_var.get(),
                description=self.desc_var.get(),
                priority=self.priority_var.get(),
                due_date=due_date,
                project_id=self.project_id_var.get(),
                assignee_id=self.assignee_id_var.get()
            )
            self.clear_form()
            self.load_tasks()
            messagebox.showinfo("Успех", "Задача добавлена!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_form(self):
        self.title_var.set("")
        self.desc_var.set("")
        self.priority_var.set(2)
        self.due_date_var.set("")
        self.project_id_var.set(1)
        self.assignee_id_var.set(1)

    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = self.controller.get_all_tasks()
        for task in tasks:
            self.tree.insert("", "end", values=(
                task.id,
                task.title,
                task.priority,
                task.status,
                task.due_date.strftime("%Y-%m-%d"),
                task.project_id,
                task.assignee_id
            ))

    def search_tasks(self):
        query = self.search_var.get()
        if not query:
            self.load_tasks()
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = self.controller.search_tasks(query)
        for task in tasks:
            self.tree.insert("", "end", values=(
                task.id,
                task.title,
                task.priority,
                task.status,
                task.due_date.strftime("%Y-%m-%d"),
                task.project_id,
                task.assignee_id
            ))

    def delete_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления")
            return
        task_id = self.tree.item(selected[0])["values"][0]
        self.controller.delete_task(task_id)
        self.load_tasks()
        messagebox.showinfo("Успех", f"Задача {task_id} удалена")