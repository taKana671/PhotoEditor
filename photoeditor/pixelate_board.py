import math
import tkinter as tk
import tkinter.ttk as ttk
from collections import namedtuple
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageTk
from scipy.interpolate import splrep, splev
from TkinterDnD2 import *

from base_board import BaseBoard
from board_window import BoardWindow
from config import PADY, BOARD_W, BOARD_H


Rectangle = namedtuple('Rectangle', 'x y width height')


class EditorBoard(BoardWindow):

    def __init__(self, master):
        self.rectangle_tag = 'rect'
        self.left_top_x = None
        self.left_top_y = None
        self.right_bottom_x = None
        self.right_bottom_y = None
        super().__init__(master)

    def create_board_variables(self):
        self.ratio_double = tk.DoubleVar()

    def create_left_canvas(self, base_frame):
        self.left_canvas = LeftCanvas(base_frame)
        self.left_canvas.grid(
            row=0, column=0, padx=(5, 1), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_right_canvas(self, base_frame):
        self.right_canvas = RightCanvas(
            base_frame, self.width_var, self.height_var, self.ratio_double,
            self.get_rectangle, self.clear_rectangle)
        self.right_canvas.grid(
            row=0, column=1, padx=(1, 5), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.right_canvas.bind('<ButtonPress-1>', self.start_drawing)
        self.right_canvas.bind('<Button1-Motion>', self.draw_rectangle)
        self.right_canvas.bind('<ButtonRelease-1>', self.end_drawing)

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_save_widgets(controller_frame, self.right_canvas.save_open_cv)
        self.create_pixelate_widgets(controller_frame)

    def create_pixelate_widgets(self, controller_frame):
        ratio_list = [0.1, 0.05]
        for ratio in ratio_list:
            radio = ttk.Radiobutton(
                controller_frame, text=str(ratio), value=ratio, variable=self.ratio_double)
            radio.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        self.ratio_double.set(ratio_list[-1])
        entire_button = ttk.Button(
            controller_frame, text='Entire', command=self.right_canvas.show_pixelated_entire)
        entire_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        area_button = ttk.Button(
            controller_frame, text='Area', command=self.right_canvas.show_pixelated_area)
        area_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))

    def get_img_size(self):
        img_width = self.right_canvas.display_img.width()
        img_height = self.right_canvas.display_img.height()
        return img_width, img_height

    def start_drawing(self, event):
        """Get x, y at the clicked point.
        """
        if self.right_canvas.display_img:
            self.clear_rectangle()
            img_width, img_height = self.get_img_size()
            if event.x < img_width and event.y < img_height:
                self.right_canvas.create_rectangle(
                    event.x, event.y, event.x, event.y, outline='white', tag=self.rectangle_tag)
                self.start_x = event.x
                self.start_y = event.y

    def draw_rectangle(self, event):
        """Draw rectangle.
        """
        if self.right_canvas.display_img:
            img_width, img_height = self.get_img_size()
            end_x = min(img_width, event.x)
            end_y = min(img_height, event.y)
            self.right_canvas.coords(
                self.rectangle_tag, self.start_x, self.start_y, end_x, end_y)

    def end_drawing(self, event):
        """Get the left top and right bottom of the rectangle.
        """
        if self.right_canvas.display_img:
            self.left_top_x, self.left_top_y, self.right_bottom_x, self.right_bottom_y = \
                self.right_canvas.coords(self.rectangle_tag)

    def get_rectangle(self):
        """Returns namedtuple or None.
        """
        if all([self.left_top_x, self.left_top_y,
               self.right_bottom_x, self.right_bottom_y]):
            width = self.right_bottom_x - self.left_top_x
            height = self.right_bottom_y - self.left_top_y
            return Rectangle(self.left_top_x, self.left_top_y, width, height)
        return None

    def clear_rectangle(self):
        """Delete rectangle.
        """
        self.right_canvas.delete(self.rectangle_tag)
        self.left_top_x = None
        self.left_top_y = None
        self.right_bottom_x = None
        self.right_bottom_y = None


class PixelateBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)

    def show_image(self, path):
        """Display an image on a canvas when the image was dropped.
        """
        self.delete('all')
        self.current_img = cv2.imread(path)
        self.img_path = Path(path)
        # img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_photo_image()

    # def create_photo_image(self, img_rgb):
    def create_photo_image(self):
        h, w = self.current_img.shape[:2]
        img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        if w <= BOARD_W and h <= BOARD_H:
            self.display_img = ImageTk.PhotoImage(img_pil)
        else:
            nw, nh = self.get_cv_aspect()
            self.display_img = ImageTk.PhotoImage(img_pil.resize((nw, nh)))
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)

    def get_display_image(self):
        h, w = self.current_img.shape[:2]
        if w <= BOARD_W and h <= BOARD_H:
            return self.current_img
        else:
            nw, nh = self.get_cv_aspect()
            return cv2.resize(self.current_img, dsize=(nw, nh))


class LeftCanvas(PixelateBoard):
    """The left canvas to show an original image.
    """
    def __init__(self, master):
        super().__init__(master)
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.drag_source_register(1, '*')
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)
        self.dnd_bind('<<DragInitCmd>>', self.drag_init)
        self.dnd_bind('<<DragEndCmd>>', self.drag_end)

    def drop_enter(self, event):
        event.widget.focus_force()
        print(f'Drop_enter: {event.widget}')
        return event.action

    def drop_position(self, event):
        print(f'Position: x {event.x_root}, y {event.y_root}')
        return event.action

    def drop_leave(self, event):
        print(f'Drop_leaving {event.widget}')

    def drop(self, event):
        print(f'Drop: {event.widget}')
        if self.is_image_file(event.data):
            self.show_image(event.data)

    def drag_init(self, event):
        """Set BaseBoard.drag_start to True,
           when drag starts from the left canvas.
        """
        print(f'Drag_start: {event.widget}')
        BaseBoard.drag_start = True
        data = (self.img_path, )
        return((ASK, COPY), (DND_FILES), data)

    def drag_end(self, event):
        print(f'Drag_ended: {event.widget}')


class RightCanvas(PixelateBoard):
    """The right canvas to show a pixelated image.
    """
    def __init__(self, master, width_var, height_var, ratio_double,
                 get_rectangle, clear_rectangle):
        super().__init__(master, width_var, height_var)
        self.ratio_double = ratio_double
        self.get_rectangle = get_rectangle
        self.clear_rectangle = clear_rectangle
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def drop_enter(self, event):
        event.widget.focus_force()
        print(f'Drop_enter: {event.widget}')
        return event.action

    def drop_position(self, event):
        print(f'Position: x {event.x_root}, y {event.y_root}')
        return event.action

    def drop_leave(self, event):
        print(f'Drop_Leave {event.widget}')

    def drop(self, event):
        """Display image and its size, only when the imaged was
           dragged from the left canvas.
        """
        print('Dropped:', event.widget)
        if BaseBoard.drag_start:
            self.show_image(event.data)
            self.display_image_size(*self.current_img.shape[:-1][::-1])
            BaseBoard.drag_start = False

    def pixelate(self, img):
        ratio = self.ratio_double.get()
        smaller = cv2.resize(
            img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(smaller, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def show_pixelated_entire(self):
        img = cv2.imread(self.img_path.as_posix())
        self.current_img = self.pixelate(img)
        # img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_photo_image()

    def show_pixelated_area(self):
        if rectangle := self.get_rectangle():
            current_h, current_w = self.current_img.shape[:2]
            # get magnification ratio
            scale_x = current_w / self.display_img.width()
            scale_y = current_h / self.display_img.height()
            # get x, y, width and height of the self.current_img
            x = int(rectangle.x * scale_x)
            y = int(rectangle.y * scale_y)
            width = int(rectangle.width * scale_x)
            height = int(rectangle.height * scale_y)
            self.current_img[y:y + height, x:x + width] = \
                self.pixelate(self.current_img[y:y + height, x:x + width])
            self.create_photo_image()
            self.clear_rectangle()