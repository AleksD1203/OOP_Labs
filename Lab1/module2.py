import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class IScrollModule(ABC):
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def get_current_value(self): pass

class ScrollBarDialog:
    def __init__(self, parent, title="Вибір значення", min_val=1, max_val=100):
        self.parent = parent
        self.title = title
        self.min_value = min_val
        self.max_value = max_val
        self.current_value = (min_val + max_val) // 2
        self.result = 0
        
    def create_dialog(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("500x280")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.center_window()
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Виберіть значення від {self.min_value} до {self.max_value}:",
                 font=("Arial", 11)).pack(pady=(0, 10))
        
        value_frame = ttk.Frame(main_frame)
        value_frame.pack(pady=(0, 10), fill=tk.X)
        ttk.Label(value_frame, text="Поточне значення:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.value_label = ttk.Label(value_frame, text=str(self.current_value),
                                    font=("Arial", 14, "bold"), foreground="blue")
        self.value_label.pack(side=tk.RIGHT)
        
        self.scale_widget = tk.Scale(main_frame, from_=self.min_value, to=self.max_value,
                                   orient=tk.HORIZONTAL, length=400, command=self.on_scale_change,
                                   font=("Arial", 10))
        self.scale_widget.set(self.current_value)
        self.scale_widget.pack(pady=(10, 15), fill=tk.X)
        
        range_frame = ttk.Frame(main_frame)
        range_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(range_frame, text=str(self.min_value), font=("Arial", 9)).pack(side=tk.LEFT)
        ttk.Label(range_frame, text=str(self.max_value), font=("Arial", 9)).pack(side=tk.RIGHT)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(5, 0))
        
        ok_button = ttk.Button(button_frame, text="Так", command=self.ok_clicked, width=12)
        ok_button.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Відміна", command=self.cancel_clicked, width=12).pack(side=tk.LEFT)
        ok_button.focus_set()
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())
        
    def center_window(self):
        self.parent.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - 250
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - 140
        screen_w, screen_h = self.dialog.winfo_screenwidth(), self.dialog.winfo_screenheight()
        x = max(0, min(x, screen_w - 500))
        y = max(0, min(y, screen_h - 280))
        self.dialog.geometry(f"500x280+{x}+{y}")
        
    def on_scale_change(self, value):
        self.current_value = int(float(value))
        self.value_label.config(text=str(self.current_value))
        
    def ok_clicked(self):
        self.result = 1
        if self.dialog: self.dialog.destroy()
        
    def cancel_clicked(self):
        self.result = 0
        if self.dialog: self.dialog.destroy()
        
    def show(self):
        self.create_dialog()
        self.dialog.wait_window()
        return self.result

class ValueProcessor:
    @staticmethod
    def get_percentage(value, min_val, max_val):
        return ((value - min_val) / (max_val - min_val)) * 100
    
    @staticmethod
    def get_description(value):
        if value <= 20: return "Дуже низьке"
        elif value <= 40: return "Низьке"
        elif value <= 60: return "Середнє"
        elif value <= 80: return "Високе"
        else: return "Дуже високе"
    
    @staticmethod
    def format_info(value, min_val=1, max_val=100):
        return {
            'value': value,
            'percentage': round(ValueProcessor.get_percentage(value, min_val, max_val), 1),
            'description': ValueProcessor.get_description(value)
        }

class Module2(IScrollModule):
    def __init__(self, parent):
        self.parent = parent
        self.selected_value = 50
        self.value_info = {}
        
    def execute(self):
        dialog = ScrollBarDialog(self.parent, "Модуль 2 - Вибір числа")
        result = dialog.show()
        if result:
            self.selected_value = dialog.current_value
            self.value_info = ValueProcessor.format_info(self.selected_value)
        return result
    
    def get_current_value(self):
        return self.selected_value
    
    def get_result_value(self):
        if not self.value_info:
            return f"Значення: {self.selected_value}"
        info = self.value_info
        return f"{info['value']} ({info['description']}, {info['percentage']}%)"