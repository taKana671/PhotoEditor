import os
import tkinter as tk
import tkinter.ttk as ttk
from functools import wraps
from pathlib import Path
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from config import BOARD_W, BOARD_H

class InvalidSizeError(Exception):
    pass


class BaseBoard(tk.Canvas):

    drag_start = False
   
    def __init__(self, master, width_var=None, height_var=None):
        self.current_img = None
        self.display_img = None
        self.width_var = width_var
        self.height_var = height_var
        super().__init__(master, width=BOARD_W, height=BOARD_H, bg='snow')

    def display_image_size(self, width, height):
        self.width_var.set(width)
        self.height_var.set(height)
     
    def create_photo_image(self):
        display_img = self.get_display_image()
        self.delete('all')
        self.display_img = ImageTk.PhotoImage(display_img)
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)
        
    def get_display_image(self):
        w, h = self.current_img.size
        if w <= BOARD_W and h <= BOARD_H:
            return self.current_img
        else:
            img = self.current_img.copy()
            img.thumbnail((BOARD_W, BOARD_H), Image.BICUBIC)
            return img

    def is_image_file(self, path):
        if os.path.isfile(path):
            _, ext = os.path.splitext(path)
            if ext in {'.bmp', '.tiff', '.jpg', '.png', '.PNG'}:
                return True
        return False

    def save_image(save_func):
        @wraps(save_func)
        def save_decorator(self):
            if self.current_img is not None:
                save_path = filedialog.asksaveasfilename(
                    title='Save as',
                    filetypes=[('jpg', '*.jpg'), ('png', '*.png')])
                if save_path:
                    try:
                        width = int(self.width_var.get())
                        height = int(self.height_var.get())
                        if not width or not height:
                            raise InvalidSizeError('Value of Width or Height is invalid.')
                        save_func(self, save_path, width, height)
                    except Exception as e:
                        messagebox.showerror('Error', e)
                    else:
                        messagebox.showinfo('Info', 'Save successfully.')
        return save_decorator

    @save_image
    def save_with_pil(self, save_path, width, height):
        if self.current_img.size != (width, height):
            save_img = self.current_img.copy()
            save_img.thumbnail((width, height), Image.BICUBIC)
            save_img.save(save_path)
        else:
            self.current_img.save(save_path)

    @save_image
    def save_open_cv(self, save_path, width, height):
        if self.current_img.shape[:2] != (height, width):
            nw, nh = self.get_cv_aspect(width, height)
            save_img = cv2.resize(self.current_img, dsize=(nw, nh))
            cv2.imwrite(Path(save_path).as_posix(), save_img)
        else:
            cv2.imwrite(Path(save_path).as_posix(), self.current_img)

    def get_cv_aspect(self, width=BOARD_W, height=BOARD_H):
        h, w = self.current_img.shape[:2]
        aspect = w / h
        if width / height >= aspect:
            nh = height
            nw = round(nh * aspect)
        else:
            nw = width
            nh = round(nw / aspect)
        return nw, nh