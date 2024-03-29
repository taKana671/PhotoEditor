import os
import tkinter as tk
import tkinter.ttk as ttk
from functools import wraps
from pathlib import Path
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from config import (BOARD_W, BOARD_H, EXTENSIONS, FILETYPES, ERROR,
    INFO, RIGHT_CANVAS_MSG_1, SAVE_MSG_1, SAVE_MSG_2, SAVE_MSG_3, DIALOG_TITLE, GIF_FILETYPES)


class InvalidSizeError(Exception):
    pass


class NoImageOnTheCanvasError(Exception):
    pass


class NotSelectedAreaError(Exception):
    pass


class TheNumberOfImagesError(Exception):
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

    def create_image_pil(self, img):
        self.delete('all')
        self.display_img = self.get_display_image_pil(img)
        self.photo_img = ImageTk.PhotoImage(self.display_img)
        self.create_image(0, 0, image=self.photo_img, anchor=tk.NW)

    def get_display_image_pil(self, img):
        w, h = img.size
        if w <= BOARD_W and h <= BOARD_H:
            return img
        else:
            copy_img = img.copy()
            copy_img.thumbnail((BOARD_W, BOARD_H), Image.BICUBIC)
            return copy_img

    def create_image_cv(self, img):
        self.delete('all')
        self.display_img = self.get_display_image_cv(img)
        self.photo_img = ImageTk.PhotoImage(self.display_img)
        self.create_image(0, 0, image=self.photo_img, anchor=tk.NW)

    def get_display_image_cv(self, img):
        h, w = img.shape[:2]
        img_pil = Image.fromarray(img)
        if w <= BOARD_W and h <= BOARD_H:
            return img_pil
        else:
            nw, nh = self.get_cv_aspect()
            return img_pil.resize((nw, nh))

    def is_image_file(self, path):
        if os.path.isfile(path):
            _, ext = os.path.splitext(path)
            if ext in EXTENSIONS:
                return True
        return False

    def save_image(save_func):
        @wraps(save_func)
        def save_decorator(self):
            try:
                if self.current_img is None:
                    raise NoImageOnTheCanvasError(RIGHT_CANVAS_MSG_1)
                if not (width := int(self.width_var.get())) or not (height := int(self.height_var.get())):
                    raise InvalidSizeError(SAVE_MSG_1)
                save_path = filedialog.asksaveasfilename(
                    title=DIALOG_TITLE,
                    filetypes=FILETYPES)
                if save_path:
                    save_func(self, save_path, width, height)
                    messagebox.showinfo(INFO, SAVE_MSG_2)
            except ValueError:
                messagebox.showerror(ERROR, SAVE_MSG_3)
            except (NoImageOnTheCanvasError, InvalidSizeError) as e:
                messagebox.showerror(ERROR, e)
        return save_decorator

    def save_gif(save_func):
        @wraps(save_func)
        def save_decorator(self):
            try:
                if self.current_img is None:
                    raise NoImageOnTheCanvasError(RIGHT_CANVAS_MSG_1)
                save_path = filedialog.asksaveasfilename(
                    title=DIALOG_TITLE,
                    filetypes=GIF_FILETYPES)
                if save_path:
                    save_func(self, save_path)
                    messagebox.showinfo(INFO, SAVE_MSG_2)
            except Exception as e:
                messagebox.showerror(ERROR, e)
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

    @save_gif
    def save_gif_file(self, save_path):
        imgs = self.create_animated_gif()
        imgs[0].save(
            save_path,
            save_all=True,
            append_images=imgs[1:],
            optimize=False,
            duration=50,
            loop=0)
