import tkinter as tk
from tkinter import messagebox
from editor import PointEditor, LineEditor, RectEditor, EllipseEditor


class ShapeObjectsEditor:
    """Головний клас редактора графічних об'єктів
    Інтерфейс модуля shape_editor"""
    
    MAX_SHAPES = 104  # Варіант 4: Ж + 100 = 4 + 100
    
    def __init__(self, root):
        self._root = root
        self._root.title("Графічний редактор об'єктів")
        self._root.geometry("800x600")
        
        # Статичний масив для об'єктів Shape* (варіант 4: Ж mod 3 = 1)
        self._pcshape = [None] * self.MAX_SHAPES
        self._shape_count = 0
        
        # Поточний редактор (вказівник на базовий клас ShapeEditor)
        self._pse = None
        
        # Поточний індекс меню
        self._current_menu_index = 0
        
        # Спочатку створюємо меню та канву
        self._create_menu()
        self._create_canvas()
        
        # Тільки після цього встановлюємо початковий режим
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
        
        # Додаємо пункти меню
        self._objects_menu.add_command(label="Крапка", command=self.start_point_editor)
        self._objects_menu.add_command(label="Лінія", command=self.start_line_editor)
        self._objects_menu.add_command(label="Прямокутник", command=self.start_rect_editor)
        self._objects_menu.add_command(label="Еліпс", command=self.start_ellipse_editor)
        
        # Меню Довідка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self._show_about)
    
    def _create_canvas(self):
        """Створення канви для малювання"""
        # Рамка для канви
        canvas_frame = tk.Frame(self._root, bg="white", relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Канва для малювання
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
        self._current_menu_index = 0
        self._on_init_menu_popup()
    
    def start_line_editor(self):
        """Початок вводу об'єктів-ліній"""
        if self._pse:
            del self._pse
        self._pse = LineEditor(self._canvas, self)
        self._current_menu_index = 1
        self._on_init_menu_popup()
    
    def start_rect_editor(self):
        """Початок вводу прямокутників"""
        if self._pse:
            del self._pse
        self._pse = RectEditor(self._canvas, self)
        self._current_menu_index = 2
        self._on_init_menu_popup()
    
    def start_ellipse_editor(self):
        """Початок вводу еліпсів"""
        if self._pse:
            del self._pse
        self._pse = EllipseEditor(self._canvas, self)
        self._current_menu_index = 3
        self._on_init_menu_popup()
    
    def _on_init_menu_popup(self):
        for i in range(4):
            self._objects_menu.entryconfigure(i, background="")
        
        self._objects_menu.entryconfigure(
            self._current_menu_index, 
            background="lightblue"
        )
    
    def on_lb_down(self, event):
        if self._pse:
            self._pse.on_lb_down(event)
    
    def on_lb_up(self, event):
        if self._pse:
            self._pse.on_lb_up(event)
    
    def on_mouse_move(self, event):
        if self._pse:
            self._pse.on_mouse_move(event)
    
    def on_paint(self):
    
        self._canvas.delete("all")
        
        for i in range(self._shape_count):
            if self._pcshape[i]:
                self._pcshape[i].show(self._canvas)
    
    def add_shape(self, shape):
        """Додавання нової фігури до масиву Shape*"""
        if self._shape_count < self.MAX_SHAPES:
            self._pcshape[self._shape_count] = shape
            self._shape_count += 1
        else:
            messagebox.showwarning(
                "Попередження", 
                f"Досягнуто максимальну кількість об'єктів: {self.MAX_SHAPES}"
            )
    
    def _clear_canvas(self):
        """Очищення масиву об'єктів"""
        self._canvas.delete("all")
        self._pcshape = [None] * self.MAX_SHAPES
        self._shape_count = 0
    
    def _show_about(self):
        """Інформація про програму"""
        info = """Лабораторна робота №2
Варіант 4 (Ж = 4)

Параметри варіанту:

• Масив: статичний Shape *pcshape[104]
• Гумовий слід: суцільна чорна лінія
• Прямокутник:
  - Ввід: по двом протилежним кутам
  - Відображення: чорний контур без заповнення
• Еліпс:
  - Ввід: від центру до кута
  - Відображення: чорний контур з 
    померанчевим заповненням
• Позначка: в меню (OnInitMenuPopup)"""
        
        messagebox.showinfo("Про програму", info)