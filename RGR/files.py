import json
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from shapes import Shape

class FileManager:
    @staticmethod
    def save(shapes, filename, parent):
        if not filename:
            filename, _ = QFileDialog.getSaveFileName(parent, "Зберегти", "", "JSON (*.json)")
        
        if filename:
            try:
                if not filename.endswith('.json'): filename += '.json'
                
                data = {
                    'shapes': [s.to_dict() for s in shapes],
                    'version': '1.0'
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                return True, filename
            except Exception as e:
                QMessageBox.critical(parent, "Помилка", str(e))
        return False, None

    @staticmethod
    def load(parent):
        filename, _ = QFileDialog.getOpenFileName(parent, "Відкрити", "", "JSON (*.json)")
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                shapes = []
                for item in data['shapes']:
                    s = Shape.from_dict(item)
                    if s: shapes.append(s)
                    
                return shapes, filename
            except Exception as e:
                QMessageBox.critical(parent, "Помилка", str(e))
        return None, None