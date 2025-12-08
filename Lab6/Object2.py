import sys
import random
import tkinter as tk
from tkinter import ttk
import os

class PointGenerator:
    """Генератор, відображення та збереження точок."""
    
    CLIPBOARD_FILENAME = "clipboard.txt"
    
    def __init__(self, n_point, x_min, x_max, y_min, y_max):
        self.n_point = n_point
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.points = []
        
        self.generate_points()
        self.save_points_to_clipboard()
        self.show_window()
    
    def generate_points(self):
        """Генерація випадкових цілочисельних точок у заданих діапазонах."""
        self.points = [
            (
                random.randint(self.x_min, self.x_max),
                random.randint(self.y_min, self.y_max)
            )
            for _ in range(self.n_point)
        ]
        self.points.sort(key=lambda p: p[0])
    
    def save_points_to_clipboard(self):
        """
        Збереження точок у файл (імітація Clipboard Windows) у текстовому форматі.
        Кожна точка записується як "X Y\n".
        """
        try:
            with open(self.CLIPBOARD_FILENAME, "w") as file:
                for x, y in self.points:
                    file.write(f"{x} {y}\n")
            print(f"Object2: Дані успішно записано у {self.CLIPBOARD_FILENAME}")
        except IOError:
            print(f"Помилка: Неможливо записати дані у файл {self.CLIPBOARD_FILENAME}")
    
    def show_window(self):
        """Створення та відображення вікна з таблицею згенерованих точок."""
        window = tk.Tk()
        window.title(f"Object2 - Генератор точок ({self.n_point} шт.)")
        window.geometry("400x500")
        
        self.center_window(window)
        
        # Заголовок
        title = tk.Label(
            window, text="OBJECT2 - ТАБЛИЦЯ ЗГЕНЕРОВАНИХ ТОЧОК",
            font=("Arial", 12, "bold"), fg="darkgreen"
        )
        title.pack(pady=10)
        
        # Параметри
        params_text = (
            f"Точок: {self.n_point} | "
            f"X: [{self.x_min}..{self.x_max}] | "
            f"Y: [{self.y_min}..{self.y_max}]"
        )
        tk.Label(window, text=params_text, font=("Arial", 9)).pack()
        
        # Таблиця
        self._create_table(window)
        
        # Інформація про Clipboard
        tk.Label(
            window, text=f"✓ Дані для Object3 збережено у {self.CLIPBOARD_FILENAME}",
            font=("Arial", 9, "italic"), fg="gray"
        ).pack(pady=5)
        
        window.mainloop()
    
    def _create_table(self, parent):
        """Створення таблиці з точками за допомогою Treeview."""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(
            frame, columns=("x", "y"), 
            show="headings", height=15
        )
        tree.heading("x", text="X Координата")
        tree.heading("y", text="Y Координата")
        tree.column("x", width=150, anchor=tk.CENTER)
        tree.column("y", width=150, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Додавання точок у таблицю
        for x, y in self.points:
            tree.insert("", "end", values=(x, y))
    
    def center_window(self, window):
        """Центрування вікна на екрані (щоб не накладалося на Lab6)."""
        window.update_idletasks()
        w = window.winfo_width()
        h = window.winfo_height()
        # Розміщуємо Object2 ліворуч
        x = (window.winfo_screenwidth() - w) // 2 - 250
        y = (window.winfo_screenheight() - h) // 2
        window.geometry(f"{w}x{h}+{x}+{y}")


def main():
    """Точка входу для Object2."""
    if len(sys.argv) != 6:
        print("Object2: Запустіть програму через Lab6.py, оскільки потрібні вхідні параметри.")
        input("Натисніть Enter для виходу...")
        return
    
    try:
        params = [int(arg) for arg in sys.argv[1:]]
        
        PointGenerator(*params)
        
    except ValueError:
        print("Object2: Помилка конвертації параметрів. Очікувалися цілі числа.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Object2: Критична помилка під час виконання: {e}")