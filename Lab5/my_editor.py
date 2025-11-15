import tkinter as tk
from typing import List, Optional, Callable
from shape import Point, Line, Ellipse, Rectangle, Shape
import json
import os

class MyEditor:
    _instance = None
    _shapes: List[Shape] = []
    _current_shape_type: str = "Point"
    _start_x: Optional[int] = None
    _start_y: Optional[int] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MyEditor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._observers: List[Callable] = []
    
    def add_observer(self, observer: Callable):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def notify_observers(self, event_type: str, data=None):
        """Безпечне сповіщення спостерігачів"""
        observers_to_remove = []
        
        for observer in self._observers:
            try:
                observer(event_type, data)
            except tk.TclError as e:
                if "invalid command name" in str(e):
                    observers_to_remove.append(observer)
                else:
                    print(f"Помилка в обсервері: {e}")
            except Exception as e:
                print(f"Помилка в обсервері: {e}")
        
        for observer in observers_to_remove:
            self._observers.remove(observer)
    
    def set_shape_type(self, shape_type: str):
        self._current_shape_type = shape_type
    
    def start_drawing(self, x: int, y: int):
        self._start_x = x
        self._start_y = y
    
    def finish_drawing(self, x: int, y: int):
        if self._start_x is None or self._start_y is None:
            return
        
        shape = None
        if self._current_shape_type == "Point":
            shape = Point(x, y, x, y)
        elif self._current_shape_type == "Line":
            shape = Line(self._start_x, self._start_y, x, y)
        elif self._current_shape_type == "Ellipse":
            shape = Ellipse(self._start_x, self._start_y, x, y)
        elif self._current_shape_type == "Rectangle":
            shape = Rectangle(self._start_x, self._start_y, x, y)
        
        if shape:
            self._shapes.append(shape)
            self.notify_observers("shape_added", shape)
    
    def get_shapes(self) -> List[Shape]:
        return self._shapes.copy()
    
    def clear_shapes(self):
        self._shapes.clear()
        self.notify_observers("shapes_cleared")
    
    def select_shape(self, index: int):
        for i, shape in enumerate(self._shapes):
            shape.set_selected(i == index)
        self.notify_observers("shape_selected", index)
    
    def delete_shape(self, index: int):
        if 0 <= index < len(self._shapes):
            del self._shapes[index]
            self.notify_observers("shape_deleted", index)
    
    def save_to_file(self, filename: str = None):
        try:
            if filename is None:
                filename = 'shapes_drawing.json'
            
            data = []
            for shape in self._shapes:
                data.append({
                    'type': shape.get_name(),
                    'coords': shape.get_coordinates()
                })
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Помилка збереження: {e}")
            return False
    
    def load_from_file(self, filename: str = None):
        try:
            if filename is None:
                filename = 'shapes_drawing.json'
            
            if not os.path.exists(filename):
                print("Файл не знайдено")
                return False
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._shapes.clear()
            for item in data:
                coords = item['coords']
                if item['type'] == 'Точка':
                    shape = Point(*coords)
                elif item['type'] == 'Лінія':
                    shape = Line(*coords)
                elif item['type'] == 'Еліпс':
                    shape = Ellipse(*coords)
                elif item['type'] == 'Прямокутник':
                    shape = Rectangle(*coords)
                else:
                    continue
                self._shapes.append(shape)
            
            self.notify_observers("shapes_loaded")
            return True
        except Exception as e:
            print(f"Помилка завантаження: {e}")
            return False