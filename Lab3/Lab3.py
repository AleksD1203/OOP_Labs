import tkinter as tk
from shape_editor import ShapeObjectsEditor


def main():
    """Головна функція програми - точка входу"""
    root = tk.Tk()
    editor = ShapeObjectsEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()