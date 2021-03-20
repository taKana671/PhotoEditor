import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import filedialog

from TkinterDnD2 import *

import composite_board
import connect_board

CONNECT = 'Connect'
COMPOSITE = 'Composite'


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, width=1200, height=500)
        self.editor_boards = {}
        self.create_ui()

    def create_ui(self):
        self.create_board()
        self.create_menu()

    def create_board(self):
        base_frame = ttk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        for name, module in zip((CONNECT, COMPOSITE),
                (connect_board, composite_board)):
            frame = ttk.Frame(base_frame)
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            board = module.EditorBoard(frame)
            board.pack(fill=tk.BOTH, expand=True)
            self.editor_boards[name] = frame

    def change_boards(self, board_name):
        frame = self.editor_boards[board_name]
        frame.tkraise()

    def create_menu(self):
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        menu = tk.Menu(self.menubar, tearoff=0, name='game')
        menu.add_command(label='Connect', 
                         command=lambda: self.change_boards(CONNECT),
                         compound=tk.LEFT)
        menu.add_command(label='Composite', 
                         command=lambda: self.change_boards(COMPOSITE),
                         compound=tk.LEFT)
        self.menubar.add_cascade(label="Menu", menu=menu)

    def close(self, event=None):
        self.quit()


if __name__ == '__main__':
    app = TkinterDnD.Tk()
    # app.geometry('650x500')
    # app.withdraw()
    app.resizable(False, False)
    app.title('Image Editor')
    window = Window(app)
    app.protocol('WM_DELETE_WINDOW', window.close)
    app.mainloop()
    # app = tk.Tk()
    # app.title('Image Editor')
    # window = Window(app)
    # app.protocol('WM_DELETE_WINDOW', window.close)
    # app.mainloop()







