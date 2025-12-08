import tkinter as tk
import math 
import os

class GraphPlotter:
    """Клас для побудови графіка на Tkinter Canvas."""
    
    CLIPBOARD_FILENAME = "clipboard.txt"
    
    def __init__(self, points):
        # Точки, відсортовані Object2 за X (для коректного малювання лінії)
        self.points = points 
        self.window = None
        self.canvas = None
        
        self.create_window()
        # Затримка для коректного отримання розмірів Canvas
        self.window.after(300, self.plot_graph) 
        self.window.mainloop()
    
    # --- Налаштування UI та Обмежень ---
    
    def create_window(self):
        """Створення головного вікна та Canvas."""
        self.window = tk.Tk()
        self.window.title("Object3 - Графік y=f(x)")
        
        # Розміщуємо Object3 праворуч від Object2
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        w = 1000
        h = 700
        x = (screen_w - w) // 2 + 300 
        y = (screen_h - h) // 2
        
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        
        # Canvas для малювання
        self.canvas = tk.Canvas(self.window, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def calculate_bounds(self):
        """Розрахунок меж графіка з примусовим включенням нуля."""
        x_vals = [p[0] for p in self.points]
        y_vals = [p[1] for p in self.points]
        
        x_min_data, x_max_data = min(x_vals), max(x_vals)
        y_min_data, y_max_data = min(y_vals), max(y_vals)
        
        # Визначаємо діапазон даних
        x_range = max(1.0, x_max_data - x_min_data)
        y_range = max(1.0, y_max_data - y_min_data)
        
        # Межі з відступом
        x_min_raw = x_min_data - x_range * 0.1
        y_min_raw = y_min_data - y_range * 0.1
        
        # Примусово встановлюємо мінімальні межі відображення, щоб нуль був видимий
        x_min_plot = min(0.0, x_min_raw)
        y_min_plot = min(0.0, y_min_raw)
        
        x_max_plot = x_max_data + x_range * 0.1
        y_max_plot = y_max_data + y_range * 0.1
        
        return {
            'x_min': x_min_plot, 'x_max': x_max_plot,
            'y_min': y_min_plot, 'y_max': y_max_plot,
            'x_range': x_max_plot - x_min_plot,
            'y_range': y_max_plot - y_min_plot
        }
    
    def setup_coordinate_system(self, bounds):
        """Налаштування системи координат та функції перетворення."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 100 or height < 100: return None, None
        
        margin = {'left': 80, 'right': 40, 'top': 60, 'bottom': 80}
        plot_w = width - margin['left'] - margin['right']
        plot_h = height - margin['top'] - margin['bottom']
        
        # Функція перетворення (масштабування) координат даних у координати Canvas
        def to_screen(x, y):
            screen_x = margin['left'] + (x - bounds['x_min']) / bounds['x_range'] * plot_w
            # Інвертуємо Y, оскільки Canvas Y зростає вниз
            screen_y = margin['top'] + plot_h - (y - bounds['y_min']) / bounds['y_range'] * plot_h
            return screen_x, screen_y
        
        return to_screen, {'width': width, 'height': height, 'margin': margin}

    # --- Методи Малювання ---
    
    def _get_tick_step(self, data_range):
        """Визначає оптимальний цілочисельний крок для поділок."""
        if data_range > 40: return 5
        if data_range > 20: return 2
        return 1

    def draw_grid(self, to_screen, bounds):
        """Малювання сітки."""
        
        # Вертикальні лінії
        x_start = math.floor(bounds['x_min'])
        x_end = math.ceil(bounds['x_max'])
        step_x = self._get_tick_step(x_end - x_start)

        for x_val in range(x_start, x_end + 1, step_x):
            if bounds['x_min'] < x_val < bounds['x_max']:
                sx, sy1 = to_screen(x_val, bounds['y_min'])
                _, sy2 = to_screen(x_val, bounds['y_max'])
                self.canvas.create_line(sx, sy1, sx, sy2, fill="#e8e8e8", width=1, dash=(2, 2))
        
        # Горизонтальні лінії
        y_start = math.floor(bounds['y_min'])
        y_end = math.ceil(bounds['y_max'])
        step_y = self._get_tick_step(y_end - y_start)

        for y_val in range(y_start, y_end + 1, step_y):
            if bounds['y_min'] < y_val < bounds['y_max']:
                sx1, sy = to_screen(bounds['x_min'], y_val)
                sx2, _ = to_screen(bounds['x_max'], y_val)
                self.canvas.create_line(sx1, sy, sx2, sy, fill="#e8e8e8", width=1, dash=(2, 2))
    
    def draw_axes(self, to_screen, bounds):
        """Малювання осей X та Y, враховуючи положення нуля."""
        
        # Визначаємо положення осей
        zero_x_val = max(bounds['x_min'], min(0.0, bounds['x_max']))
        zero_y_val = max(bounds['y_min'], min(0.0, bounds['y_max']))
        
        # --- Вісь X (горизонтальна, проходить через zero_y_val) ---
        start_x, start_y = to_screen(bounds['x_min'], zero_y_val)
        end_x, end_y = to_screen(bounds['x_max'], zero_y_val)
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="black", width=3)
        
        # Стрілка та підпис X
        arrow = 12
        self.canvas.create_line(end_x, end_y, end_x - arrow, end_y - arrow, fill="black", width=3)
        self.canvas.create_line(end_x, end_y, end_x - arrow, end_y + arrow, fill="black", width=3)
        self.canvas.create_text(end_x + 25, end_y - 10, text="X", font=("Arial", 16, "bold"))
        
        # --- Вісь Y (вертикальна, проходить через zero_x_val) ---
        start_x_y, start_y_y = to_screen(zero_x_val, bounds['y_min'])
        end_x_y, end_y_y = to_screen(zero_x_val, bounds['y_max'])
        self.canvas.create_line(start_x_y, start_y_y, end_x_y, end_y_y, fill="black", width=3)
        
        # Стрілка та підпис Y
        self.canvas.create_line(end_x_y, end_y_y, end_x_y - arrow, end_y_y + arrow, fill="black", width=3)
        self.canvas.create_line(end_x_y, end_y_y, end_x_y + arrow, end_y_y + arrow, fill="black", width=3)
        self.canvas.create_text(start_x_y - 25, end_y_y + 25, text="Y", font=("Arial", 16, "bold"))
        
        self.draw_ticks(to_screen, bounds, zero_x_val, zero_y_val)
    
    def draw_ticks(self, to_screen, bounds, zero_x_val, zero_y_val):
        """Малювання цілочисельних поділок та їх підписів."""
        
        # На осі X
        x_start = math.floor(bounds['x_min'])
        x_end = math.ceil(bounds['x_max'])
        step_x = self._get_tick_step(x_end - x_start)
        
        for x_val in range(x_start, x_end + 1, step_x):
            if bounds['x_min'] <= x_val <= bounds['x_max']:
                sx, sy = to_screen(x_val, zero_y_val)
                
                # Позначка (крім 0, якщо вісь чітко проходить через нього)
                if x_val != 0 or zero_y_val != 0.0:
                     self.canvas.create_line(sx, sy - 6, sx, sy + 6, fill="black", width=2)
                
                # Підпис
                if x_val != 0 or (abs(zero_x_val) > 0.01 and abs(zero_y_val) > 0.01):
                    self.canvas.create_text(sx, sy + 20, text=str(x_val), font=("Arial", 11, "bold"), fill="darkblue")

        # На осі Y
        y_start = math.floor(bounds['y_min'])
        y_end = math.ceil(bounds['y_max'])
        step_y = self._get_tick_step(y_end - y_start)

        for y_val in range(y_start, y_end + 1, step_y):
            if bounds['y_min'] <= y_val <= bounds['y_max']:
                sx, sy = to_screen(zero_x_val, y_val)

                # Позначка
                if y_val != 0 or zero_x_val != 0.0:
                    self.canvas.create_line(sx - 6, sy, sx + 6, sy, fill="black", width=2)
                
                # Підпис
                if y_val != 0:
                    self.canvas.create_text(sx - 15, sy, text=str(y_val), font=("Arial", 11, "bold"), fill="darkblue", anchor=tk.E)
    
    def draw_graph(self, to_screen):
        """Малювання точок та лінії графіка."""
        
        screen_points = [to_screen(x, y) for x, y in self.points]
        
        # Лінія
        if len(screen_points) > 1:
            points_flat = [coord for point in screen_points for coord in point]
            self.canvas.create_line(points_flat, fill="blue", width=3)
        
        # Точки
        point_size = 4
        for sx, sy in screen_points:
            self.canvas.create_oval(
                sx - point_size, sy - point_size,
                sx + point_size, sy + point_size,
                fill="red", outline="darkred", width=1
            )
    
    def plot_graph(self):
        """Головна функція малювання графіка."""
        self.canvas.delete("all")
        
        if len(self.points) < 2: return
        
        bounds = self.calculate_bounds()
        to_screen, layout = self.setup_coordinate_system(bounds)
        
        if not to_screen:
            self.window.after(100, self.plot_graph)
            return
        
        self.draw_grid(to_screen, bounds)
        self.draw_axes(to_screen, bounds)
        self.draw_graph(to_screen)
        self.add_labels(bounds, layout)

    def add_labels(self, bounds, layout):
        """Додавання заголовка та інформаційних підписів."""
        self.canvas.create_text(
            layout['width'] // 2, 25,
            text="ГРАФІК ФУНКЦІЇ y = f(x)",
            font=("Arial", 18, "bold"), fill="darkred"
        )
        
        info = (
            f"Точок: {len(self.points)} | "
            f"X: {math.floor(bounds['x_min'])}..{math.ceil(bounds['x_max'])} | "
            f"Y: {math.floor(bounds['y_min'])}..{math.ceil(bounds['y_max'])}"
        )
        
        self.canvas.create_text(
            layout['width'] // 2, layout['height'] - 25,
            text=info, font=("Arial", 12), fill="green"
        )

def main():
    """Точка входу для Object3."""
    try:
        points = []
        with open(GraphPlotter.CLIPBOARD_FILENAME, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        x, y = map(float, line.split())
                        points.append((x, y))
                    except:
                        continue
        
        if len(points) >= 2:
            GraphPlotter(points)
        else:
            print(f"Object3: Недостатньо даних у {GraphPlotter.CLIPBOARD_FILENAME} (мінімум 2 точки).")
            input("Натисніть Enter...")
            
    except FileNotFoundError:
        print(f"Object3: Файл {GraphPlotter.CLIPBOARD_FILENAME} не знайдено. Запустіть Lab6.")
        input("Натисніть Enter...")
    except Exception as e:
        print(f"Object3: Критична помилка під час виконання: {e}")


if __name__ == "__main__":
    main()