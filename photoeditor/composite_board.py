import re
import tkinter as tk
import tkinter.ttk as ttk
from collections import namedtuple
from pathlib import Path
from tkinter import messagebox

from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from TkinterDnD2 import *

from base_board import BaseBoard
from board_window import BoardWindow
from config import PADY, BOARD_W, BOARD_H


Corner = namedtuple('Corner', 'x y')


class EditorBoard(BoardWindow):

    def create_board_variables(self):
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.is_blur = tk.BooleanVar()         # Whether blur check box in checked or not
        self.which_shapes = tk.IntVar()        # Which radio button is selected, rectangle or oval

    def create_left_canvas(self, base_frame):
        """Create the left canvas.
        """
        self.left_canvas = LeftCanvas(
            base_frame, self.is_blur, self.which_shapes)
        self.left_canvas.grid(
            row=0, column=0, padx=(5, 1), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_right_canvas(self, base_frame):
        """Create the right canvas.
        """
        self.right_canvas = RightCanvas(
            base_frame, self.width_var, self.height_var)
        self.right_canvas.grid(
            row=0, column=1, padx=(1, 5), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

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
            controller_frame, text='Reset', command=self.left_canvas.delete_shapes)
        reset_button.pack(side=tk.LEFT, pady=PADY, padx=(5, 1))
        create_mask_button = ttk.Button(
            controller_frame, text='Create', command=self.left_canvas.create_new_mask)
        create_mask_button.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))
        for i, text in enumerate(['Oval', 'Rectangle', 'Corners'], 1):
            radio = ttk.Radiobutton(
                controller_frame, text=text, value=i, variable=self.which_shapes)
            radio.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))
        self.which_shapes.set(1)
        check_blur = ttk.Checkbutton(
            controller_frame, text='Blur', variable=self.is_blur, onvalue=True, offvalue=False)
        check_blur.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))
        self.is_blur.set(True)
        mask_button = ttk.Button(
            controller_frame, text='Change', command=self.left_canvas.toggle_mask)
        mask_button.pack(side=tk.LEFT, pady=PADY, padx=(1, 1))

    def create_crop_widgets(self, controller_frame):
        crop_button = ttk.Button(
            controller_frame, text='Crop', command=self.left_canvas.crop_image)
        crop_button.pack(side=tk.LEFT, pady=PADY, padx=(10, 1))


class CompositeBoard(BaseBoard):

    created_mask_id = None
    cropped_image_id = None
    holder = {}
    mask_count = 0

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)
        self.img_path = None

    def show_image(self, path):
        """When an image is dropped on a canvas,
           the image was open.
        """
        self.current_img = Image.open(path)
        self.img_path = Path(path)
        self.create_image_pil(self.current_img)


class LeftCanvas(CompositeBoard):
    """Left canvas to create masks
    """
    def __init__(self, master, is_blur, which_shapes):
        super().__init__(master)
        self.is_blur = is_blur                # Whether blur check box in checked or not
        self.which_shapes = which_shapes      # Which radio button is selected, rectangle or oval
        self.counter = 0
        self.shape_tag = 'shape'
        self.corners = []
        self.get_mask_images()
        self.create_bind()

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
        self.bind('<ButtonPress-3>', self.start_drawing)
        self.bind('<Button3-Motion>', self.drawing)
        self.bind('<ButtonRelease-3>', self.end_drawing)

    def get_2d_gradient(self, start, stop, width, height, is_horizontal):
        if is_horizontal:
            return np.tile(np.linspace(start, stop, width), (height, 1))
        else:
            return np.tile(np.linspace(start, stop, height), (width, 1)).T

    def get_3d_gradient(self, start_tuple, stop_tuple, is_horizontal_tuple,
                        width=BOARD_W, height=BOARD_H):
        array = np.zeros((height, width, len(start_tuple)), dtype=np.float)
        for i, (start, stop, is_horizontal) in enumerate(
                zip(start_tuple, stop_tuple, is_horizontal_tuple)):
            array[:, :, i] = self.get_2d_gradient(start, stop, width, height, is_horizontal)
        return array

    def create_mask_images(self):
        yield Image.new("L", (BOARD_W, BOARD_H), 128)
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
        CompositeBoard.created_mask_id = CompositeBoard.mask_count
        CompositeBoard.cropped_image_id = CompositeBoard.created_mask_id + 1

    def toggle_mask(self):
        """When change button is clicked,
           change mask images on the canvas.
        """
        self.counter += 1
        holder_id = self.counter % CompositeBoard.mask_count
        self.current_img = CompositeBoard.holder[holder_id]
        self.create_image_pil(self.current_img)

    def sort_corners(self, corners):
        # x_center = sum(x[0] for x in vertices) / len(vertices)
        y_center = sum(x[1] for x in corners) / len(corners)
        above = [x for x in corners if x[1] <= y_center]
        below = [x for x in corners if x[1] > y_center]
        above.sort(reverse=True)
        below.sort()
        return tuple(above + below)

    def get_current_img_corners(self):
        current_w, current_h = self.current_img.size
        display_w, display_h = self.display_img.size
        # get magnification ratio
        scale_x = current_w / display_w
        scale_y = current_h / display_h
        # return the corners on the self.current_img
        return tuple((corner.x * scale_x, corner.y * scale_y) for corner in self.corners)

    def draw_shape(self):
        blur = 4 if self.current_img.size == self.display_img.size else 15
        xy = self.get_current_img_corners()
        base = Image.new('L', self.current_img.size, 0)
        draw = ImageDraw.Draw(base)
        shape_type = self.which_shapes.get()
        print(shape_type)
        if shape_type == 1:
            draw.ellipse(xy, fill=255)
        elif shape_type == 2:
            draw.rectangle(xy, fill=255)
        elif shape_type == 3:
            xy = self.sort_corners(xy)
            draw.polygon(xy, fill=255)
        if self.is_blur.get():
            base = base.filter(ImageFilter.GaussianBlur(blur))
        return base

    def create_new_mask(self):
        if self.corners:
            if self.which_shapes.get() == 3 and len(self.corners) < 3:
                messagebox.showerror('Error', 'Requires more than 3 corners')
            else:
                self.current_img = self.draw_shape()
                self.delete_shapes()
                self.create_image_pil(self.current_img)
                CompositeBoard.holder[CompositeBoard.created_mask_id] = self.current_img

    def crop_image(self):
        if self.corners:
            if self.which_shapes.get() == 3 and len(self.corners) < 3:
                messagebox.showerror('Error', 'Requires more than 3 corners')
            else:
                base = self.draw_shape()
                self.current_img.putalpha(base)
                self.delete_shapes()
                self.create_image_pil(self.current_img)
                CompositeBoard.holder[CompositeBoard.cropped_image_id] = self.current_img

    def get_key_from_holder(self):
        keys = [k for k, v in CompositeBoard.holder.items() if v == self.current_img]
        if keys:
            return keys[0]
        else:
            return None

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

    def start_drawing(self, event):
        """Start drawing a shape.
        """
        if self.display_img:
            shape_type = self.which_shapes.get()
            if shape_type in {1, 2}:
                self.delete_shapes()
            img_width, img_height = self.display_img.size
            if event.x < img_width and event.y < img_height:
                if shape_type == 1:
                    self.create_oval(
                        event.x, event.y, event.x, event.y, outline='white', tag=self.shape_tag)
                    self.start_x, self.start_y = event.x, event.y
                elif shape_type == 2:
                    self.create_rectangle(
                        event.x, event.y, event.x, event.y, outline='white', tag=self.shape_tag)
                    self.start_x, self.start_y = event.x, event.y
                elif shape_type == 3:
                    self.create_oval(event.x, event.y, event.x + 7, event.y + 7,
                                     outline='white', fill='white', tag=self.shape_tag)
                    self.corners.append(Corner(event.x, event.y))

    def drawing(self, event):
        if self.display_img and self.which_shapes.get() in {1, 2}:
            img_width, img_height = self.display_img.size
            end_x = min(img_width, event.x)
            end_y = min(img_height, event.y)
            self.coords(
                self.shape_tag, self.start_x, self.start_y, end_x, end_y)

    def end_drawing(self, event):
        """Get the left top and right bottom of the shape.
        """
        if self.display_img and self.which_shapes.get() in {1, 2}:
            left_top_x, left_top_y, right_bottom_x, right_bottom_y = \
                self.coords(self.shape_tag)
            self.corners.extend([
                Corner(left_top_x, left_top_y),
                Corner(right_bottom_x, right_bottom_y)
            ])

    def delete_shapes(self):
        """Delete shapes drawn on the canvas.
        """
        self.delete(self.shape_tag)
        self.corners = []


class RightCanvas(CompositeBoard):
    """The right canvas to composite images
    """
    def __init__(self, master, width_var, height_var):
        super().__init__(master, width_var, height_var)
        self.composite_images = []  # The path of a dropped image is appended.
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
            if self.holder_id and self.holder_id <= CompositeBoard.created_mask_id:
                first_img = Image.open(self.composite_images[0])
                second_img = Image.open(self.composite_images[1]).resize(first_img.size)
                mask = CompositeBoard.holder[self.holder_id].resize(first_img.size)
                self.current_img = Image.composite(first_img, second_img, mask)
                self.create_image_pil(self.current_img)
                self.display_image_size(*self.current_img.size)
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
                self.create_image_pil(self.current_img)
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
