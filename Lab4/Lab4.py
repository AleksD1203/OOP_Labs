import tkinter as tk
from main_window import MainWindow


def main():
    """Головна функція програми Lab4"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()