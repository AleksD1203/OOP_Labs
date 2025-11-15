import tkinter as tk
from tkinter import ttk, messagebox, Menu, filedialog
from my_editor import MyEditor
from my_table import MyTable
import os

class GraphicsEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Графічний редактор - Lab5")
        self.root.geometry("900x700")
        
        # Ініціалізація змінних
        self.drawing = False
        self.current_item = None
        self.current_file = None
        self.active_tool_button = None
        self.tool_buttons = {}
        self.status_var = tk.StringVar()
        
        # Singleton редактор
        self.editor = MyEditor()
        self.editor.add_observer(self.on_editor_event)
        
        # Немодальне вікно таблиці
        self.table = MyTable()
        self.table.set_selection_callback(self.on_table_selection)
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Головний контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Toolbar
        self.setup_toolbar(main_frame)
        
        # Canvas для малювання
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Прив'язка подій миші
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Статус бар
        self.setup_statusbar(main_frame)
        
        # Меню
        self.setup_menu()
        
        self.redraw_canvas()
    
    def setup_toolbar(self, parent):
        """Налаштування панелі інструментів з підсвічуванням"""
        toolbar = tk.Frame(parent, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Кнопки інструментів малювання
        tools = [
            ("●", "Крапка", "Point"),
            ("／", "Лінія", "Line"), 
            ("□", "Прямокутник", "Rectangle"),
            ("○", "Еліпс", "Ellipse")
        ]
        
        for icon, text, shape_type in tools:
            btn = tk.Button(
                toolbar,
                text=icon,
                width=4,
                command=lambda st=shape_type, btn_text=text: self.set_active_tool(st, btn_text),
                relief=tk.RAISED,
                bd=2,
                font=("Arial", 12),
                bg="SystemButtonFace"
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.tool_buttons[shape_type] = btn
            self.create_tooltip(btn, text)
        
        # Встановлюємо першу кнопку як активну
        self.set_active_tool("Point", "Крапка")
        
        # Роздільник
        separator = tk.Frame(toolbar, width=2, bd=1, relief=tk.SUNKEN)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Кнопки файлових операцій
        file_tools = [
            ("💾", "Зберегти", self.save_drawing),
            ("📂", "Відкрити", self.open_drawing),
            ("🗑", "Очистити", self.clear_canvas),
            ("📊", "Таблиця", self.table.show)
        ]
        
        for icon, text, command in file_tools:
            btn = tk.Button(
                toolbar,
                text=icon,
                width=4,
                command=command,
                relief=tk.RAISED,
                bd=2,
                font=("Arial", 12)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.create_tooltip(btn, text)
    
    def set_active_tool(self, shape_type, tool_name):
        """Встановлення активного інструменту з підсвічуванням"""
        # Скидаємо підсвічування всіх кнопок
        for btn in self.tool_buttons.values():
            btn.config(relief=tk.RAISED, bg="SystemButtonFace")
        
        # Підсвічуємо активну кнопку
        if shape_type in self.tool_buttons:
            self.tool_buttons[shape_type].config(relief=tk.SUNKEN, bg="lightblue")
            self.active_tool_button = self.tool_buttons[shape_type]
        
        # Встановлюємо тип фігури в редакторі
        self.editor.set_shape_type(shape_type)
        
        # Оновлюємо статус
        self.status_var.set(f"Обрано інструмент: {tool_name}")
    
    def create_tooltip(self, widget, text):
        """Створення підказки для кнопок toolbar"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background="yellow",
                relief=tk.SOLID,
                borderwidth=1,
                padx=5,
                pady=2,
                font=("Arial", 9)
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def setup_statusbar(self, parent):
        """Налаштування статус бара"""
        statusbar = ttk.Frame(parent)
        statusbar.pack(fill=tk.X, pady=2)
        
        self.status_var.set("Готовий до малювання. Оберіть інструмент.")
        
        status_label = ttk.Label(statusbar, textvariable=self.status_var, 
                                relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(fill=tk.X, padx=5, pady=2)
    
    def setup_menu(self):
        """Налаштування меню"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новий", command=self.clear_canvas, accelerator="Ctrl+N")
        file_menu.add_command(label="Відкрити...", command=self.open_drawing, accelerator="Ctrl+O")
        file_menu.add_command(label="Зберегти", command=self.save_drawing, accelerator="Ctrl+S")
        file_menu.add_command(label="Зберегти як...", command=self.save_drawing_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.on_closing, accelerator="Ctrl+Q")
        
        # Меню Вид
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Показати таблицю", command=self.table.show, accelerator="Ctrl+T")
        
        # Меню Інструменти
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Інструменти", menu=tools_menu)
        tools_menu.add_command(label="Крапка", command=lambda: self.set_active_tool("Point", "Крапка"))
        tools_menu.add_command(label="Лінія", command=lambda: self.set_active_tool("Line", "Лінія"))
        tools_menu.add_command(label="Прямокутник", command=lambda: self.set_active_tool("Rectangle", "Прямокутник"))
        tools_menu.add_command(label="Еліпс", command=lambda: self.set_active_tool("Ellipse", "Еліпс"))
        
        # Меню Допомога
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Допомога", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self.show_about)
        
        # Гарячі клавіші
        self.root.bind('<Control-n>', lambda e: self.clear_canvas())
        self.root.bind('<Control-o>', lambda e: self.open_drawing())
        self.root.bind('<Control-s>', lambda e: self.save_drawing())
        self.root.bind('<Control-t>', lambda e: self.table.show())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        
        # Гарячі клавіші для інструментів
        self.root.bind('<Key-1>', lambda e: self.set_active_tool("Point", "Крапка"))
        self.root.bind('<Key-2>', lambda e: self.set_active_tool("Line", "Лінія"))
        self.root.bind('<Key-3>', lambda e: self.set_active_tool("Rectangle", "Прямокутник"))
        self.root.bind('<Key-4>', lambda e: self.set_active_tool("Ellipse", "Еліпс"))
    
    def save_drawing(self):
        """Зберегти малюнок"""
        if self.current_file:
            success = self.editor.save_to_file(self.current_file)
            if success:
                self.status_var.set(f"Малюнок збережено: {self.current_file}")
                messagebox.showinfo("Збереження", "Малюнок успішно збережено!")
        else:
            self.save_drawing_as()
    
    def save_drawing_as(self):
        """Зберегти малюнок як..."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Зберегти малюнок як..."
        )
        
        if filename:
            success = self.editor.save_to_file(filename)
            if success:
                self.current_file = filename
                self.status_var.set(f"Малюнок збережено: {os.path.basename(filename)}")
                messagebox.showinfo("Збереження", "Малюнок успішно збережено!")
    
    def open_drawing(self):
        """Відкрити малюнок"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Відкрити малюнок"
        )
        
        if filename:
            success = self.editor.load_from_file(filename)
            if success:
                self.current_file = filename
                self.status_var.set(f"Малюнок завантажено: {os.path.basename(filename)}")
                messagebox.showinfo("Завантаження", "Малюнок успішно завантажено!")
    
    def show_about(self):
        """Показати інформацію про програму"""
        messagebox.showinfo("Про програму", 
                          "Графічний редактор - Lab5\n\n"
                          "Варіант 4\n")
    
    def on_mouse_down(self, event):
        self.drawing = True
        self.editor.start_drawing(event.x, event.y)
        
        if self.editor._current_shape_type == "Point":
            self.editor.finish_drawing(event.x, event.y)
            self.drawing = False
            self.status_var.set(f"Додано точку ({event.x}, {event.y})")
    
    def on_mouse_drag(self, event):
        if self.drawing and self.editor._current_shape_type != "Point":
            self.redraw_canvas()
            
            start_x, start_y = self.editor._start_x, self.editor._start_y
            if self.editor._current_shape_type == "Line":
                self.current_item = self.canvas.create_line(start_x, start_y, event.x, event.y, 
                                                           fill="gray", width=2, dash=(4, 2))
            elif self.editor._current_shape_type == "Ellipse":
                self.current_item = self.canvas.create_oval(start_x, start_y, event.x, event.y, 
                                                           outline="gray", width=2, dash=(4, 2))
            elif self.editor._current_shape_type == "Rectangle":
                self.current_item = self.canvas.create_rectangle(start_x, start_y, event.x, event.y, 
                                                                outline="gray", width=2, dash=(4, 2))
    
    def on_mouse_up(self, event):
        if self.drawing and self.editor._current_shape_type != "Point":
            if self.current_item:
                self.canvas.delete(self.current_item)
            self.editor.finish_drawing(event.x, event.y)
            self.drawing = False
            
            shape_name = ""
            if self.editor._current_shape_type == "Line":
                shape_name = "лінію"
            elif self.editor._current_shape_type == "Ellipse":
                shape_name = "еліпс"
            elif self.editor._current_shape_type == "Rectangle":
                shape_name = "прямокутник"
            
            self.status_var.set(f"Додано {shape_name}")
    
    def clear_canvas(self):
        if messagebox.askyesno("Очищення", "Ви впевнені, що хочете очистити полотно?"):
            self.editor.clear_shapes()
            self.canvas.delete("all")
            self.status_var.set("Полотно очищено")
    
    def redraw_canvas(self):
        self.canvas.delete("all")
        for shape in self.editor.get_shapes():
            shape.draw(self.canvas)
    
    def on_editor_event(self, event_type: str, data=None):
        if event_type == "shape_added":
            self.table.add_shape(data)
            self.redraw_canvas()
        elif event_type == "shapes_cleared":
            self.table.clear()
            self.redraw_canvas()
        elif event_type == "shape_selected":
            self.redraw_canvas()
            if data is not None and data < len(self.editor.get_shapes()):
                shape = self.editor.get_shapes()[data]
                self.status_var.set(f"Виділено: {shape.get_name()}")
        elif event_type == "shape_deleted":
            # ВИПРАВЛЕННЯ: повністю перебудовуємо таблицю після видалення
            self.table.clear()
            for shape in self.editor.get_shapes():
                self.table.add_shape(shape)
            self.redraw_canvas()
            self.status_var.set("Об'єкт видалено")
        elif event_type == "shapes_loaded":
            self.table.clear()
            for shape in self.editor.get_shapes():
                self.table.add_shape(shape)
            self.redraw_canvas()
            self.status_var.set("Малюнок завантажено")
    
    def on_table_selection(self, index, delete=False):
        """Обробник виділення/видалення з таблиці"""
        if delete:
            # Перевіряємо, чи індекс коректний
            if index < len(self.editor.get_shapes()):
                shape_name = self.editor.get_shapes()[index].get_name()
                # Спитати підтвердження ПЕРШЕ
                if messagebox.askyesno("Видалення", f"Видалити {shape_name}?"):
                    # Якщо так - видаляємо з редактора
                    self.editor.delete_shape(index)
                    # Таблиця оновиться автоматично через on_editor_event("shape_deleted")
                # Якщо ні - нічого не робимо (об'єкт залишається)
            else:
                messagebox.showwarning("Помилка", "Об'єкт не знайдено")
        else:
            # Звичайне виділення
            self.editor.select_shape(index)
    
    def on_closing(self):
        if messagebox.askokcancel("Вихід", "Ви впевнені, що хочете вийти?"):
            if hasattr(self.table, '_window') and self.table._window:
                self.table._on_close()
            self.root.destroy()

def main():
    root = tk.Tk()
    app = GraphicsEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()