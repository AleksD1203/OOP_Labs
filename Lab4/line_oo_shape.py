from shape import LineShape, EllipseShape

class LineOOShape(LineShape, EllipseShape):
    def __init__(self):
        LineShape.__init__(self)
        EllipseShape.__init__(self)
        self._circle_radius = 8
    
    def show(self, canvas):
        # 1. Малюємо центральну лінію
        LineShape.show(self, canvas)
        
        # 2. Малюємо кружечок на початку лінії
        temp_xs1, temp_ys1 = self._xs1, self._ys1
        temp_xs2, temp_ys2 = self._xs2, self._ys2
        
        # Встановлюємо координати для першого кружечка
        self.set(
            self._xs1 - self._circle_radius,
            self._ys1 - self._circle_radius,
            self._xs1 + self._circle_radius,
            self._ys1 + self._circle_radius
        )
        # Малюємо ПРОЗОРИЙ кружечок
        canvas.create_oval(
            self._xs1, self._ys1, self._xs2, self._ys2,
            outline="black", fill="", width=2  # Прозоре заповнення
        )
        
        # 3. Малюємо кружечок в кінці лінії
        self.set(
            temp_xs2 - self._circle_radius,
            temp_ys2 - self._circle_radius,
            temp_xs2 + self._circle_radius,
            temp_ys2 + self._circle_radius
        )
        canvas.create_oval(
            self._xs1, self._ys1, self._xs2, self._ys2,
            outline="black", fill="", width=2  # Прозоре заповнення
        )
        
        # Відновлюємо оригінальні координати
        self.set(temp_xs1, temp_ys1, temp_xs2, temp_ys2)