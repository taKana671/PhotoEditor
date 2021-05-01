import tkinter as tk
import tkinter.ttk as ttk

from TkinterDnD2 import *

import composite_board
import connect_board
import convert_board
from config import WINDOW_W, WINDOW_H, CONNECT, COMPOSITE, CONVERT


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, width=WINDOW_W, height=WINDOW_H)
        self.editor_boards = {}
        self.create_ui()

    def create_ui(self):
        base_frame = ttk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        self.create_board(base_frame)
        self.create_menu(base_frame)

    def create_board(self, base_frame):
        board_frame = ttk.Frame(base_frame)
        board_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        for name, module in zip((CONNECT, COMPOSITE, CONVERT),
                                (connect_board, composite_board, convert_board)):
            frame = ttk.Frame(board_frame)
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            board = module.EditorBoard(frame)
            board.pack(fill=tk.BOTH, expand=True)
            self.editor_boards[name] = frame

    def change_boards(self, board_name):
        frame = self.editor_boards[board_name]
        frame.tkraise()

    def create_menu(self, base_frame):
        menu_frame = ttk.Frame(base_frame)
        menu_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.menu_bool = tk.IntVar()
        texts = [CONVERT, COMPOSITE, CONNECT]
        commands = [
            lambda: self.change_boards(CONVERT),
            lambda: self.change_boards(COMPOSITE),
            lambda: self.change_boards(CONNECT)]
        for num, (text, command) in enumerate(zip(texts, commands), 1):
            radio = ttk.Radiobutton(
                menu_frame, text=text, value=num, variable=self.menu_bool, command=command)
            radio.pack(side=tk.LEFT, pady=(4, 0), padx=(5, 1))
        self.menu_bool.set(1)

    def close(self, event=None):
        self.quit()


if __name__ == '__main__':
    app = TkinterDnD.Tk()
    app.resizable(False, False)
    app.title('Photo Editor')
    window = Window(app)
    app.protocol('WM_DELETE_WINDOW', window.close)
    app.mainloop()
