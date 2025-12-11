from abc import ABC, abstractmethod
from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPolygon
import math

class Shape(ABC):
    """Базовий клас для фігур"""
    
    def __init__(self, start_point, end_point):
        self.start = QPoint(start_point)
        self.end = QPoint(end_point)
        # Налаштування стилю
        self.color = QColor(0, 0, 0)
        self.line_width = 2
        self.line_style = Qt.SolidLine
        self.fill_color = QColor(255, 255, 255, 0) # Прозорий
        self.fill_enabled = False
        
        # Стан фігури
        self.selected = False
        self.is_being_drawn = False
        
    @abstractmethod
    def draw(self, painter):
        pass
    
    @abstractmethod
    def get_type(self):
        pass
    
    def set_color(self, color):
        self.color = color
    
    def set_fill_color(self, color):
        self.fill_color = color
        self.fill_enabled = color.alpha() > 0
    
    def set_line_width(self, width):
        self.line_width = width

    def set_line_style(self, style):
        self.line_style = style
    
    def get_bounding_rect(self):
        return QRect(self.start, self.end).normalized()
    
    def contains(self, point):
        rect = self.get_bounding_rect()
        return rect.adjusted(-5, -5, 5, 5).contains(point)
    
    def is_in_selection_rect(self, selection_rect):
        return selection_rect.intersects(self.get_bounding_rect())
    
    def move(self, dx, dy):
        self.start.setX(self.start.x() + dx)
        self.start.setY(self.start.y() + dy)
        self.end.setX(self.end.x() + dx)
        self.end.setY(self.end.y() + dy)
    
    # Логіка зміни розміру
    def resize(self, handle_index, new_point):
        if not self.selected: return
            
        # Логіка для 8 точок (кути і сторони)
        if handle_index == 0:   self.start = new_point
        elif handle_index == 1: self.start.setY(new_point.y())
        elif handle_index == 2: 
            self.start.setY(new_point.y())
            self.end.setX(new_point.x())
        elif handle_index == 3: self.start.setX(new_point.x())
        elif handle_index == 4: self.end.setX(new_point.x())
        elif handle_index == 5:
            self.start.setX(new_point.x())
            self.end.setY(new_point.y())
        elif handle_index == 6: self.end.setY(new_point.y())
        elif handle_index == 7: self.end = new_point
    
    def get_resize_handles(self):
        if not self.selected: return []
        
        rect = self.get_bounding_rect()
        d = 8
        
        return [
            QRect(rect.left(), rect.top(), d, d),
            QRect(rect.center().x() - d//2, rect.top(), d, d),
            QRect(rect.right() - d, rect.top(), d, d),
            QRect(rect.left(), rect.center().y() - d//2, d, d),
            QRect(rect.right() - d, rect.center().y() - d//2, d, d),
            QRect(rect.left(), rect.bottom() - d, d, d),
            QRect(rect.center().x() - d//2, rect.bottom() - d, d, d),
            QRect(rect.right() - d, rect.bottom() - d, d, d)
        ]
    
    def get_resize_handle_at(self, point):
        if not self.selected: return -1
        
        handles = self.get_resize_handles()
        for i, handle in enumerate(handles):
            if handle.contains(point):
                return i
        return -1
    
    def to_dict(self):
        return {
            'type': self.get_type(),
            'start': {'x': self.start.x(), 'y': self.start.y()},
            'end': {'x': self.end.x(), 'y': self.end.y()},
            'color': self.color.rgba(),
            'fill_color': self.fill_color.rgba(),
            'line_width': self.line_width,
            'line_style': self.line_style
        }
    
    @staticmethod
    def from_dict(data):
        type_ = data['type']
        p1 = QPoint(data['start']['x'], data['start']['y'])
        p2 = QPoint(data['end']['x'], data['end']['y'])
        
        # Створюємо об'єкт потрібного класу
        obj = None
        if type_ == 'rectangle': obj = Rectangle(p1, p2)
        elif type_ == 'ellipse': obj = Ellipse(p1, p2)
        elif type_ == 'line':    obj = Line(p1, p2)
        elif type_ == 'triangle':obj = Triangle(p1, p2)
        elif type_ == 'arrow':   obj = Arrow(p1, p2)
        elif type_ == 'text':
            obj = TextShape(p1, p2)
            obj.text = data.get('text', 'Текст')
            obj.font_size = data.get('font_size', 20)
            obj.font_family = data.get('font_family', 'Arial')
            
        if obj:
            obj.color = QColor.fromRgba(data['color'])
            obj.fill_color = QColor.fromRgba(data['fill_color'])
            obj.line_width = data['line_width']
            obj.line_style = data.get('line_style', Qt.SolidLine)
            obj.fill_enabled = obj.fill_color.alpha() > 0
            
        return obj

class Rectangle(Shape):
    def draw(self, painter):
        painter.setPen(QPen(self.color, self.line_width, self.line_style))
        painter.setBrush(QBrush(self.fill_color) if self.fill_enabled else Qt.NoBrush)
        painter.drawRect(self.get_bounding_rect())
        
        if self.selected and not self.is_being_drawn:
            self.draw_handles(painter)
            
    def draw_handles(self, painter):
        painter.setPen(QPen(QColor(0, 120, 215), 1))
        painter.setBrush(QBrush(Qt.white))
        for r in self.get_resize_handles():
            painter.drawRect(r)
            
    def get_type(self): return 'rectangle'

class Ellipse(Shape):
    def draw(self, painter):
        painter.setPen(QPen(self.color, self.line_width, self.line_style))
        painter.setBrush(QBrush(self.fill_color) if self.fill_enabled else Qt.NoBrush)
        painter.drawEllipse(self.get_bounding_rect())
        
        if self.selected and not self.is_being_drawn:
            self.draw_handles(painter)
            
    def draw_handles(self, painter):
        painter.setPen(QPen(QColor(0, 120, 215), 1))
        painter.setBrush(QBrush(Qt.white))
        for r in self.get_resize_handles():
            painter.drawRect(r)

    def get_type(self): return 'ellipse'

class Line(Shape):
    def draw(self, painter):
        painter.setPen(QPen(self.color, self.line_width, self.line_style))
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(self.start, self.end)
        
        if self.selected and not self.is_being_drawn:
            self.draw_handles(painter)
            
    def draw_handles(self, painter):
        painter.setPen(QPen(QColor(0, 120, 215), 1))
        painter.setBrush(QBrush(Qt.white))
        handles = self.get_resize_handles()
        # Малюємо тільки кутові точки
        for i in [0, 2, 5, 7]:
            if i < len(handles): painter.drawRect(handles[i])

    def get_type(self): return 'line'

class Triangle(Shape):
    def __init__(self, start, end):
        super().__init__(start, end)
        self.calculate_third_point()
        
    def calculate_third_point(self):
        # Рахуємо координати трикутника (рівнобедрений)
        x1, y1 = self.start.x(), self.start.y()
        x2, y2 = self.end.x(), self.end.y()
        
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        if y1 < y2:
            self.a = QPoint(min_x, max_y)
            self.b = QPoint(max_x, max_y)
            self.c = QPoint(min_x + (max_x - min_x)//2, min_y)
        else:
            self.a = QPoint(min_x, min_y)
            self.b = QPoint(max_x, min_y)
            self.c = QPoint(min_x + (max_x - min_x)//2, max_y)
            
    def draw(self, painter):
        painter.setPen(QPen(self.color, self.line_width, self.line_style))
        painter.setBrush(QBrush(self.fill_color) if self.fill_enabled else Qt.NoBrush)
        painter.drawPolygon(QPolygon([self.a, self.b, self.c]))
        
        if self.selected and not self.is_being_drawn:
            self.draw_handles(painter)

    def draw_handles(self, painter):
        painter.setPen(QPen(QColor(0, 120, 215), 1))
        painter.setBrush(QBrush(Qt.white))
        d = 8
        for p in [self.a, self.b, self.c]:
            painter.drawRect(p.x() - d//2, p.y() - d//2, d, d)

    def get_type(self): return 'triangle'
    
    # Перевизначаємо для 3 точок
    def get_bounding_rect(self):
        xs = [self.a.x(), self.b.x(), self.c.x()]
        ys = [self.a.y(), self.b.y(), self.c.y()]
        return QRect(QPoint(min(xs), min(ys)), QPoint(max(xs), max(ys)))
        
    def move(self, dx, dy):
        super().move(dx, dy)
        self.a.setX(self.a.x() + dx); self.a.setY(self.a.y() + dy)
        self.b.setX(self.b.x() + dx); self.b.setY(self.b.y() + dy)
        self.c.setX(self.c.x() + dx); self.c.setY(self.c.y() + dy)
        
    def resize(self, idx, pt):
        if not self.selected: return
        if idx == 0: self.a = pt
        elif idx == 1: self.b = pt
        elif idx == 2: self.c = pt
        
    def get_resize_handles(self):
        if not self.selected: return []
        d = 8
        return [QRect(p.x() - d//2, p.y() - d//2, d, d) for p in [self.a, self.b, self.c]]
        
    def to_dict(self):
        d = super().to_dict()
        d.update({
            'point_a': {'x': self.a.x(), 'y': self.a.y()},
            'point_b': {'x': self.b.x(), 'y': self.b.y()},
            'point_c': {'x': self.c.x(), 'y': self.c.y()}
        })
        return d
        
    @staticmethod
    def from_dict(data):
        t = Triangle(QPoint(data['start']['x'], data['start']['y']),
                    QPoint(data['end']['x'], data['end']['y']))
        if 'point_a' in data:
            t.a = QPoint(data['point_a']['x'], data['point_a']['y'])
            t.b = QPoint(data['point_b']['x'], data['point_b']['y'])
            t.c = QPoint(data['point_c']['x'], data['point_c']['y'])
        
        t.color = QColor.fromRgba(data['color'])
        t.fill_color = QColor.fromRgba(data['fill_color'])
        t.line_width = data['line_width']
        t.line_style = data.get('line_style', Qt.SolidLine)
        t.fill_enabled = t.fill_color.alpha() > 0
        return t

class Arrow(Shape):
    def draw(self, painter):
        painter.setPen(QPen(self.color, self.line_width, self.line_style))
        painter.setBrush(QBrush(self.fill_color) if self.fill_enabled else Qt.NoBrush)
        painter.drawLine(self.start, self.end)
        
        # Малюємо стрілочку
        dx = self.end.x() - self.start.x()
        dy = self.end.y() - self.start.y()
        angle = math.atan2(dy, dx)
        size = 15
        
        p1 = QPoint(int(self.end.x() - size * math.cos(angle - math.pi/6)),
                   int(self.end.y() - size * math.sin(angle - math.pi/6)))
        p2 = QPoint(int(self.end.x() - size * math.cos(angle + math.pi/6)),
                   int(self.end.y() - size * math.sin(angle + math.pi/6)))
                   
        painter.setPen(QPen(self.color, self.line_width, Qt.SolidLine)) # Стрілка завжди суцільна
        painter.setBrush(QBrush(self.fill_color) if self.fill_color.alpha() > 0 else QBrush(self.color))
        painter.drawPolygon(QPolygon([self.end, p1, p2]))
        
        if self.selected and not self.is_being_drawn:
            self.draw_handles(painter)
            
    def draw_handles(self, painter):
        painter.setPen(QPen(QColor(0, 120, 215), 1))
        painter.setBrush(QBrush(Qt.white))
        for r in self.get_resize_handles():
            painter.drawRect(r)
            
    def get_type(self): return 'arrow'

class TextShape(Shape):
    def __init__(self, start, end):
        super().__init__(start, end)
        self.text = "Текст"
        self.font_size = 20
        self.font_family = "Arial"
        self.fill_enabled = True
        self.is_editing = False
        self.old_text = ""
        
    def draw(self, painter):
        if self.fill_color.alpha() > 0:
            painter.setBrush(QBrush(self.fill_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.get_bounding_rect())
            
        painter.setPen(QPen(self.color, 1))
        painter.setFont(QFont(self.font_family, self.font_size))
        painter.drawText(self.get_bounding_rect(), Qt.AlignCenter | Qt.TextWordWrap, self.text)
        
        if self.selected and not self.is_being_drawn:
            self.draw_handles(painter)
            
    def draw_handles(self, painter):
        painter.setPen(QPen(QColor(0, 120, 215), 1))
        painter.setBrush(QBrush(Qt.white))
        for r in self.get_resize_handles():
            painter.drawRect(r)
            
    def get_type(self): return 'text'
    
    def set_font_size(self, size):
        self.font_size = max(8, min(72, size))
        
    def set_font_family(self, font):
        self.font_family = font
        
    def start_editing(self):
        self.is_editing = True
        self.old_text = self.text
        
    def finish_editing(self, text=None):
        self.is_editing = False
        if text is not None: self.text = text
        
    def cancel_editing(self):
        self.is_editing = False
        self.text = self.old_text
        
    def to_dict(self):
        d = super().to_dict()
        d.update({'text': self.text, 'font_size': self.font_size, 'font_family': self.font_family})
        return d