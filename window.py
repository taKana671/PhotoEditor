import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk

from editor_board import CoverImageCanvas, BaseImageCanvas
from TkinterDnD2 import *

class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, width=1200, height=500)
        self.create_ui()

    def create_ui(self):
        base_frame = tk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        self.create_cover_image_canvas(base_frame)
        self.create_base_image_canvas(base_frame)
        self.create_controller(base_frame)

    def create_cover_image_canvas(self, base_frame):
        self.cover_image_canvas = CoverImageCanvas(base_frame)
        self.cover_image_canvas.grid(row=0, column=0, padx=(5, 1),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
           
    def create_base_image_canvas(self, base_frame):
        self.base_image_canvas = BaseImageCanvas(base_frame)
        self.base_image_canvas.grid(row=0, column=1, padx=(1, 5),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(row=1, column=0, columnspan=2, 
            sticky=(tk.W, tk.E, tk.N, tk.S))
        save_button = ttk.Button(controller_frame, text='save', 
            command=self.base_image_canvas.save_image)
        save_button.pack()
 
    def close(self, event=None):
        self.quit()


if __name__ == '__main__':
    app = TkinterDnD.Tk()
    # app.geometry('650x500')
    # app.withdraw()
    app.title('Image Editor')
    window = Window(app)
    app.protocol('WM_DELETE_WINDOW', window.close)
    app.mainloop()
    # app = tk.Tk()
    # app.title('Image Editor')
    # window = Window(app)
    # app.protocol('WM_DELETE_WINDOW', window.close)
    # app.mainloop()







