import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# Константы
HISTORY_FILE = "password_history.json"
MIN_LENGTH = 4
MAX_LENGTH = 64

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x400")

        # Переменные
        self.length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Ползунок длины
        ttk.Label(self.root, text="Длина пароля:").pack(pady=5)
        length_scale = ttk.Scale(
            self.root, from_=MIN_LENGTH, to=MAX_LENGTH,
            orient="horizontal", variable=self.length,
            command=self.update_length_label  # Связываем с функцией обновления
        )
        length_scale.pack(fill="x", padx=20)

        # Метка для отображения текущей длины — теперь создаётся до вызова функции
        self.length_label = ttk.Label(self.root, text=f"{self.length.get()} символов")
        self.length_label.pack(pady=5)  # Добавляем отступы для лучшей читаемости

        # Чекбоксы
        ttk.Checkbutton(self.root, text="Цифры (0-9)",
                        variable=self.use_digits).pack(anchor="w", padx=20)
        ttk.Checkbutton(self.root, text="Буквы (a-z, A-Z)",
                        variable=self.use_letters).pack(anchor="w", padx=20)
        ttk.Checkbutton(self.root, text="Спецсимволы (!@#$%)",
                        variable=self.use_special).pack(anchor="w", padx=20)

        # Кнопка генерации
        ttk.Button(self.root, text="Сгенерировать пароль",
                   command=self.generate_password).pack(pady=10)

        # Поле вывода пароля
        self.password_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.password_var,
                  state="readonly", font=("Courier", 12)).pack(fill="x", padx=20, pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").pack(pady=5)
        columns = ("Дата", "Длина", "Пароль")
        self.history_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        self.history_tree.pack(fill="both", expand=True, padx=20, pady=5)

    # Функция для обновления метки при движении ползунка
    def update_length_label(self, value):
        length = int(float(value))  # Преобразуем значение ползунка в целое число
        self.length_label.config(text=f"{length} символов")

    def generate_password(self):
        length = self.length.get()
        if length < MIN_LENGTH or length > MAX_LENGTH:
            messagebox.showerror("Ошибка", f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}")
            return

        chars = ""
        if self.use_digits.get():
            chars += "0123456789"
        if self.use_letters.get():
            chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.use_special.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Добавляем в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_to_history(timestamp, length, password)
        self.save_history()

    def add_to_history(self, timestamp, length, password):
        self.history_tree.insert("", "end", values=(timestamp, length, password))

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    for entry in history:
                        self.add_to_history(entry["timestamp"], entry["length"], entry["password"])
            except Exception as e:
                messagebox.showwarning("Предупреждение", f"Не удалось загрузить историю: {e}")

    def save_history(self):
        history = []
        for item in self.history_tree.get_children():
            values = self.history_tree.item(item)["values"]
            history.append({
                "timestamp": values[0],
                "length": values[1],
                "password": values[2]
            })
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

