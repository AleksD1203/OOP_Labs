import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional
from shape import Shape

class MyTable:
    def __init__(self):
        self._window: Optional[tk.Toplevel] = None
        self._tree: Optional[ttk.Treeview] = None
        self._selection_callback: Optional[Callable] = None
        self._shapes_buffer: List[Shape] = []
    
    def set_selection_callback(self, callback: Callable):
        """Встановлення callback-функції для виділення/видалення"""
        self._selection_callback = callback
    
    def show(self):
        """Показати вікно таблиці"""
        if self._window is not None and self._window.winfo_exists():
            self._window.lift()
            return
        
        self._window = tk.Toplevel()
        self._window.title("Таблиця об'єктів")
        self._window.geometry("600x400")
        
        self._create_table()
        self._window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Додаємо фігури з буфера
        for shape in self._shapes_buffer:
            self._add_shape_to_tree(shape)
        self._shapes_buffer.clear()
    
    def _create_table(self):
        """Створення таблиці"""
        frame = ttk.Frame(self._window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._tree = ttk.Treeview(frame, columns=('name', 'x1', 'y1', 'x2', 'y2'), 
                                 show='headings', selectmode='browse')
        
        # Заголовки стовпців
        self._tree.heading('name', text='Назва')
        self._tree.heading('x1', text='x1')
        self._tree.heading('y1', text='y1')
        self._tree.heading('x2', text='x2')
        self._tree.heading('y2', text='y2')
        
        self._tree.column('name', width=120)
        self._tree.column('x1', width=80)
        self._tree.column('y1', width=80)
        self._tree.column('x2', width=80)
        self._tree.column('y2', width=80)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._tree.bind('<<TreeviewSelect>>', self._on_select)
        
        button_frame = ttk.Frame(self._window)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Видалити виділений", 
                  command=self._on_delete).pack(side=tk.LEFT, padx=5)
    
    def _add_shape_to_tree(self, shape: Shape):
        """Безпечне додавання форми до таблиці"""
        if self._tree and self._window and self._window.winfo_exists():
            try:
                name = shape.get_name()
                x1, y1, x2, y2 = shape.get_coordinates()
                self._tree.insert('', 'end', values=(name, x1, y1, x2, y2))
            except tk.TclError:
                pass
    
    def add_shape(self, shape: Shape):
        """Додавання форми до таблиці"""
        if self._window and self._tree and self._window.winfo_exists():
            self._add_shape_to_tree(shape)
        else:
            self._shapes_buffer.append(shape)
    
    def clear(self):
        """Очищення таблиці"""
        if self._tree and self._window and self._window.winfo_exists():
            try:
                for item in self._tree.get_children():
                    self._tree.delete(item)
            except tk.TclError:
                pass
        self._shapes_buffer.clear()
    
    def _on_select(self, event):
        """Обробник виділення рядка"""
        if (self._selection_callback and self._tree and 
            self._window and self._window.winfo_exists()):
            try:
                selection = self._tree.selection()
                if selection:
                    index = self._tree.index(selection[0])
                    self._selection_callback(index)
            except tk.TclError:
                pass
    
    def _on_delete(self):
        """Обробник видалення виділеного рядка"""
        if (self._selection_callback and self._tree and 
            self._window and self._window.winfo_exists()):
            try:
                selection = self._tree.selection()
                if selection:
                    index = self._tree.index(selection[0])
                    self._selection_callback(index, delete=True)
            except tk.TclError:
                pass
    
    def remove_shape_from_table(self, index: int):
        """Видалення форми з таблиці (викликається після підтвердження)"""
        if self._tree and self._window and self._window.winfo_exists():
            try:
                items = self._tree.get_children()
                if 0 <= index < len(items):
                    self._tree.delete(items[index])
            except tk.TclError:
                pass
    
    def _on_close(self):
        """Закриття вікна таблиці"""
        if self._window:
            try:
                self._window.destroy()
            except tk.TclError:
                pass
            self._window = None
            self._tree = None