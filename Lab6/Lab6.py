import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import os
import time

class Lab6App:
    """Головний клас менеджера системи"""
    INPUT_PARAMS = [
        ("nPoint", "Кількість точок:", ""),
        ("xMin", "Мінімальне X:", ""),
        ("xMax", "Максимальне X:", ""),
        ("yMin", "Мінімальне Y:", ""),
        ("yMax", "Максимальне Y:", "")
    ]
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Lab6 - Менеджер Взаємодії")
        self.window.geometry("450x400")
        self.child_processes = {}  
        self.setup_ui()
    
    def setup_ui(self):
        """Ініціалізація графічного інтерфейсу."""
        
        # Заголовки
        tk.Label(self.window, text="Лабораторна робота №6", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        # Поля для вводу параметрів
        self.entries = self._create_param_fields()
        
        # Кнопка запуску
        self.btn_start = tk.Button(
            self.window, text="▶ Запустити послідовність",
            command=self.start_sequence_thread,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
            width=25, height=2
        )
        self.btn_start.pack(pady=20)
        
        # Статус виконання
        self.lbl_status = tk.Label(
            self.window, text="Введіть параметри та натисніть старт",
            font=("Arial", 10), fg="blue"
        )
        self.lbl_status.pack()

    def _create_param_fields(self):
        """Створення полів для параметрів у рамці."""
        frame = tk.LabelFrame(self.window, text="Параметри точок", font=("Arial", 11))
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        entries = {}
        for i, (key, label, default_value) in enumerate(self.INPUT_PARAMS):
            tk.Label(frame, text=label, font=("Arial", 10)).grid(
                row=i, column=0, sticky=tk.W, pady=3, padx=5)
            
            entry = tk.Entry(frame, width=15, font=("Arial", 10))
            entry.insert(0, default_value)
            entry.grid(row=i, column=1, pady=3, padx=5)
            entries[key] = entry
            
        return entries
    
    def validate_params(self):
        """Перевірка та конвертація введених параметрів."""
        try:
            params = {}
            for key in self.entries:
                value = self.entries[key].get().strip()
                if not value:
                    messagebox.showerror("Помилка вводу", "Заповніть всі поля!")
                    return None
                
                params[key] = int(value)
            
            # Додаткова логічна перевірка
            if params["xMin"] >= params["xMax"] or params["yMin"] >= params["yMax"]:
                messagebox.showerror("Помилка", "Мінімальне значення має бути менше максимального!")
                return None
            
            if params["nPoint"] <= 0:
                 messagebox.showerror("Помилка", "Кількість точок має бути більше 0!")
                 return None
            
            return params
            
        except ValueError:
            messagebox.showerror("Помилка вводу", "Введіть коректні цілі числа!")
            return None
    
    def _terminate_running_processes(self):
        """Завершує роботу всіх дочірніх процесів перед новим запуском."""
        for name, process in self.child_processes.items():
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=1)
                except:
                    process.kill()
                    time.sleep(0.5)
        
        self.child_processes.clear()
        
    def start_sequence_thread(self):
        """Запускає основну послідовність роботи в окремому потоці"""
        params = self.validate_params()
        if not params:
            return
        
        self.btn_start.config(state=tk.DISABLED, text="Виконується...")
        self.lbl_status.config(text="Запуск програм...", fg="orange")
        
        # Створюємо та запускаємо потік для виконання логіки
        thread = threading.Thread(target=self._run_task_sequence, args=(params,))
        thread.daemon = True
        thread.start()
    
    def _run_task_sequence(self, params):
        """Основна логіка: реалізація алгоритму взаємодії"""
        try:
            # Етап 1: Ініціалізація та очищення
            self._terminate_running_processes()
            self._cleanup_clipboard_file()
            
            self._update_ui_status("Запуск Object2 (Генератор)...", "blue")
            
            # Етап 2: Запуск Object2 та передача параметрів
            object2_args = [
                "python", "Object2.py",
                str(params["nPoint"]),
                str(params["xMin"]),
                str(params["xMax"]),
                str(params["yMin"]),
                str(params["yMax"])
            ]
            
            self.child_processes["object2"] = subprocess.Popen(object2_args)
            time.sleep(2) # Затримка, щоб Object2 встиг згенерувати дані та записати у файл
            
            # Етап 3: Запуск Object3
            self._update_ui_status("Запуск Object3 (Графік)...", "blue")
            
            self.child_processes["object3"] = subprocess.Popen(["python", "Object3.py"])
            
            self._update_ui_success()
            
        except FileNotFoundError:
             self._update_ui_error("Не знайдено Object2.py або Object3.py. Перевірте шляхи.")
        except Exception as e:
            self._update_ui_error(f"Критична помилка виконання: {e}")
        
    def _cleanup_clipboard_file(self):
        """Очищення файлу, що імітує Clipboard."""
        CLIPBOARD_FILENAME = "clipboard.txt"
        try:
            if os.path.exists(CLIPBOARD_FILENAME):
                os.remove(CLIPBOARD_FILENAME)
        except Exception as e:
            print(f"Помилка очищення файлу {CLIPBOARD_FILENAME}: {e}")
    
    def _update_ui_status(self, msg, color="blue"):
         self.window.after(0, lambda: self.lbl_status.config(text=msg, fg=color))
         
    def _update_ui_success(self):
        self._update_ui_status("✅ Роботу послідовності завершено. Результати у дочірніх вікнах.", "green")
        self.window.after(0, lambda: self.btn_start.config(
            state=tk.NORMAL, text="▶ Запустити знову"))
    
    def _update_ui_error(self, error_msg):
        self._update_ui_status(f"❌ Помилка: {error_msg}", "red")
        self.window.after(0, lambda: self.btn_start.config(
            state=tk.NORMAL, text="▶ Запустити послідовність"))

    def run(self):
        """Запуск головного циклу Tkinter."""
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing) 
        self.window.mainloop()
        
    def on_closing(self):
        """Обробник події закриття вікна."""
        self._terminate_running_processes()
        self.window.destroy()


if __name__ == "__main__":
    app = Lab6App()
    app.run()