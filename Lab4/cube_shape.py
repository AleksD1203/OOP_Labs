from shape import LineShape, RectShape

class CubeShape(LineShape, RectShape):
    def __init__(self):
        LineShape.__init__(self)
        RectShape.__init__(self)
        self._depth_offset = 30
    
    def _draw_line(self, canvas, x1, y1, x2, y2):
        """Допоміжний метод для малювання лінії"""
        self.set(x1, y1, x2, y2)
        LineShape.show(self, canvas)
    
    def show(self, canvas):
        # Зберігаємо оригінальні координати
        x1, y1 = self._xs1, self._ys1
        x2, y2 = self._xs2, self._ys2
        
        # Обчислюємо розміри
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        # Нормалізуємо координати
        left = min(x1, x2)
        top = min(y1, y2)
        right = left + width
        bottom = top + height
        
        # 1. Малюємо передню грань (суцільна)
        self.set(left, top, right, bottom)
        canvas.create_rectangle(
            self._xs1, self._ys1, self._xs2, self._ys2,
            outline="black", fill="", width=2  # Прозоре заповнення
        )
        
        # 2. Малюємо задню грань (пунктирна - прозора)
        offset = self._depth_offset
        self.set(
            left + offset, top - offset,
            right + offset, bottom - offset
        )
        canvas.create_rectangle(
            self._xs1, self._ys1, self._xs2, self._ys2,
            outline="black", fill="", width=2, dash=(5, 3)  # Пунктир для прозорості
        )
        
        # 3. З'єднуємо передню та задню грані лініями
        # Видимі лінії - суцільні
        self._draw_line(canvas, left, top, left + offset, top - offset)
        self._draw_line(canvas, right, top, right + offset, top - offset)
        self._draw_line(canvas, left, bottom, left + offset, bottom - offset)
        self._draw_line(canvas, right, bottom, right + offset, bottom - offset)
        
        # Невидимі лінії - пунктирні (прозорі)
        canvas.create_line(
            left, top, left + offset, top - offset,
            fill="gray", width=1, dash=(5, 3)
        )
        canvas.create_line(
            right, bottom, right + offset, bottom - offset,
            fill="gray", width=1, dash=(5, 3)
        )
        
        # Відновлюємо оригінальні координати
        self.set(x1, y1, x2, y2)