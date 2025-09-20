import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class IDialogModule(ABC):
    @abstractmethod
    def execute(self): pass

class TextInputDialog:
    def __init__(self, parent, title="Введення тексту"):
        self.parent = parent
        self.title = title
        self.result = 0
        self.entered_text = ""
        
    def create_dialog(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("450x180")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.center_window()
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Введіть текст:", font=("Arial", 11)).pack(pady=(0, 10))
        
        self.text_entry = ttk.Entry(main_frame, font=("Arial", 11), width=40)
        self.text_entry.pack(pady=(0, 20), fill=tk.X)
        self.text_entry.focus()
        self.text_entry.bind('<Return>', lambda e: self.ok_clicked())
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="Так", command=self.ok_clicked, width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Відміна", command=self.cancel_clicked, width=12).pack(side=tk.LEFT)
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)
        
    def center_window(self):
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - 225
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - 90
        self.dialog.geometry(f"+{x}+{y}")
        
    def ok_clicked(self):
        self.entered_text = self.text_entry.get().strip()
        if self.entered_text:
            self.result = 1
            self.dialog.destroy()
            
    def cancel_clicked(self):
        self.result = 0
        self.dialog.destroy()
        
    def show(self):
        self.create_dialog()
        self.dialog.wait_window()
        return self.result

class TextValidator:
    @staticmethod
    def get_text_info(text):
        clean = text.strip()
        return {
            'length': len(clean),
            'words': len(clean.split()),
            'chars': len(clean.replace(' ', ''))
        }

class Module1(IDialogModule):
    def __init__(self, parent):
        self.parent = parent
        self.entered_text = ""
        self.text_info = {}
        
    def execute(self):
        dialog = TextInputDialog(self.parent)
        result = dialog.show()
        if result:
            self.entered_text = dialog.entered_text
            self.text_info = TextValidator.get_text_info(self.entered_text)
        return result
            
    def get_result_text(self):
        if not self.entered_text:
            return "Текст не введено"
        info = self.text_info
        return f"'{self.entered_text}' ({info['length']} символів, {info['words']} слів)"
    
    def get_entered_text(self):
        return self.entered_text