import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import module1
import module2

class BaseWindow(ABC):
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        
    @abstractmethod
    def create_window(self): pass
    @abstractmethod
    def setup_ui(self): pass

class MainApplication(BaseWindow):
    def __init__(self):
        super().__init__()
        self.display_text = ""
        
    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Lab1")
        self.window.geometry("800x600")
        self.window.geometry("+%d+%d" % (
            (self.window.winfo_screenwidth() // 2) - 400,
            (self.window.winfo_screenheight() // 2) - 300
        ))
        
    def setup_ui(self):
        self.create_menu()
        self.create_main_area()
        
    def create_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        actions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Дії", menu=actions_menu)
        actions_menu.add_command(label="Робота1", command=self.work1_handler)
        actions_menu.add_command(label="Робота2", command=self.work2_handler)
        actions_menu.add_separator()
        actions_menu.add_command(label="Вихід", command=self.exit_handler)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self.about_handler)
        
    def create_main_area(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        ttk.Label(main_frame, text="Лабораторна робота №1", 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(0, 20))
        
        self.result_frame = ttk.LabelFrame(main_frame, text="Результати виконання", padding="10")
        self.result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)
        
        self.text_display = tk.Text(self.result_frame, height=15, font=("Consolas", 11),
                                   wrap=tk.WORD, state=tk.DISABLED)
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, 
                                 command=self.text_display.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_display.configure(yscrollcommand=scrollbar.set)
        
        self.update_display("Програма запущена. Оберіть дію з меню.")
        
    def update_display(self, message):
        self.text_display.configure(state=tk.NORMAL)
        self.text_display.insert(tk.END, f"{message}\n")
        self.text_display.configure(state=tk.DISABLED)
        self.text_display.see(tk.END)
        
    def work1_handler(self):
        try:
            mod1 = module1.Module1(self.window)
            result = mod1.execute()
            if result:
                self.update_display(f"Робота1: {mod1.get_result_text()}")
            else:
                self.update_display("Робота1 скасована")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка Робота1: {e}")
            
    def work2_handler(self):
        try:
            mod2 = module2.Module2(self.window)
            result = mod2.execute()
            if result:
                self.update_display(f"Робота2: {mod2.get_result_value()}")
            else:
                self.update_display("Робота2 скасована")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка Робота2: {e}")
            
    def about_handler(self):
        messagebox.showinfo("Про програму", 
            "Назва: Лабораторна робота №1\n\nВарiанти завдань: B₁=0, B₂=1") 
        
    def exit_handler(self):
        if messagebox.askokcancel("Вихід", "Вийти з програми?"):
            self.window.quit()
            
    def run(self):
        self.create_window()
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.exit_handler)
        self.window.mainloop()

def main():
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка запуску: {e}")

if __name__ == "__main__":
    main()