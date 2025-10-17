import tkinter as tk
from tkinter import messagebox
from editor import PointEditor, LineEditor, RectEditor, EllipseEditor


class ShapeObjectsEditor:
    """Головний клас редактора графічних об'єктів з Toolbar"""
    
    MAX_SHAPES = 105  # Варіант 5: Ж + 100 = 5 + 100
    
    def __init__(self, root):
        self._root = root
        self._root.title("Графічний редактор - Режим: Крапка")
        self._root.geometry("900x650")
        
        # Статичний масив для об'єктів Shape*
        self._pcshape = [None] * self.MAX_SHAPES
        self._shape_count = 0
        
        # Поточний редактор (вказівник на базовий клас ShapeEditor)
        self._pse = None
        
        # Поточний режим
        self._current_mode = "Крапка"
        
        # Створюємо інтерфейс
        self._create_menu()
        self._create_toolbar() 
        self._create_canvas()
        
        # Встановлюємо початковий режим
        self.start_point_editor()
    
    def _create_menu(self):
        """Створення меню програми"""
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новий", command=self._clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self._root.quit)
        
        # Меню Об'єкти
        self._objects_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Об'єкти", menu=self._objects_menu)
        
        self._objects_menu.add_command(label="Крапка", command=self.start_point_editor)
        self._objects_menu.add_command(label="Лінія", command=self.start_line_editor)
        self._objects_menu.add_command(label="Прямокутник", command=self.start_rect_editor)
        self._objects_menu.add_command(label="Еліпс", command=self.start_ellipse_editor)
        
        # Меню Довідка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self._show_about)
    
    def _create_toolbar(self):
        """Створення панелі інструментів (Toolbar)"""
        # Рамка для toolbar
        toolbar_frame = tk.Frame(self._root, bd=1, relief=tk.RAISED)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Зберігаємо кнопки для керування їх станом
        self._toolbar_buttons = []
        
        # Кнопка "Крапка" з підказкою (tooltip)
        btn_point = tk.Button(
            toolbar_frame, 
            text="●", 
            width=4,
            command=self.start_point_editor,
            relief=tk.RAISED,
            bd=2
        )
        btn_point.pack(side=tk.LEFT, padx=2, pady=2)
        self._create_tooltip(btn_point, "Крапка")
        self._toolbar_buttons.append(btn_point)
        
        # Кнопка "Лінія"
        btn_line = tk.Button(
            toolbar_frame,
            text="／",
            width=4,
            command=self.start_line_editor,
            relief=tk.RAISED,
            bd=2
        )
        btn_line.pack(side=tk.LEFT, padx=2, pady=2)
        self._create_tooltip(btn_line, "Лінія")
        self._toolbar_buttons.append(btn_line)
        
        # Кнопка "Прямокутник"
        btn_rect = tk.Button(
            toolbar_frame,
            text="▭",
            width=4,
            command=self.start_rect_editor,
            relief=tk.RAISED,
            bd=2
        )
        btn_rect.pack(side=tk.LEFT, padx=2, pady=2)
        self._create_tooltip(btn_rect, "Прямокутник")
        self._toolbar_buttons.append(btn_rect)
        
        # Кнопка "Еліпс"
        btn_ellipse = tk.Button(
            toolbar_frame,
            text="⬭",
            width=4,
            command=self.start_ellipse_editor,
            relief=tk.RAISED,
            bd=2
        )
        btn_ellipse.pack(side=tk.LEFT, padx=2, pady=2)
        self._create_tooltip(btn_ellipse, "Еліпс")
        self._toolbar_buttons.append(btn_ellipse)
        
        # Роздільник
        separator = tk.Frame(toolbar_frame, width=2, bd=1, relief=tk.SUNKEN)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Кнопка "Очистити"
        btn_clear = tk.Button(
            toolbar_frame,
            text="🗑",
            width=4,
            command=self._clear_canvas,
            relief=tk.RAISED,
            bd=2
        )
        btn_clear.pack(side=tk.LEFT, padx=2, pady=2)
        self._create_tooltip(btn_clear, "Очистити")
    
    def on_notify(self, widget_id):
        """Обробка WM_NOTIFY - повідомлень від елементів toolbar"""
        pass
    
    def _create_tooltip(self, widget, text):
        """Створення підказки (tooltip) для віджета"""
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
            
            self.on_notify(id(widget))
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _update_toolbar_state(self, active_index):
        """Оновлення стану кнопок toolbar (підсвічування активної)"""
        for i, btn in enumerate(self._toolbar_buttons):
            if i == active_index:
                btn.config(relief=tk.SUNKEN, bg="lightblue")
            else:
                btn.config(relief=tk.RAISED, bg="SystemButtonFace")
    
    def _create_canvas(self):
        """Створення канви для малювання"""
        canvas_frame = tk.Frame(self._root, bg="white", relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._canvas = tk.Canvas(canvas_frame, bg="white", cursor="cross")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        
        # Прив'язка обробників подій миші
        self._canvas.bind("<Button-1>", self.on_lb_down)
        self._canvas.bind("<ButtonRelease-1>", self.on_lb_up)
        self._canvas.bind("<Motion>", self.on_mouse_move)
    
    def start_point_editor(self):
        """Початок вводу точкових об'єктів"""
        if self._pse:
            del self._pse
        self._pse = PointEditor(self._canvas, self)
        self._current_mode = "Крапка"
        self._update_window_title()  # Варіант 5: позначка в заголовку
        self._update_toolbar_state(0)
    
    def start_line_editor(self):
        """Початок вводу об'єктів-ліній"""
        if self._pse:
            del self._pse
        self._pse = LineEditor(self._canvas, self)
        self._current_mode = "Лінія"
        self._update_window_title()
        self._update_toolbar_state(1)
    
    def start_rect_editor(self):
        """Початок вводу прямокутників"""
        if self._pse:
            del self._pse
        self._pse = RectEditor(self._canvas, self)
        self._current_mode = "Прямокутник"
        self._update_window_title()
        self._update_toolbar_state(2)
    
    def start_ellipse_editor(self):
        """Початок вводу еліпсів"""
        if self._pse:
            del self._pse
        self._pse = EllipseEditor(self._canvas, self)
        self._current_mode = "Еліпс"
        self._update_window_title()
        self._update_toolbar_state(3)
    
    def _update_window_title(self):
        """Оновлення заголовку вікна з поточним режимом"""
        self._root.title(f"Графічний редактор - Режим: {self._current_mode}")
    
    def on_lb_down(self, event):
        """Обробка WM_LBUTTONDOWN - натискання лівої кнопки миші"""
        if self._pse:
            self._pse.on_lb_down(event)
    
    def on_lb_up(self, event):
        """Обробка WM_LBUTTONUP - відпускання лівої кнопки миші"""
        if self._pse:
            self._pse.on_lb_up(event)
    
    def on_mouse_move(self, event):
        """Обробка WM_MOUSEMOVE - переміщення миші"""
        if self._pse:
            self._pse.on_mouse_move(event)
    
    def on_paint(self):
        """Обробка WM_PAINT - перемалювання вікна"""
        self._canvas.delete("all")
        
        # Поліморфний виклик Show для всіх об'єктів у масиві
        for i in range(self._shape_count):
            if self._pcshape[i]:
                self._pcshape[i].show(self._canvas)
    
    def add_shape(self, shape):
        """Додавання нової фігури до масиву Shape"""
        if self._shape_count < self.MAX_SHAPES:
            self._pcshape[self._shape_count] = shape
            self._shape_count += 1
        else:
            messagebox.showwarning(
                "Попередження", 
                f"Досягнуто максимальну кількість об'єктів: {self.MAX_SHAPES}"
            )
    
    def _clear_canvas(self):
        """Очищення канви та масиву об'єктів"""
        self._canvas.delete("all")
        self._pcshape = [None] * self.MAX_SHAPES
        self._shape_count = 0
    
    def _show_about(self):
        """Інформація про програму"""
        info = """Лабораторна робота №3
Графічний редактор з інтерфейсом

Студент: Варіант 5 (Ж = Ж_лаб2 + 1 = 5)

Параметри варіанту:

• Масив: статичний Shape *pcshape[105]
• Гумовий слід: суцільна червона лінія
• Прямокутник:
  - Ввід: від центру до кута
  - Відображення: контур з білим заповненням
• Еліпс:
  - Ввід: по двом протилежним кутам
  - Відображення: контур без заповнення
• Позначка: в заголовку вікна

Модульна структура:

• Lab3.py - головний файл
• shape_editor.py - ShapeObjectsEditor + Toolbar
• editor.py - Editor та похідні
• shape.py - Shape та похідні"""
        
        messagebox.showinfo("Про програму", info)