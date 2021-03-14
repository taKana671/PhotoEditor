import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox


class InvalidSizeError(Exception):
    pass


class BaseBoard(tk.Canvas):

    drag_start = False
   
    def __init__(self, master, width_var=None, height_var=None):
        self.img_path = None
        self.current_img = None
        self.width_var = width_var
        self.height_var = height_var
        super().__init__(master, width=600, height=500, bg='snow')
     
    def show_image(self, path):
        self.current_img = Image.open(path)
        self.img_path = Path(path)
        self.display_img = ImageTk.PhotoImage(self.current_img.resize((600, 500)))
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)

    def save_image(self):
        if self.img_path:
            save_path = filedialog.asksaveasfilename(
                initialdir=self.img_path.parent,
                title='Save as',
                filetypes=[('jpg', '*.jpg'), ('png', '*.png')])
            if save_path:
                try:
                    width = int(self.width_var.get())
                    height = int(self.height_var.get())
                    if not width or not height:
                        raise InvalidSizeError('Value of Width or Height is invalid.')
                    if self.current_img.size != (width, height):
                        save_img = self.current_img.copy()
                        save_img.thumbnail((width, height), Image.BICUBIC)
                        save_img.save(save_path)
                    else:
                        self.current_img.save(save_path)
                except Exception as e:
                    messagebox.showerror('Error', e)
                else:
                    messagebox.showinfo('Info', 'Save successfully.')
