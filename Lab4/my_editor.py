import tkinter as tk
from tkinter import messagebox
from shape import Shape


class MyEditor:
    """Головний клас графічного редактора (Lab4)"""
    
    MAX_SHAPES = 105
    
    def __init__(self, root, canvas):
        """Конструктор"""
        self._root = root
        self._canvas = canvas
        
        # Динамічний масив вказівників на об'єкти Shape
        self._pshape = []
        self._shape_count = 0
        
        # Поточна фігура, що редагується
        self._current_shape = None
        
        # Стан малювання
        self._is_drawing = False
        self._start_x = 0
        self._start_y = 0
        self._current_x = 0
        self._current_y = 0
        self._rubber_line = None
        
        # Режим редагування
        self._current_mode = "Крапка"
    
    def __del__(self):
        self._pshape.clear()
    
    def start(self, shape):
        """Початок редагування об'єкта певного типу"""
        self._current_shape = shape
        
        # Визначаємо режим за типом об'єкта
        shape_name = type(shape).__name__
        mode_map = {
            'PointShape': 'Крапка',
            'LineShape': 'Лінія',
            'RectShape': 'Прямокутник',
            'EllipseShape': 'Еліпс',
            'LineOOShape': 'Лінія з кружечками',
            'CubeShape': 'Каркас куба'
        }
        self._current_mode = mode_map.get(shape_name, 'Невідомо')
        self._update_window_title()
    
    def on_lb_down(self, event):
        """Обробка WM_LBUTTONDOWN - натискання лівої кнопки миші"""
        if not self._current_shape:
            return
        
        self._is_drawing = True
        self._start_x = event.x
        self._start_y = event.y
        self._current_x = event.x
        self._current_y = event.y
        
        # Для точки достатньо одного кліка
        if type(self._current_shape).__name__ == 'PointShape':
            shape = type(self._current_shape)()
            shape.set(event.x, event.y, event.x, event.y)
            self._add_shape(shape)
            self.on_paint()
            self._is_drawing = False
    
    def on_lb_up(self, event):
        """Обробка WM_LBUTTONUP - відпускання лівої кнопки миші"""
        if not self._is_drawing or not self._current_shape:
            return
        
        self._is_drawing = False
        
        # Видалити гумовий слід
        if self._rubber_line:
            self._canvas.delete(self._rubber_line)
            self._rubber_line = None
        
        # Створити фігуру
        self._create_shape(self._start_x, self._start_y, event.x, event.y)
        self.on_paint()
    
    def on_mouse_move(self, event):
        """Обробка WM_MOUSEMOVE - переміщення миші"""
        if not self._is_drawing or not self._current_shape:
            return
        
        # Стерти попередній гумовий слід
        if self._rubber_line:
            self._canvas.delete(self._rubber_line)
        
        self._current_x = event.x
        self._current_y = event.y
        
        # Намалювати новий гумовий слід
        self._draw_rubber_band()
    
    def on_paint(self):
        """Обробка WM_PAINT - перемалювання вікна"""
        self._canvas.delete("all")
        
        # Цикл відображення об'єктів
        for shape in self._pshape:
            if shape:
                shape.show(self._canvas)
    
    def _create_shape(self, x1, y1, x2, y2):
        """Створення фігури відповідно до поточного типу"""
        if not self._current_shape:
            return
        
        shape_type = type(self._current_shape)
        shape = shape_type()
        
        # Обробка різних типів фігур
        if shape_type.__name__ == 'RectShape':
            # Від центру до кута (варіант 5)
            width = abs(x2 - x1) * 2
            height = abs(y2 - y1) * 2
            shape.set(
                x1 - width // 2, y1 - height // 2,
                x1 + width // 2, y1 + height // 2
            )
        elif shape_type.__name__ in ['CubeShape']:
            # Від центру для куба
            width = abs(x2 - x1) * 2
            height = abs(y2 - y1) * 2
            shape.set(
                x1 - width // 2, y1 - height // 2,
                x1 + width // 2, y1 + height // 2
            )
        else:
            # Для інших фігур - по двом точкам
            shape.set(x1, y1, x2, y2)
        
        self._add_shape(shape)
    
    def _draw_rubber_band(self):
        """Малювання гумового сліду"""
        
        if not self._current_shape:
            return
        
        shape_type = type(self._current_shape).__name__
        
        if shape_type == 'PointShape':
            return
        
        dash_pattern = (5, 3)  # Пунктир
        
        if shape_type == 'LineShape' or shape_type == 'LineOOShape':
            self._rubber_line = self._canvas.create_line(
                self._start_x, self._start_y,
                self._current_x, self._current_y,
                fill="gray", width=1, dash=dash_pattern
            )
        elif shape_type == 'RectShape' or shape_type == 'CubeShape':
            # Від центру
            width = abs(self._current_x - self._start_x) * 2
            height = abs(self._current_y - self._start_y) * 2
            x1 = self._start_x - width // 2
            y1 = self._start_y - height // 2
            x2 = self._start_x + width // 2
            y2 = self._start_y + height // 2
            
            self._rubber_line = self._canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="gray", fill="", width=1, dash=dash_pattern
            )
        elif shape_type == 'EllipseShape':
            # По двом кутам
            self._rubber_line = self._canvas.create_oval(
                self._start_x, self._start_y,
                self._current_x, self._current_y,
                outline="gray", fill="", width=1, dash=dash_pattern
            )
    
    def _add_shape(self, shape):
        """Додавання фігури до масиву"""
        if self._shape_count < self.MAX_SHAPES:
            self._pshape.append(shape)
            self._shape_count += 1
        else:
            messagebox.showwarning(
                "Попередження",
                f"Досягнуто максимальну кількість об'єктів: {self.MAX_SHAPES}"
            )
    
    def clear_canvas(self):
        """Очищення канви та масиву"""
        self._canvas.delete("all")
        self._pshape.clear()
        self._shape_count = 0
    
    def _update_window_title(self):
        """Оновлення заголовку вікна"""
        self._root.title(f"Графічний редактор Lab4 - Режим: {self._current_mode}")
    
    def get_current_mode(self):
        """Отримати поточний режим"""
        return self._current_mode