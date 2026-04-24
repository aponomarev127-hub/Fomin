import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FILE_NAME = "trainings.json"


class TrainingPlanner:
    def __init__(self, window):
        self.window = window
        self.window.title("Training Planner")
        self.window.geometry("900x600")

        self.trainings = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Верхняя форма
        form = tk.Frame(self.window)
        form.pack(pady=10)

        tk.Label(form, text="Дата (YYYY-MM-DD)").grid(row=0, column=0, padx=5)
        self.date_entry = tk.Entry(form)
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Тип тренировки").grid(row=0, column=2, padx=5)
        self.type_box = ttk.Combobox(
            form,
            values=["Силовая", "Кардио", "Бег", "Плавание", "Растяжка"],
            state="readonly"
        )
        self.type_box.grid(row=0, column=3, padx=5)
        self.type_box.current(0)

        tk.Label(form, text="Длительность (мин)").grid(row=0, column=4, padx=5)
        self.duration_entry = tk.Entry(form)
        self.duration_entry.grid(row=0, column=5, padx=5)

        tk.Button(
            form,
            text="Добавить тренировку",
            command=self.add_training
        ).grid(row=0, column=6, padx=10)

        # Фильтры
        filter_frame = tk.Frame(self.window)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр тип").grid(row=0, column=0, padx=5)

        self.filter_box = ttk.Combobox(
            filter_frame,
            values=["Все", "Силовая", "Кардио", "Бег", "Плавание", "Растяжка"],
            state="readonly"
        )
        self.filter_box.grid(row=0, column=1, padx=5)
        self.filter_box.current(0)

        tk.Label(filter_frame, text="От").grid(row=0, column=2, padx=5)
        self.from_entry = tk.Entry(filter_frame)
        self.from_entry.grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="До").grid(row=0, column=4, padx=5)
        self.to_entry = tk.Entry(filter_frame)
        self.to_entry.grid(row=0, column=5, padx=5)

        tk.Button(
            filter_frame,
            text="Применить фильтр",
            command=self.show_data
        ).grid(row=0, column=6, padx=10)

        # Таблица
        self.tree = ttk.Treeview(
            self.window,
            columns=("date", "type", "duration"),
            show="headings",
            height=18
        )

        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Кнопка сохранить
        tk.Button(
            self.window,
            text="Сохранить JSON",
            command=self.save_data
        ).pack(pady=5)

    def valid_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except:
            return False

    def add_training(self):
        date = self.date_entry.get().strip()
        workout = self.type_box.get().strip()
        duration = self.duration_entry.get().strip()

        if not self.valid_date(date):
            messagebox.showerror(
                "Ошибка",
                "Дата должна быть в формате YYYY-MM-DD"
            )
            return

        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError
        except:
            messagebox.showerror(
                "Ошибка",
                "Длительность должна быть положительным числом"
            )
            return

        self.trainings.append({
            "date": date,
            "type": workout,
            "duration": duration
        })

        self.show_data()
        self.save_data()

        self.date_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def show_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_type = self.filter_box.get()
        date_from = self.from_entry.get().strip()
        date_to = self.to_entry.get().strip()

        for row in self.trainings:
            if selected_type != "Все":
                if row["type"] != selected_type:
                    continue

            if date_from:
                if row["date"] < date_from:
                    continue

            if date_to:
                if row["date"] > date_to:
                    continue

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row["date"],
                    row["type"],
                    row["duration"]
                )
            )

    def save_data(self):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(
                self.trainings,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load_data(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                self.trainings = json.load(file)

        self.show_data()


window = tk.Tk()
app = TrainingPlanner(window)
window.mainloop()
