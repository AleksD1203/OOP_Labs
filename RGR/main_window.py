from PyQt5.QtWidgets import QMainWindow, QAction, QStatusBar, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from viewer import Viewer
from toolbar import Toolbar
from files import FileManager
from shapes import TextShape

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filename = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Векторний графічний редактор")
        self.resize(1000, 700) # Оптимальний розмір при запуску
        
        # Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        
        self.add_action(file_menu, "Новий", self.new_file, "Ctrl+N")
        self.add_action(file_menu, "Відкрити...", self.open_file, "Ctrl+O")
        self.add_action(file_menu, "Зберегти", self.save_file, "Ctrl+S")
        self.add_action(file_menu, "Зберегти як...", self.save_as)
        file_menu.addSeparator()
        self.add_action(file_menu, "Вихід", self.close)
        
        edit_menu = menubar.addMenu("Редагування")
        self.add_action(edit_menu, "Очистити сцену", self.clear_scene)
        self.add_action(edit_menu, "Видалити об'єкт", self.delete_obj, "Delete")
        self.add_action(edit_menu, "Редагувати текст", self.edit_text, "F2")
        
        view_menu = menubar.addMenu("Вид")
        self.add_action(view_menu, "Сітка вкл/викл", self.toggle_grid, "Ctrl+G")
        
        help_menu = menubar.addMenu("Довідка")
        self.add_action(help_menu, "Про програму", self.about)
        
        # Тулбар
        self.toolbar = Toolbar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        
        # Вювер
        self.viewer = Viewer(self)
        self.setCentralWidget(self.viewer)
        
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Готово. Оберіть інструмент для малювання.")

    def add_action(self, menu, name, func, shortcut=None):
        act = QAction(name, self)
        act.triggered.connect(func)
        if shortcut: act.setShortcut(shortcut)
        menu.addAction(act)
    
    def set_current_tool(self, tool):
        self.viewer.canvas.set_tool(tool)
        names = {
            'select': 'Виділення', 'rectangle': 'Прямокутник', 'ellipse': 'Еліпс',
            'line': 'Лінія', 'triangle': 'Трикутник', 'arrow': 'Стрілка', 'text': 'Текст'
        }
        name = names.get(tool, tool)
        self.statusbar.showMessage(f"Обрано інструмент: {name}")
        
    def set_current_color(self, c): self.viewer.canvas.set_current_color(c)
    def set_fill_color(self, c): self.viewer.canvas.set_fill_color(c)
    def set_line_width(self, w): self.viewer.canvas.set_line_width(w)
    def set_line_style(self, s): self.viewer.canvas.set_line_style(s)
    def set_font_size(self, s): self.viewer.canvas.set_font_size(s)
    def set_font_family(self, f): self.viewer.canvas.set_font_family(f)
    
    def clear_scene(self):
        if QMessageBox.question(self, "Очищення", "Ви впевнені, що хочете видалити всі об'єкти?") == QMessageBox.Yes:
            self.viewer.canvas.clear_scene()
            self.statusbar.showMessage("Сцену очищено")
            
    def delete_obj(self):
        if self.viewer.canvas.selected_shapes:
            self.viewer.canvas.delete_selected()
            self.statusbar.showMessage("Об'єкти видалено")
        
    def toggle_grid(self):
        c = self.viewer.canvas
        c.grid_enabled = not c.grid_enabled
        c.update()
        state = "увімкнено" if c.grid_enabled else "вимкнено"
        self.statusbar.showMessage(f"Сітку {state}")
        
    def edit_text(self):
        found = False
        for s in self.viewer.canvas.selected_shapes:
            if isinstance(s, TextShape):
                self.viewer.canvas.start_text_editing(s)
                found = True
                break
        if not found:
            self.statusbar.showMessage("Виділіть текстовий об'єкт для редагування")
    
    def new_file(self):
        if QMessageBox.question(self, "Новий файл", "Створити новий файл? Незбережені дані будуть втрачені.") == QMessageBox.Yes:
            self.viewer.canvas.clear_scene()
            self.filename = None
            self.setWindowTitle("Векторний графічний редактор")
            self.statusbar.showMessage("Створено новий файл")

    def open_file(self):
        shapes, fname = FileManager.load(self)
        if shapes is not None:
            self.viewer.canvas.set_shapes(shapes)
            self.filename = fname
            self.setWindowTitle(f"Векторний графічний редактор - {fname}")
            self.statusbar.showMessage(f"Завантажено файл: {fname}")

    def save_file(self):
        shapes = self.viewer.canvas.get_shapes()
        ok, fname = FileManager.save(shapes, self.filename, self)
        if ok:
            self.filename = fname
            self.setWindowTitle(f"Векторний графічний редактор - {fname}")
            self.statusbar.showMessage("Файл збережено успішно")
            
    def save_as(self):
        shapes = self.viewer.canvas.get_shapes()
        ok, fname = FileManager.save(shapes, None, self)
        if ok:
            self.filename = fname
            self.setWindowTitle(f"Векторний графічний редактор - {fname}")
            self.statusbar.showMessage("Файл збережено успішно")

    def about(self):
        # Oпис програми
        text = """
        <h3>Векторний Графічний Редактор</h3>
        <p>Програмний засіб для створення та редагування векторних зображень.</p>
        
        <p><b>Функціональні можливості:</b></p>
        <ul>
            <li>Створення примітивів: лінії, прямокутники, еліпси, трикутники, стрілки.</li>
            <li>Робота з текстовими об'єктами.</li>
            <li>Налаштування стилів: колір контуру та заливки, товщина та тип ліній.</li>
            <li>Маніпуляції з об'єктами: виділення, переміщення, масштабування.</li>
            <li>Збереження та завантаження проектів у форматі JSON.</li>
        </ul>
        
        <p><b>Керування:</b></p>
        <ul>
            <li><b>ЛКМ</b> - Малювання / Виділення</li>
            <li><b>Ctrl + ЛКМ</b> - Множинне виділення</li>
            <li><b>ПКМ (на тексті)</b> - Швидке редагування тексту</li>
            <li><b>F2</b> - Редагування тексту</li>
            <li><b>Delete</b> - Видалення виділеного</li>
        </ul>
        """
        QMessageBox.about(self, "Про програму", text)