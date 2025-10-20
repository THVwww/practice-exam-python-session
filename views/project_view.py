import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ProjectView:
    def __init__(self, parent, project_controller):
        self.controller = project_controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Форма проекта ===
        form_frame = ttk.LabelFrame(self.frame, text="Проект")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Описание:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.desc_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.desc_var, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Начало (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.start_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.start_var, width=15).grid(row=2, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(form_frame, text="Окончание (ГГГГ-ММ-ДД):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.end_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.end_var, width=15).grid(row=3, column=1, sticky="w", padx=5, pady=2)

        ttk.Button(form_frame, text="Добавить проект", command=self.add_project).grid(row=4, column=0, columnspan=2, pady=10)

        # === Таблица проектов ===
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = ("ID", "Название", "Статус", "Прогресс (%)", "Начало", "Окончание")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_project_select)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Обновить", command=self.load_projects).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_selected_project).pack(side="left", padx=5)

        self.load_projects()

    def parse_date(self, date_str):
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты")
            return None

    def add_project(self):
        start = self.parse_date(self.start_var.get())
        end = self.parse_date(self.end_var.get())
        if start is None or end is None:
            return
        try:
            self.controller.add_project(
                name=self.name_var.get(),
                description=self.desc_var.get(),
                start_date=start,
                end_date=end
            )
            self.clear_form()
            self.load_projects()
            messagebox.showinfo("Успех", "Проект добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_form(self):
        self.name_var.set("")
        self.desc_var.set("")
        self.start_var.set("")
        self.end_var.set("")

    def load_projects(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        projects = self.controller.get_all_projects()
        for proj in projects:
            progress = self.controller.get_project_progress(proj.id)
            self.tree.insert("", "end", values=(
                proj.id,
                proj.name,
                proj.status,
                f"{progress:.1f}",
                proj.start_date.strftime("%Y-%m-%d"),
                proj.end_date.strftime("%Y-%m-%d")
            ))

    def on_project_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        project_id = self.tree.item(selected[0])["values"][0]
        # Здесь можно открыть окно с задачами проекта (упрощённо — просто сообщение)
        tasks = self.controller.task_controller.get_tasks_by_project(project_id) \
            if hasattr(self.controller, 'task_controller') else []
        messagebox.showinfo("Задачи проекта", f"Проект {project_id} имеет {len(tasks)} задач(и)")

    def delete_selected_project(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите проект")
            return
        proj_id = self.tree.item(selected[0])["values"][0]
        self.controller.delete_project(proj_id)
        self.load_projects()
        messagebox.showinfo("Успех", f"Проект {proj_id} удалён")