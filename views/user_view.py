import tkinter as tk
from tkinter import ttk, messagebox


class UserView:
    def __init__(self, parent, user_controller):
        self.controller = user_controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Форма пользователя ===
        form_frame = ttk.LabelFrame(self.frame, text="Пользователь")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.username_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.username_var, width=25).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=25).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Роль:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.role_var = tk.StringVar(value="developer")
        roles = ["admin", "manager", "developer"]
        ttk.Combobox(form_frame, textvariable=self.role_var, values=roles, state="readonly", width=22).grid(row=2, column=1, padx=5, pady=2)

        ttk.Button(form_frame, text="Добавить пользователя", command=self.add_user).grid(row=3, column=0, columnspan=2, pady=10)

        # === Таблица пользователей ===
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = ("ID", "Имя", "Email", "Роль", "Регистрация")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_user_select)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Обновить", command=self.load_users).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_selected_user).pack(side="left", padx=5)

        self.load_users()

    def add_user(self):
        try:
            self.controller.add_user(
                username=self.username_var.get(),
                email=self.email_var.get(),
                role=self.role_var.get()
            )
            self.clear_form()
            self.load_users()
            messagebox.showinfo("Успех", "Пользователь добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_form(self):
        self.username_var.set("")
        self.email_var.set("")
        self.role_var.set("developer")

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        users = self.controller.get_all_users()
        for user in users:
            self.tree.insert("", "end", values=(
                user.id,
                user.username,
                user.email,
                user.role,
                user.registration_date.strftime("%Y-%m-%d")
            ))

    def on_user_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        user_id = self.tree.item(selected[0])["values"][0]
        tasks = self.controller.get_user_tasks(user_id)
        messagebox.showinfo("Задачи пользователя", f"Пользователь {user_id} имеет {len(tasks)} задач(и)")

    def delete_selected_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        user_id = self.tree.item(selected[0])["values"][0]
        self.controller.delete_user(user_id)
        self.load_users()
        messagebox.showinfo("Успех", f"Пользователь {user_id} удалён")