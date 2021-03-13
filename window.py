import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import filedialog

from TkinterDnD2 import *

from composite_board import EditorBoard
# from connect_board import EditorBoard


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, width=1200, height=500)
        self.create_ui()
        self.editor_boards = {}

    def create_ui(self):
        base_frame = ttk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        composite_board = EditorBoard(base_frame)
        composite_board.pack(fill=tk.BOTH, expand=True)

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







