from abc import ABC, abstractmethod


class Shape(ABC):
    """Базовий абстрактний клас для всіх геометричних фігур"""
    
    def __init__(self):
        self._xs1 = 0
        self._ys1 = 0
        self._xs2 = 0
        self._ys2 = 0
    
    def set(self, x1, y1, x2, y2):
        """Встановлення координат фігури"""
        self._xs1 = x1
        self._ys1 = y1
        self._xs2 = x2
        self._ys2 = y2
    
    @abstractmethod
    def show(self, canvas):
        """Віртуальний метод відображення фігури"""
        pass


class PointShape(Shape):
    """Похідний клас для точкових об'єктів"""
    
    def show(self, canvas):
        """Реалізація методу відображення точки"""
        canvas.create_oval(
            self._xs1 - 2, self._ys1 - 2, 
            self._xs1 + 2, self._ys1 + 2, 
            fill="black", outline="black"
        )


class LineShape(Shape):
    """Похідний клас для лінійних об'єктів"""
    
    def show(self, canvas):
        """Реалізація методу відображення лінії"""
        canvas.create_line(
            self._xs1, self._ys1, 
            self._xs2, self._ys2, 
            fill="black", width=1
        )


class RectShape(Shape):
    """Похідний клас для прямокутників"""
    
    def show(self, canvas):
        """Реалізація методу відображення прямокутника"""
        canvas.create_rectangle(
            self._xs1, self._ys1, 
            self._xs2, self._ys2, 
            outline="black", fill="", width=1
        )


class EllipseShape(Shape):
    """Похідний клас для еліпсів"""
    
    def show(self, canvas):
        """Реалізація методу відображення еліпса"""
        canvas.create_oval(
            self._xs1, self._ys1, 
            self._xs2, self._ys2, 
            outline="black", fill="#FF8000", width=1
        )
