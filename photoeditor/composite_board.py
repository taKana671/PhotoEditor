import re
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

import numpy as np
from TkinterDnD2 import *

from base_board import BaseBoard
from board_window import BoardWindow
from config import PADY


class EditorBoard(BoardWindow):

    def __init__(self, master):
        self.vertices = {}
        super().__init__(master)

    def create_board_variables(self):
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.blur_bool = tk.BooleanVar()
        self.rectangle_bool = tk.BooleanVar()

    def create_left_canvas(self, base_frame):
        """Create the left canvas.
        """
        self.left_canvas = LeftCanvas(
            base_frame, self.vertices, self.blur_bool, self.rectangle_bool)
        self.left_canvas.grid(
            row=0, column=0, padx=(5, 1), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.left_canvas.bind(
            '<ButtonRelease-3>', self.create_vertices)

    def create_right_canvas(self, base_frame):
        """Create the right canvas.
        """
        self.right_canvas = RightCanvas(
            base_frame, self.width_var, self.height_var)
        self.right_canvas.grid(
            row=0, column=1, padx=(1, 5), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_vertices(self, event):
        """Get the coordinates of where an image displayed
           on the left canvas was right-click, and create
           white ovals there.
        """
        if self.left_canvas.display_img:
            img_width = self.left_canvas.display_img.width()
            img_height = self.left_canvas.display_img.height()
            x, y = event.x, event.y
            if x <= img_width and y <= img_height:
                id = self.left_canvas.create_oval(
                    x, y, x + 7, y + 7, outline='white', fill='white')
                self.vertices[id] = (x, y)

    def delete_vertices(self):
        """Delete white ovals on an image displayed on the left canvas.
        """
        ids = list(self.vertices.keys())
        self.left_canvas.delete(*ids)
        self.vertices.clear()

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_save_widgets(controller_frame, self.right_canvas.save_with_pil)
        self.create_clear_widgets(controller_frame)
        self.create_mask_widgets(controller_frame)
        self.create_crop_widgets(controller_frame)

    def create_clear_widgets(self, controller_frame):
        clear_button = ttk.Button(
            controller_frame, text='Clear', command=self.right_canvas.clear_image)
        clear_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))

    def create_mask_widgets(self, controller_frame):
        reset_button = ttk.Button(
            controller_frame, text='Reset', command=self.delete_vertices)
        reset_button.pack(side=tk.LEFT, pady=PADY, padx=(5, 1))
        create_mask_button = ttk.Button(
            controller_frame, text='Create', command=self.left_canvas.create_new_mask)
        create_mask_button.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))
        check_rectangle = ttk.Checkbutton(
            controller_frame, text='Rectangle', variable=self.rectangle_bool,
            onvalue=True, offvalue=False)
        check_rectangle.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))
        self.blur_bool.set(True)
        check_blur = ttk.Checkbutton(
            controller_frame, text='Blur', variable=self.blur_bool, onvalue=True, offvalue=False)
        check_blur.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))
        mask_button = ttk.Button(
            controller_frame, text='Change', command=self.left_canvas.toggle_mask)
        mask_button.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))

    def create_crop_widgets(self, controller_frame):
        crop_button = ttk.Button(
            controller_frame, text='Crop', command=self.left_canvas.crop_image)
        crop_button.pack(side=tk.LEFT, pady=PADY, padx=(10, 1))


class CompositeBoard(BaseBoard):

    original_mask_id = None
    cropped_image_id = None
    holder = {}
    mask_count = 0

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)
        self.img_path = None

    def show_image(self, path):
        self.delete('all')
        self.current_img = Image.open(path)
        self.img_path = Path(path)
        self.create_photo_image()


class LeftCanvas(CompositeBoard):
    """Left canvas to create masks
    """
    def __init__(self, master, vertices, blur_bool, rectangle_bool):
        super().__init__(master)
        self.vertices = vertices
        self.blur_bool = blur_bool
        self.rectangle_bool = rectangle_bool
        self.get_mask_images()
        self.create_bind()
        self.counter = 0

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        # self.drag_source_register(1, DND_TEXT, DND_FILES)
        self.drag_source_register(1, '*')
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)
        self.dnd_bind('<<DragInitCmd>>', self.drag_init)
        self.dnd_bind('<<DragEndCmd>>', self.drag_end)

    def get_2d_gradient(self, start, stop, width, height, is_horizontal):
        if is_horizontal:
            return np.tile(np.linspace(start, stop, width), (height, 1))
        else:
            return np.tile(np.linspace(start, stop, height), (width, 1)).T

    def get_3d_gradient(self, start_tuple, stop_tuple, is_horizontal_tuple,
                        width=600, height=500):
        array = np.zeros((height, width, len(start_tuple)), dtype=np.float)
        for i, (start, stop, is_horizontal) in enumerate(
                zip(start_tuple, stop_tuple, is_horizontal_tuple)):
            array[:, :, i] = self.get_2d_gradient(start, stop, width, height, is_horizontal)
        return array

    def create_mask_images(self):
        yield Image.new("L", (600, 500), 128)
        params = [
            [(255, 255, 255), (0, 0, 0), (False, False, False)],
            [(0, 0, 0), (255, 255, 255), (False, False, False)],
            [(255, 255, 255), (0, 0, 0), (True, True, True)],
            [(0, 0, 0), (255, 255, 255), (True, True, True)],
            [(0, 0, 192), (255, 255, 64), (True, False, False)]
        ]
        for param in params:
            start, stop, is_horizontal = param
            array = self.get_3d_gradient(start, stop, is_horizontal)
            yield Image.fromarray(np.uint8(array)).convert('L')

    def get_mask_images(self):
        for i, image in enumerate(self.create_mask_images()):
            CompositeBoard.holder[i] = image
        CompositeBoard.mask_count = len(CompositeBoard.holder)
        CompositeBoard.original_mask_id = CompositeBoard.mask_count
        CompositeBoard.cropped_image_id = CompositeBoard.original_mask_id + 1

    def toggle_mask(self):
        self.counter += 1
        holder_id = self.counter % CompositeBoard.mask_count
        self.current_img = CompositeBoard.holder[holder_id]
        self.create_photo_image()

    def sort_two_vertices(self, vertices):
        left_top_x = min(x[0] for x in vertices)
        left_top_y = min(x[1] for x in vertices)
        right_bottom_x = max(x[0] for x in vertices)
        right_bottom_y = max(x[1] for x in vertices)
        return ((left_top_x, left_top_y), (right_bottom_x, right_bottom_y))

    def sort_multi_vertices(self, vertices):
        # x_center = sum(x[0] for x in vertices) / len(vertices)
        y_center = sum(x[1] for x in vertices) / len(vertices)
        above = [x for x in vertices if x[1] <= y_center]
        below = [x for x in vertices if x[1] > y_center]
        above.sort(reverse=True)
        below.sort()
        return tuple(above + below)

    def draw_shape(self):
        base = Image.new(
            'L', (self.display_img.width(), self.display_img.height()), 0)
        draw = ImageDraw.Draw(base)
        if len(self.vertices) == 2:
            xy = self.sort_two_vertices(self.vertices.values())
            if self.rectangle_bool.get():
                draw.rectangle(xy, fill=255)
            else:
                draw.ellipse(xy, fill=255)
        elif len(self.vertices) >= 3:
            xy = self.sort_multi_vertices(self.vertices.values())
            draw.polygon(xy, fill=255)
        if self.blur_bool.get():
            base = base.filter(ImageFilter.GaussianBlur(4))
        return base

    def create_new_mask(self):
        if len(self.vertices) >= 2:
            self.current_img = self.draw_shape()
            self.create_photo_image()
            self.vertices.clear()
            CompositeBoard.holder[CompositeBoard.original_mask_id] = self.current_img

    def get_key_from_holder(self):
        keys = [k for k, v in CompositeBoard.holder.items() \
            if v == self.current_img]
        if keys:
            return keys[0]
        else:
            return None

    def crop_image(self):
        if len(self.vertices) >= 2:
            base = self.draw_shape()
            self.current_img = self.get_display_image()
            self.current_img.putalpha(base)
            CompositeBoard.holder[CompositeBoard.cropped_image_id] = self.current_img
            self.create_photo_image()
            self.vertices.clear()

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
        print(f'Drag_start: {event.widget}')
        BaseBoard.drag_start = True
        if key := self.get_key_from_holder():
            data = (key,)
        else:
            data = (self.img_path, )
        return((ASK, COPY), (DND_FILES), data)

    def drag_end(self, event):
        print(f'Drag_ended: {event.widget}')


class RightCanvas(CompositeBoard):
    """The right canvas to composite images
    """

    def __init__(self, master, width_var, height_var):
        super().__init__(master, width_var, height_var)
        self.composite_images = []
        self.holder_id = None
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def show_composite_image(self):
        if len(self.composite_images) == 2:
            if self.holder_id and self.holder_id <= CompositeBoard.original_mask_id:
                first_img = Image.open(self.composite_images[0])
                second_img = Image.open(self.composite_images[1]).resize(first_img.size)
                mask = CompositeBoard.holder[self.holder_id].resize(first_img.size)
                self.current_img = Image.composite(first_img, second_img, mask)
                self.create_photo_image()
                self.composite_images = []
                self.holder_id = None

    def clear_image(self):
        self.delete('all')
        self.composite_images = []
        self.holder_id = None

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
        print('Dropped:', event.widget)
        if BaseBoard.drag_start:
            if re.fullmatch('[0-9]+', event.data):
                self.holder_id = int(event.data)
                self.current_img = CompositeBoard.holder[self.holder_id]
                self.create_photo_image()
                self.display_image_size(*self.current_img.size)
            BaseBoard.drag_start = False
        else:
            if self.is_image_file(event.data):
                print('event data', event.data)
                self.show_image(event.data)
                self.display_image_size(*self.current_img.size)
                if len(self.composite_images) == 2:
                    self.composite_images = []
                self.composite_images.append(self.img_path)
        self.show_composite_image()
