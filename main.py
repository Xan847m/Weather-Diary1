import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

DATA_FILE = 'weather_data.json'

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля ввода
        ttk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.temp_entry = ttk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.desc_entry = ttk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Осадки (да/нет):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.precip_var = tk.StringVar()
        self.precip_combo = ttk.Combobox(self.root, textvariable=self.precip_var, values=["да", "нет"], state="readonly")
        self.precip_combo.current(1)
        self.precip_combo.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        add_btn = ttk.Button(self.root, text="Добавить запись", command=self.add_record)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Температура", "Описание", "Осадки"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Температура", text="Температура")
        self.tree.heading("Описание", text="Описание")
        self.tree.heading("Осадки", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        ttk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.filter_date_entry = ttk.Entry(self.root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')
        filter_date_btn = ttk.Button(self.root, text="Фильтр по дате", command=self.filter_by_date)
        filter_date_btn.grid(row=6, column=2, padx=5, pady=5)

        ttk.Label(self.root, text="Минимальная температура (°C):").grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.filter_temp_entry = ttk.Entry(self.root)
        self.filter_temp_entry.grid(row=7, column=1, padx=5, pady=5)
        filter_temp_btn = ttk.Button(self.root, text="Фильтр по температуре", command=self.filter_by_temp)
        filter_temp_btn.grid(row=7, column=2, padx=5, pady=5)

        # Кнопка очистки фильтров
        clear_filters_btn = ttk.Button(self.root, text="Очистить фильтры", command=self.load_data)
        clear_filters_btn.grid(row=8, column=0, columnspan=3, pady=10)

        # Кнопки сохранения и загрузки
        save_btn = ttk.Button(self.root, text="Сохранить в файл", command=self.save_data)
        save_btn.grid(row=9, column=0, padx=5, pady=5)
        load_btn = ttk.Button(self.root, text="Загрузить из файла", command=self.load_data)
        load_btn.grid(row=9, column=1, padx=5, pady=5)

    def add_record(self):
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        precip = self.precip_var.get()

        # Проверка корректности
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return
        if not desc:
            messagebox.showerror("Ошибка", "Описание погоды не должно быть пустым.")
            return

        record = {
            "date": date_str,
            "temperature": temp,
            "description": desc,
            "precipitation": precip
        }
        self.records.append(record)
        self.refresh_tree()
        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_combo.current(1)

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def refresh_tree(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data_to_show = data if data is not None else self.records
        for rec in data_to_show:
            self.tree.insert('', tk.END, values=(
                rec["date"],
                rec["temperature"],
                rec["description"],
                rec["precipitation"]
            ))

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def load_data(self):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = []
        self.refresh_tree()

    def filter_by_date(self):
        date_filter = self.filter_date_entry.get().strip()
        if not self.validate_date(date_filter):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        filtered = [rec for rec in self.records if rec["date"] == date_filter]
        self.refresh_tree(filtered)

    def filter_by_temp(self):
        temp_str = self.filter_temp_entry.get().strip()
        try:
            temp_min = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число для фильтрации по температуре.")
            return
        filtered = [rec for rec in self.records if rec["temperature"] >= temp_min]
        self.refresh_tree(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()