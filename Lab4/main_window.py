import tkinter as tk
from tkinter import messagebox
from my_editor import MyEditor
from shape import PointShape, LineShape, RectShape, EllipseShape
from line_oo_shape import LineOOShape
from cube_shape import CubeShape


class MainWindow:
    """Головне вікно програми"""
    
    def __init__(self, root):
        self._root = root
        self._root.title("Графічний редактор Lab4 - Рефакторинг")
        self._root.geometry("900x700")
        
        self._create_canvas()
        
        # Динамічний об'єкт MyEditor
        self._ped = MyEditor(self._root, self._canvas)
        
        self._create_menu()
        self._create_toolbar()
        
        # Встановлюємо початковий режим
        self._start_point()
    
    def __del__(self):
        """Деструктор - знищує динамічний об'єкт MyEditor"""
        if hasattr(self, '_ped') and self._ped:
            del self._ped
            self._ped = None
    
    def _create_menu(self):
        """Створення меню"""
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новий", command=self._clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self._root.quit)
        
        # Меню Об'єкти
        objects_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)
        objects_menu.add_command(label="Крапка", command=self._start_point)
        objects_menu.add_command(label="Лінія", command=self._start_line)
        objects_menu.add_command(label="Прямокутник", command=self._start_rect)
        objects_menu.add_command(label="Еліпс", command=self._start_ellipse)
        objects_menu.add_separator()
        objects_menu.add_command(label="Лінія з кружечками", command=self._start_line_oo)
        objects_menu.add_command(label="Каркас куба", command=self._start_cube)
        
        # Меню Довідка - ВИПРАВЛЕНО
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self._show_about)
    
    def _create_toolbar(self):
        toolbar_frame = tk.Frame(self._root, bd=1, relief=tk.RAISED)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        
        self._toolbar_buttons = []
        
        # 6 кнопок для 6 типів фігур
        buttons_data = [
            ("●", "Крапка", self._start_point),
            ("／", "Лінія", self._start_line),
            ("▭", "Прямокутник", self._start_rect),
            ("⬭", "Еліпс", self._start_ellipse),
            ("●═●", "Лінія з кружечками", self._start_line_oo),
            ("▢", "Каркас куба", self._start_cube),
        ]
        
        for text, tooltip, command in buttons_data:
            btn = tk.Button(
                toolbar_frame,
                text=text,
                width=5,
                command=command,
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self._create_tooltip(btn, tooltip)
            self._toolbar_buttons.append(btn)
        
       
        separator = tk.Frame(toolbar_frame, width=2, bd=1, relief=tk.SUNKEN)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
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
    
        btn_help = tk.Button(
            toolbar_frame,
            text="?",
            width=4,
            command=self._show_about,
            relief=tk.RAISED,
            bd=2,
            bg="lightyellow"
        )
        btn_help.pack(side=tk.RIGHT, padx=2, pady=2)
        self._create_tooltip(btn_help, "Довідка")
    
    def _create_tooltip(self, widget, text):
        """Створення tooltip"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip, text=text,
                background="yellow", relief=tk.SOLID,
                borderwidth=1, padx=5, pady=2, font=("Arial", 9)
            )
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _create_canvas(self):
        """Створення канви"""
        canvas_frame = tk.Frame(self._root, bg="white", relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._canvas = tk.Canvas(canvas_frame, bg="white", cursor="cross")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        
        self._canvas.bind("<Button-1>", self._on_lb_down)
        self._canvas.bind("<ButtonRelease-1>", self._on_lb_up)
        self._canvas.bind("<Motion>", self._on_mouse_move)
    
    def _update_toolbar_state(self, active_index):
        for i, btn in enumerate(self._toolbar_buttons):
            if i == active_index:
                btn.config(relief=tk.SUNKEN, bg="lightblue")
            else:
                btn.config(relief=tk.RAISED, bg="SystemButtonFace")
    
    # Методи запуску редагування
    def _start_point(self):
        self._ped.start(PointShape())
        self._update_toolbar_state(0)
    
    def _start_line(self):
        self._ped.start(LineShape())
        self._update_toolbar_state(1)
    
    def _start_rect(self):
        self._ped.start(RectShape())
        self._update_toolbar_state(2)
    
    def _start_ellipse(self):
        self._ped.start(EllipseShape())
        self._update_toolbar_state(3)
    
    def _start_line_oo(self):
        self._ped.start(LineOOShape())
        self._update_toolbar_state(4)
    
    def _start_cube(self):
        self._ped.start(CubeShape())
        self._update_toolbar_state(5)
    
    # Обробники подій
    def _on_lb_down(self, event):
        if self._ped:
            self._ped.on_lb_down(event)
    
    def _on_lb_up(self, event):
        if self._ped:
            self._ped.on_lb_up(event)
    
    def _on_mouse_move(self, event):
        if self._ped:
            self._ped.on_mouse_move(event)
    
    def _clear_canvas(self):
        if self._ped:
            self._ped.clear_canvas()
    
    def _show_about(self):
        """Інформація про програму"""
        info = """Лабораторна робота №4

Варіант 4 (парний номер)

Модульна структура:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Lab4.py - точка входу
• main_window.py - GUI + Toolbar
• my_editor.py - MyEditor (рефакторинг)
• shape.py - базові фігури
• line_oo_shape.py - лінія з кружечками
• cube_shape.py - каркас куба
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # Використовуємо messagebox безпосередньо
        messagebox.showinfo("Про програму", info)