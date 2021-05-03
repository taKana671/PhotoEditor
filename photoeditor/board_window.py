import tkinter as tk
import tkinter.ttk as ttk

from config import PADY

class BoardWindow(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.create_variables()
        self.create_ui()

    def create_variables(self):
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.create_board_variables()

    def create_ui(self):
        base_frame = tk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        self.create_left_canvas(base_frame)
        self.create_right_canvas(base_frame)
        self.create_controller(base_frame)

    def create_save_widgets(self, controller_frame, command):
        height_entry = ttk.Entry(controller_frame, width=5, textvariable=self.height_var)
        height_entry.pack(side=tk.RIGHT, pady=PADY, padx=(1, 5))
        height_label = ttk.Label(controller_frame, text='H:')
        height_label.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        width_entry = ttk.Entry(controller_frame, width=5, textvariable=self.width_var)
        width_entry.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        width_label = ttk.Label(controller_frame, text='W:')
        width_label.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        save_button = ttk.Button(
            controller_frame, text='Save', command=command)
        save_button.pack(side=tk.RIGHT, pady=PADY, padx=(20, 1))

    def create_board_variables(self):
        raise NotImplementedError()

    def create_left_canvas(self):
        raise NotImplementedError()

    def create_right_canvas(self):
        raise NotImplementedError()

    def create_controller(self):
        raise NotImplementedError()
