from abc import ABC, abstractmethod
from shape import PointShape, LineShape, RectShape, EllipseShape


class Editor(ABC):
    """Базовий абстрактний клас редактора"""
    
    @abstractmethod
    def on_lb_down(self, event):
        """Обробка WM_LBUTTONDOWN"""
        pass
    
    @abstractmethod
    def on_lb_up(self, event):
        """Обробка WM_LBUTTONUP"""
        pass
    
    @abstractmethod
    def on_mouse_move(self, event):
        """Обробка WM_MOUSEMOVE"""
        pass
    
    @abstractmethod
    def on_paint(self):
        """Обробка WM_PAINT"""
        pass


class ShapeEditor(Editor):
    """Базовий клас для редагування фігур"""
    def __init__(self, canvas, shape_objects_editor):
        self._canvas = canvas
        self._shape_objects_editor = shape_objects_editor
        self._is_drawing = False
        self._start_x = 0
        self._start_y = 0
        self._current_x = 0
        self._current_y = 0
        self._rubber_line = None
    
    def on_lb_down(self, event):
        """Обробка натискання лівої кнопки миші"""
        self._is_drawing = True
        self._start_x = event.x
        self._start_y = event.y
        self._current_x = event.x
        self._current_y = event.y
    
    def on_lb_up(self, event):
        """Обробка відпускання лівої кнопки миші"""
        if self._is_drawing:
            self._is_drawing = False
            # Видалити гумовий слід
            if self._rubber_line:
                self._canvas.delete(self._rubber_line)
                self._rubber_line = None
            
            # Створити фігуру
            self._create_shape(self._start_x, self._start_y, event.x, event.y)
            # Оновити вікно
            self._shape_objects_editor.on_paint()
    
    def on_mouse_move(self, event):
        """Обробка переміщення миші - малювання гумового сліду"""
        if self._is_drawing:
            # Стерти попередній гумовий слід
            if self._rubber_line:
                self._canvas.delete(self._rubber_line)
            
            self._current_x = event.x
            self._current_y = event.y
            
            # Намалювати новий гумовий слід
            self._draw_rubber_band()
    
    def on_paint(self):
        """Базова реалізація перемалювання"""
        pass
    
    def _create_shape(self, x1, y1, x2, y2):
        """Створення фігури"""
        pass
    
    def _draw_rubber_band(self):
        """Малювання гумового сліду"""
        pass


class PointEditor(ShapeEditor):
    """Редактор для точкових об'єктів"""
    
    def on_lb_down(self, event):
        """Для точки достатньо одного кліка"""
        shape = PointShape()
        shape.set(event.x, event.y, event.x, event.y)
        self._shape_objects_editor.add_shape(shape)
        self._shape_objects_editor.on_paint()
    
    def on_lb_up(self, event):
        """Для точки не потрібна обробка відпускання"""
        pass
    
    def on_mouse_move(self, event):
        """Для точки не потрібна обробка переміщення"""
        pass


class LineEditor(ShapeEditor):
    """Редактор для лінійних об'єктів"""
    
    def _create_shape(self, x1, y1, x2, y2):
        """Створення лінії"""
        shape = LineShape()
        shape.set(x1, y1, x2, y2)
        self._shape_objects_editor.add_shape(shape)
    
    def _draw_rubber_band(self):
        """Гумовий слід для лінії"""
        self._rubber_line = self._canvas.create_line(
            self._start_x, self._start_y, 
            self._current_x, self._current_y,
            fill="black", width=1
        )


class RectEditor(ShapeEditor):
    """Редактор для прямокутників"""
    
    def _create_shape(self, x1, y1, x2, y2):
        """Створення прямокутника"""
        shape = RectShape()
        shape.set(x1, y1, x2, y2)
        self._shape_objects_editor.add_shape(shape)
    
    def _draw_rubber_band(self):
        """Гумовий слід для прямокутника"""
        self._rubber_line = self._canvas.create_rectangle(
            self._start_x, self._start_y, 
            self._current_x, self._current_y,
            outline="black", fill="", width=1
        )


class EllipseEditor(ShapeEditor):
    """Редактор для еліпсів"""
    
    def _create_shape(self, x1, y1, x2, y2):
        """Створення еліпса"""
        shape = EllipseShape()
        # x1, y1 - центр; x2, y2 - точка на периметрі охоплюючого прямокутника
        width = abs(x2 - x1) * 2
        height = abs(y2 - y1) * 2
        shape.set(
            x1 - width // 2, y1 - height // 2, 
            x1 + width // 2, y1 + height // 2
        )
        self._shape_objects_editor.add_shape(shape)
    
    def _draw_rubber_band(self):
        """Гумовий слід для еліпса (від центру до кута)"""
        width = abs(self._current_x - self._start_x) * 2
        height = abs(self._current_y - self._start_y) * 2
        x1 = self._start_x - width // 2
        y1 = self._start_y - height // 2
        x2 = self._start_x + width // 2
        y2 = self._start_y + height // 2
        
        self._rubber_line = self._canvas.create_oval(
            x1, y1, x2, y2, 
            outline="black", fill="", width=1
        )