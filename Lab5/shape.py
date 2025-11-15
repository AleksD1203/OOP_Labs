import tkinter as tk
from abc import ABC, abstractmethod
from typing import Tuple

class Shape(ABC):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.selected = False
    
    @abstractmethod
    def draw(self, canvas: tk.Canvas):
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    def get_coordinates(self) -> Tuple[int, int, int, int]:
        return (self.x1, self.y1, self.x2, self.y2)
    
    def set_selected(self, selected: bool):
        self.selected = selected

class Point(Shape):
    def draw(self, canvas: tk.Canvas):
        color = "red" if self.selected else "black"
        canvas.create_oval(self.x1-3, self.y1-3, self.x1+3, self.y1+3, 
                          fill=color, outline=color, width=2)
    
    def get_name(self) -> str:
        return "Точка"

class Line(Shape):
    def draw(self, canvas: tk.Canvas):
        color = "red" if self.selected else "blue"
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, 
                          fill=color, width=3)
    
    def get_name(self) -> str:
        return "Лінія"

class Ellipse(Shape):
    def draw(self, canvas: tk.Canvas):
        color = "red" if self.selected else "green"
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, 
                          outline=color, width=3)
    
    def get_name(self) -> str:
        return "Еліпс"

class Rectangle(Shape):
    def draw(self, canvas: tk.Canvas):
        color = "red" if self.selected else "orange"
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, 
                               outline=color, width=3)
    
    def get_name(self) -> str:
        return "Прямокутник"