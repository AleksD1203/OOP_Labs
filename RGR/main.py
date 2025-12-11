import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

# Точка входу в програму
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Векторний графічний редактор")
    
    # Створюємо і показуємо головне вікно
    window = MainWindow()
    window.resize(1200, 800)
    window.show()
    
    sys.exit(app.exec_())