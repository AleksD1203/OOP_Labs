from PyQt5.QtWidgets import QWidget, QScrollArea, QInputDialog
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QCursor
from shapes import Rectangle, Ellipse, Line, Triangle, Arrow, TextShape

class Canvas(QWidget):
    """Полотно для малювання"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shapes = [] # Всі фігури тут
        self.current_shape = None
        
        # Статуси
        self.drawing = False
        self.selecting = False
        self.resizing = False
        self.dragging = False
        
        # Інструменти
        self.current_tool = 'select'
        self.selected_shapes = [] 
        self.selection_rect = QRect()
        
        # Для перетягування
        self.start_point = QPoint()
        self.drag_start = QPoint()
        self.resize_handle = -1
        self.resize_shape = None
        
        # Сітка (виправлено помилку з grid_enabled)
        self.grid_enabled = True
        self.grid_size = 20
        self.grid_color = QColor(220, 220, 220)
        self.background_color = QColor(240, 240, 240)
        
        # Редагування тексту
        self.editing_text = None
        
        # Налаштування стилю (поточні)
        self.current_color = QColor(0, 0, 0)
        self.fill_color = QColor(255, 255, 255, 0)
        self.line_width = 2
        self.current_line_style = Qt.SolidLine
        self.font_size = 20
        self.font_family = "Arial"
        
        # Розміри полотна
        self.scene_w = 2000
        self.scene_h = 2000
        self.setMinimumSize(self.scene_w, self.scene_h)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.background_color)
        
        # Малюємо сітку
        if self.grid_enabled:
            painter.setPen(self.grid_color)
            for x in range(0, self.scene_w, self.grid_size):
                painter.drawLine(x, 0, x, self.scene_h)
            for y in range(0, self.scene_h, self.grid_size):
                painter.drawLine(0, y, self.scene_w, y)
        
        # Малюємо фігури
        for s in self.shapes:
            if not s.selected: s.draw(painter)
            
        # Малюємо виділені поверх інших
        for s in self.selected_shapes:
            s.draw(painter)
            
        # Малюємо те, що зараз створюємо
        if self.current_shape:
            self.current_shape.draw(painter)
            
        # Рамка виділення
        if self.selecting and not self.selection_rect.isNull():
            painter.setPen(QPen(QColor(0, 120, 215), 1, Qt.DashLine))
            painter.setBrush(QBrush(QColor(0, 120, 215, 30)))
            painter.drawRect(self.selection_rect)

    def mousePressEvent(self, event):
        if self.editing_text:
            self.finish_text_editing()
            return

        pos = event.pos()
        self.start_point = pos
        
        clicked_shape = None
        for s in reversed(self.shapes):
            if s.contains(pos):
                clicked_shape = s
                break
        
        # Правий клік - редагування тексту
        if event.button() == Qt.RightButton:
            if isinstance(clicked_shape, TextShape) and self.current_tool == 'select':
                self.start_text_editing(clicked_shape)
                return

        if event.button() == Qt.LeftButton:
            if self.current_tool == 'select':
                # Перевіряємо ручки зміни розміру
                for s in self.selected_shapes:
                    idx = s.get_resize_handle_at(pos)
                    if idx != -1:
                        self.resizing = True
                        self.resize_handle = idx
                        self.resize_shape = s
                        return # Виходимо, бо ми змінюємо розмір

                # Логіка виділення
                ctrl = event.modifiers() & Qt.ControlModifier
                
                if clicked_shape:
                    if ctrl:
                        # Додаємо або прибираємо з виділення
                        if clicked_shape in self.selected_shapes:
                            self.deselect(clicked_shape)
                        else:
                            self.select(clicked_shape)
                    else:
                        # Якщо клікнули на нову фігуру без Ctrl
                        if clicked_shape not in self.selected_shapes:
                            self.clear_selection()
                            self.select(clicked_shape)
                    
                    self.dragging = True
                    self.drag_start = pos
                else:
                    # Клікнули в порожнє місце - початок виділення рамкою
                    if not ctrl: self.clear_selection()
                    self.selecting = True
                    self.selection_rect = QRect(pos, pos)
            else:
                # Малювання нової фігури
                self.drawing = True
                self.create_shape(pos)
        
        self.update()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        
        # Зміна курсора
        if self.current_tool == 'select' and not self.drawing:
            self.update_cursor(pos)
            
        if self.resizing and self.resize_shape:
            self.resize_shape.resize(self.resize_handle, pos)
            self.update()
        elif self.dragging and self.selected_shapes:
            dx = pos.x() - self.drag_start.x()
            dy = pos.y() - self.drag_start.y()
            for s in self.selected_shapes:
                s.move(dx, dy)
            self.drag_start = pos
            self.update()
        elif self.selecting:
            self.selection_rect = QRect(self.start_point, pos).normalized()
            self.update()
        elif self.drawing and self.current_shape:
            self.current_shape.end = pos
            # Оновлюємо трикутник
            if isinstance(self.current_shape, Triangle):
                self.current_shape.calculate_third_point()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.selecting:
                # Виділяємо все, що потрапило в рамку
                for s in self.shapes:
                    if s.is_in_selection_rect(self.selection_rect):
                        self.select(s)
                self.selecting = False
                self.selection_rect = QRect()
            
            elif self.drawing and self.current_shape:
                if self.current_tool == 'text':
                    text, ok = QInputDialog.getText(self, "Текст", "Введіть текст:", 
                                                  text=self.current_shape.text)
                    if ok and text:
                        self.current_shape.text = text
                        self.add_shape(self.current_shape)
                else:
                    self.add_shape(self.current_shape)
                
                self.current_shape = None
                self.drawing = False
            
            self.dragging = False
            self.resizing = False
            self.resize_shape = None
            self.update()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.current_tool == 'select':
             for s in reversed(self.shapes):
                if isinstance(s, TextShape) and s.contains(event.pos()):
                    self.start_text_editing(s)
                    break

    def create_shape(self, pos):
        tool = self.current_tool
        if tool == 'rectangle': s = Rectangle(pos, pos)
        elif tool == 'ellipse': s = Ellipse(pos, pos)
        elif tool == 'line':    s = Line(pos, pos)
        elif tool == 'triangle':s = Triangle(pos, pos)
        elif tool == 'arrow':   s = Arrow(pos, pos)
        elif tool == 'text':    s = TextShape(pos, QPoint(pos.x()+200, pos.y()+100))
        else: return
        
        # Застосовуємо стилі
        s.set_color(self.current_color)
        s.set_fill_color(self.fill_color)
        s.set_line_width(self.line_width)
        s.set_line_style(self.current_line_style)
        if tool == 'text':
            s.set_font_size(self.font_size)
            s.set_font_family(self.font_family)
            
        s.is_being_drawn = True
        self.current_shape = s

    def add_shape(self, shape):
        shape.is_being_drawn = False
        self.shapes.append(shape)
        self.clear_selection()
        self.select(shape)

    def select(self, shape):
        if shape not in self.selected_shapes:
            shape.selected = True
            self.selected_shapes.append(shape)

    def deselect(self, shape):
        if shape in self.selected_shapes:
            shape.selected = False
            self.selected_shapes.remove(shape)

    def clear_selection(self):
        for s in self.selected_shapes:
            s.selected = False
        self.selected_shapes.clear()

    def start_text_editing(self, shape):
        if self.editing_text: self.finish_text_editing()
        
        self.clear_selection()
        self.select(shape)
        self.editing_text = shape
        shape.start_editing()
        
        text, ok = QInputDialog.getText(self, "Редагування", "Текст:", text=shape.text)
        if ok: shape.finish_editing(text)
        else: shape.cancel_editing()
        
        self.editing_text = None
        self.update()

    def finish_text_editing(self):
        if self.editing_text:
            self.editing_text.cancel_editing()
            self.editing_text = None

    def update_cursor(self, pos):
        # Курсор для зміни розміру
        cursor = Qt.ArrowCursor
        for s in self.selected_shapes:
            idx = s.get_resize_handle_at(pos)
            if idx != -1:
                if isinstance(s, Triangle): cursor = Qt.SizeAllCursor
                elif idx in [0, 7]: cursor = Qt.SizeFDiagCursor
                elif idx in [1, 6]: cursor = Qt.SizeVerCursor
                elif idx in [2, 5]: cursor = Qt.SizeBDiagCursor
                elif idx in [3, 4]: cursor = Qt.SizeHorCursor
                break
        self.setCursor(cursor)
    
    def set_tool(self, t): 
        self.current_tool = t
        self.clear_selection()
    def set_current_color(self, c):
        self.current_color = c
        self._update_selected_props(lambda s: s.set_color(c))
    def set_fill_color(self, c):
        self.fill_color = c
        self._update_selected_props(lambda s: s.set_fill_color(c))
    def set_line_width(self, w):
        self.line_width = w
        self._update_selected_props(lambda s: s.set_line_width(w))
    def set_line_style(self, s):
        self.current_line_style = s
        self._update_selected_props(lambda sh: sh.set_line_style(s))
    def set_font_size(self, s):
        self.font_size = s
        self._update_selected_props(lambda sh: sh.set_font_size(s) if isinstance(sh, TextShape) else None)
    def set_font_family(self, f):
        self.font_family = f
        self._update_selected_props(lambda sh: sh.set_font_family(f) if isinstance(sh, TextShape) else None)
        
    def _update_selected_props(self, func):
        if self.current_shape: func(self.current_shape)
        for s in self.selected_shapes: func(s)
        self.update()
        
    def clear_scene(self):
        self.shapes.clear()
        self.clear_selection()
        self.update()
        
    def delete_selected(self):
        for s in self.selected_shapes:
            if s in self.shapes: self.shapes.remove(s)
        self.clear_selection()
        self.update()
        
    def get_shapes(self): return self.shapes
    def set_shapes(self, s): 
        self.shapes = s
        self.update()

class Viewer(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = Canvas(self)
        self.setWidget(self.canvas)
        self.setWidgetResizable(True)
    
    def get_canvas(self): 
        return self.canvas