from PyQt5.QtWidgets import QToolBar, QAction, QColorDialog, QSpinBox, QLabel, QPushButton, QComboBox, QMenu
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QIcon, QColor, QPixmap, QPainter, QPen, QBrush, QPolygon, QFont

# --- Базовий клас для кольорових кнопок ---
class ColorButtonBase(QPushButton):
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(34, 34) 
        self.setText("")
        self.clicked.connect(self.show_menu)
        
    def show_menu(self):
        menu = QMenu(self)
        self.populate_menu(menu)
        menu.exec_(self.mapToGlobal(self.rect().bottomLeft()))
        
    def populate_menu(self, menu):
        # Набір базових кольорів
        colors = [
            ("Чорний", QColor(0,0,0)), ("Білий", QColor(255,255,255)),
            ("Сірий", QColor(128,128,128)), ("Червоний", QColor(255,0,0)), 
            ("Зелений", QColor(0,180,0)), ("Синій", QColor(0,0,255)), 
            ("Жовтий", QColor(255,200,0)), ("Помаранчевий", QColor(255,100,0))
        ]
        
        for name, col in colors:
            action = QAction(name, self)
            pix = QPixmap(16, 16)
            pix.fill(col)
            action.setIcon(QIcon(pix))
            action.triggered.connect(lambda ch, c=col: self.set_color(c))
            menu.addAction(action)
            
        menu.addSeparator()
        action = QAction("Інший колір...", self)
        action.triggered.connect(self.open_dialog)
        menu.addAction(action)

    def set_color(self, color):
        self.color = color
        self.update_icon()
        self.colorChanged.emit(color)
        
    def open_dialog(self):
        col = QColorDialog.getColor(self.color, self)
        if col.isValid(): self.set_color(col)

# --- Кнопка заливки ---
class FillColorButton(ColorButtonBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(255, 255, 255, 0) # Прозорий старт
        self.update_icon()
        
    def populate_menu(self, menu):
        act = QAction("Без заливки", self)
        # Іконка хрестика для меню
        pix = QPixmap(16, 16)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(Qt.red, 2))
        p.drawLine(2, 2, 14, 14)
        p.drawLine(14, 2, 2, 14)
        p.end()
        act.setIcon(QIcon(pix))
        
        act.triggered.connect(lambda: self.set_color(QColor(255,255,255,0)))
        menu.addAction(act)
        menu.addSeparator()
        super().populate_menu(menu)
        
    def update_icon(self):
        pix = QPixmap(24, 24)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        
        if self.color.alpha() == 0:
            # Хрестик "без заливки"
            p.setPen(QPen(Qt.gray, 1))
            p.setBrush(Qt.white)
            p.drawRect(2, 2, 20, 20)
            
            p.setPen(QPen(Qt.red, 2))
            p.drawLine(6, 6, 18, 18)
            p.drawLine(18, 6, 6, 18)
        else:
            p.setPen(QPen(Qt.black, 1))
            p.setBrush(self.color)
            p.drawRect(2, 2, 20, 20)
            
        p.end()
        self.setIcon(QIcon(pix))

class OutlineColorButton(ColorButtonBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(0, 0, 0)
        self.update_icon()
        
    def update_icon(self):
        pix = QPixmap(24, 24)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        
        p.setPen(QPen(self.color, 3))
        p.setBrush(Qt.NoBrush)
        p.drawRect(4, 4, 16, 16)
        
        p.end()
        self.setIcon(QIcon(pix))
        
class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Інструменти", parent)
        self.setIconSize(QSize(28, 28))
        self.setMovable(False)
        self.init_ui()
        
    def init_ui(self):
        # Інструменти
        self.add_drawn_btn("select", "Виділення", self.draw_cursor_icon)
        self.addSeparator()
        
        self.add_drawn_btn("rectangle", "Прямокутник", self.draw_rect_icon)
        self.add_drawn_btn("ellipse", "Еліпс", self.draw_ellipse_icon)
        self.add_drawn_btn("line", "Лінія", self.draw_line_icon)
        self.add_drawn_btn("triangle", "Трикутник", self.draw_triangle_icon)
        self.add_drawn_btn("arrow", "Стрілка", self.draw_arrow_icon)
        self.add_drawn_btn("text", "Текст", self.draw_text_icon)
        
        self.addSeparator()
        
        # Кольори
        self.addWidget(QLabel(" Контур: "))
        self.outline_btn = OutlineColorButton(self)
        self.outline_btn.colorChanged.connect(lambda c: self.parent().set_current_color(c))
        self.addWidget(self.outline_btn)
        
        self.addWidget(QLabel("  Заливка: "))
        self.fill_btn = FillColorButton(self)
        self.fill_btn.colorChanged.connect(lambda c: self.parent().set_fill_color(c))
        self.addWidget(self.fill_btn)
        
        self.addSeparator()
        
        # Товщина
        self.addWidget(QLabel(" Товщина: "))
        sb = QSpinBox(self)
        sb.setRange(1, 20)
        sb.setValue(2)
        sb.setFixedWidth(50)
        sb.valueChanged.connect(lambda w: self.parent().set_line_width(w))
        self.addWidget(sb)
        
        # Стиль
        self.addWidget(QLabel(" "))
        cb = QComboBox(self)
        cb.setFixedWidth(80)
        cb.addItem("Суцільна", Qt.SolidLine)
        cb.addItem("Пунктир", Qt.DashLine)
        cb.addItem("Точки", Qt.DotLine)
        cb.addItem("Штрих-пункт.", Qt.DashDotLine)
        cb.currentIndexChanged.connect(lambda idx: self.parent().set_line_style(cb.itemData(idx)))
        self.addWidget(cb)
        
        self.addSeparator()
        
        # Шрифт
        font_sb = QSpinBox(self)
        font_sb.setRange(8, 72)
        font_sb.setValue(20)
        font_sb.setFixedWidth(50)
        font_sb.setToolTip("Розмір шрифту")
        font_sb.valueChanged.connect(lambda s: self.parent().set_font_size(s))
        self.addWidget(font_sb)
        
        font_cb = QComboBox(self)
        font_cb.setFixedWidth(80)
        font_cb.addItems(["Arial", "Times New Roman", "Verdana", "Courier New"])
        font_cb.currentTextChanged.connect(lambda f: self.parent().set_font_family(f))
        self.addWidget(font_cb)
        
        self.addSeparator()
        
        # Очищення
        trash_act = QAction("Очистити", self)
        trash_act.setToolTip("Очистити все")
        
        pix_trash = QPixmap(32, 32)
        pix_trash.fill(Qt.transparent)
        pt = QPainter(pix_trash)
        pt.setRenderHint(QPainter.Antialiasing)
        self.draw_trash_icon(pt)
        pt.end()
        
        trash_act.setIcon(QIcon(pix_trash))
        trash_act.triggered.connect(lambda: self.parent().clear_scene())
        self.addAction(trash_act)

    def add_drawn_btn(self, tool_id, name, draw_func):
        pix = QPixmap(32, 32)
        pix.fill(Qt.transparent)
        
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)
        draw_func(painter)
        painter.end()
        
        act = QAction(QIcon(pix), name, self)
        act.triggered.connect(lambda: self.parent().set_current_tool(tool_id))
        self.addAction(act)

    def draw_cursor_icon(self, p):
        p.setPen(QPen(Qt.black, 1))
        p.setBrush(Qt.white)
        poly = QPolygon([
            QPoint(10, 6), QPoint(22, 18), QPoint(16, 18), 
            QPoint(19, 24), QPoint(16, 25), QPoint(13, 19), QPoint(10, 22)
        ])
        p.drawPolygon(poly)

    def draw_rect_icon(self, p):
        p.setPen(QPen(Qt.black, 2))
        p.setBrush(QBrush(QColor(200, 230, 255)))
        p.drawRect(6, 8, 20, 16)

    def draw_ellipse_icon(self, p):
        p.setPen(QPen(Qt.black, 2))
        p.setBrush(QBrush(QColor(255, 230, 200)))
        p.drawEllipse(6, 6, 20, 20)

    def draw_line_icon(self, p):
        # Просто рівна лінія
        p.setPen(QPen(Qt.black, 3))
        p.drawLine(6, 26, 26, 6)

    def draw_triangle_icon(self, p):
        p.setPen(QPen(Qt.black, 2))
        p.setBrush(QBrush(QColor(200, 255, 200)))
        poly = QPolygon([QPoint(16, 6), QPoint(26, 26), QPoint(6, 26)])
        p.drawPolygon(poly)

    def draw_arrow_icon(self, p):
        p.setPen(QPen(Qt.black, 2))
        p.setBrush(Qt.black)
        p.drawLine(4, 16, 22, 16)
        poly = QPolygon([QPoint(22, 12), QPoint(28, 16), QPoint(22, 20)])
        p.drawPolygon(poly)

    def draw_text_icon(self, p):
        p.setPen(Qt.black)
        font = QFont("Times New Roman", 22, QFont.Bold)
        p.setFont(font)
        p.drawText(QRect(0, 0, 32, 32), Qt.AlignCenter, "T")

    def draw_trash_icon(self, p):
        p.setPen(QPen(QColor(200, 0, 0), 2))
        p.setBrush(Qt.NoBrush)
        bucket = QPolygon([QPoint(8, 10), QPoint(24, 10), QPoint(22, 28), QPoint(10, 28)])
        p.drawPolygon(bucket)
        p.drawLine(6, 10, 26, 10)
        p.drawLine(12, 10, 12, 7)
        p.drawLine(20, 10, 20, 7)
        p.drawLine(12, 7, 20, 7)
        p.setPen(QPen(QColor(200, 0, 0), 1))
        p.drawLine(13, 14, 14, 24)
        p.drawLine(19, 14, 18, 24)