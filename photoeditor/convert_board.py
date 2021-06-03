import math
import tkinter as tk
import tkinter.ttk as ttk
from functools import wraps
from pathlib import Path
from tkinter import messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
from scipy.interpolate import splrep, splev
from TkinterDnD2 import *

from base_board import BaseBoard, NoImageOnTheCanvasError
from board_window import BoardWindow
from config import PADY, PADX, ERROR, RIGHT_CANVAS_MSG_1


class EditorBoard(BoardWindow):

    def create_board_variables(self):
        self.noise = tk.BooleanVar()
        self.light = tk.BooleanVar()
        self.contrast = tk.BooleanVar()
        self.angle_int = tk.IntVar()
        self.scale_double = tk.DoubleVar()
        self.xy_bool = tk.BooleanVar()

    def create_left_canvas(self, base_frame):
        self.left_canvas = LeftCanvas(base_frame)
        self.left_canvas.grid(
            row=0, column=0, padx=(5, 1), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_right_canvas(self, base_frame):
        self.right_canvas = RightCanvas(
            base_frame, self.width_var, self.height_var, self.noise, self.light,
            self.contrast, self.scale_double, self.angle_int, self.xy_bool)
        self.right_canvas.grid(
            row=0, column=1, padx=(1, 5), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_save_widgets(controller_frame, self.right_canvas.save_open_cv)
        self.create_sepia_widgets(controller_frame)
        self.create_convert_widgets(controller_frame)
        self.change_mode_widgets(controller_frame)
        self.create_skew_widgets(controller_frame)

    def create_sepia_widgets(self, controller_frame):
        # sepia
        for text, variable in zip(['Noise', 'Contrast', 'Light'], [self.noise, self.contrast, self.light]):
            check = ttk.Checkbutton(
                controller_frame, text=text, variable=variable, onvalue=True, offvalue=False)
            check.pack(side=tk.RIGHT, pady=PADY, padx=PADX)
        sepia_button = ttk.Button(
            controller_frame, text='Sepia', command=self.right_canvas.show_sepia_image)
        sepia_button.pack(side=tk.RIGHT, pady=PADY, padx=(20, 1))

    def create_convert_widgets(self, controller_frame):
        # gray
        gray_button = ttk.Button(
            controller_frame, text='Gray', command=self.right_canvas.show_gray_image)
        gray_button.pack(side=tk.RIGHT, pady=PADY, padx=PADX)
        # image like animation
        anime_button = ttk.Button(
            controller_frame, text='Anime', command=self.right_canvas.show_image_like_animation)
        anime_button.pack(side=tk.RIGHT, pady=PADY, padx=PADX)
        # image like pixel art
        pixel_button = ttk.Button(
            controller_frame, text='Pixel', command=self.right_canvas.show_pixel_art)
        pixel_button.pack(side=tk.RIGHT, pady=PADY, padx=(20, 1))

    def change_mode_widgets(self, controller_frame):
        # change BorderMode
        for variable, text in zip([self.scale_double, self.angle_int], ['Scale', 'Angle']):
            entry = ttk.Entry(controller_frame, width=5, textvariable=variable)
            entry.pack(side=tk.RIGHT, pady=PADY, padx=PADX)
            label = ttk.Label(controller_frame, text=text)
            label.pack(side=tk.RIGHT, pady=PADY, padx=PADX)
        self.scale_double.set(0.5)
        self.angle_int.set(45)
        geometric_button = ttk.Button(
            controller_frame, text='Geometric', command=self.right_canvas.show_geometric_image)
        geometric_button.pack(side=tk.RIGHT, pady=PADY, padx=(10, 1))

    def create_skew_widgets(self, controller_frame):
        for text, value in zip(['Y', 'X'], [False, True]):
            radio = ttk.Radiobutton(
                controller_frame, text=text, value=value, variable=self.xy_bool)
            radio.pack(side=tk.RIGHT, pady=PADY, padx=PADX)
        skew_button = ttk.Button(
            controller_frame, text='Skew', command=self.right_canvas.show_skewed_image)
        skew_button.pack(side=tk.RIGHT, pady=PADY, padx=PADX)
        self.xy_bool.set(True)


class ConvertBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)
        self.source_img = None

    def show_image(self, path):
        """Display an image on a canvas when the image was dropped.
        """
        self.source_img = cv2.imread(path)
        self.current_img = self.source_img.copy()
        self.img_path = Path(path)
        img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_image_cv(img_rgb)


class LeftCanvas(ConvertBoard):
    """The left canvas to show a source image.
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


class RightCanvas(ConvertBoard):
    """The right canvas to show a converted image.
    """
    def __init__(self, master, width_var, height_var, noise_bool,
                 light_bool, contrast_bool, scale_double, angle_int, xy_bool):
        super().__init__(master, width_var, height_var)
        self.noise_bool = noise_bool
        self.light_bool = light_bool
        self.contrast_bool = contrast_bool
        self.scale_double = scale_double
        self.angle_int = angle_int
        self.xy_bool = xy_bool
        self.img_path = None
        self.skew_angles = [15, 30, 45]
        self.skew_angle_id = -1
        self.modes = [
            dict(borderMode=cv2.BORDER_TRANSPARENT, dst=None),
            dict(borderMode=cv2.BORDER_CONSTANT),
            dict(borderMode=cv2.BORDER_REPLICATE),
            dict(borderMode=cv2.BORDER_REFLECT),
            dict(borderMode=cv2.BORDER_WRAP),
            dict(borderMode=cv2.BORDER_REFLECT_101)]
        self.mode_id = -1
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def conversion(convert_func):
        @wraps(convert_func)
        def _conversion(self, *args, **kwargs):
            try:
                if not self.img_path:
                    raise NoImageOnTheCanvasError(RIGHT_CANVAS_MSG_1)
                convert_func(self, *args, **kwargs)
            except Exception as e:
                messagebox.showerror(ERROR, e)
        return _conversion

    @conversion
    def show_gray_image(self):
        self.current_img = cv2.cvtColor(self.source_img, cv2.COLOR_BGR2GRAY)
        self.create_image_cv(self.current_img)
        self.display_image_size(*self.current_img.shape[::-1])

    def correct_peripheral_light(self, img, gain_params):
        h, w = img.shape[:2]
        size = max([h, w])
        x = np.linspace(-w / size, w / size, w)
        y = np.linspace(-h / size, h / size, h)
        xx, yy = np.meshgrid(x, y)
        r = np.sqrt(xx ** 2 + yy ** 2)
        gainmap = gain_params * r + 1
        return np.clip(img * gainmap, 0., 255)

    def superimpose_noise(self, gray):
        h, w = gray.shape
        gauss = np.random.normal(0, 40, (h, w)).reshape(h, w)
        return np.clip(gray + gauss, 0, 255).astype(np.uint8)

    def enhance_contrast(self, gray):
        xs = [0, 0.25, 0.5, 0.75, 1]
        ys = [0, 0.15, 0.5, 0.85, 0.99]
        tck = splrep(xs, ys)
        return splev(gray / 255, tck) * 255

    @conversion
    def show_sepia_image(self):
        gray = cv2.cvtColor(self.source_img, cv2.COLOR_BGR2GRAY)
        if self.noise_bool.get():
            gray = self.superimpose_noise(gray)
        if self.contrast_bool.get():
            gray = self.enhance_contrast(gray)
        if self.light_bool.get():
            gray = self.correct_peripheral_light(gray, -0.4).astype(np.uint8)
        img_hsv = np.zeros_like(self.source_img)
        img_hsv[:, :, 0] = np.full_like(img_hsv[:, :, 0], 15, dtype=np.uint8)
        img_hsv[:, :, 1] = np.full_like(img_hsv[:, :, 1], 153, dtype=np.uint8)
        img_hsv[:, :, 2] = gray
        self.current_img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
        self.create_image_cv(img_rgb)
        self.display_image_size(*self.current_img.shape[:-1][::-1])

    @conversion
    def show_image_like_animation(self, k=30):
        gray = cv2.cvtColor(self.source_img, cv2.COLOR_BGRA2GRAY)
        edge = cv2.blur(gray, (3, 3))
        edge = cv2.Canny(edge, 50, 150, apertureSize=3)
        edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
        img = cv2.pyrMeanShiftFiltering(self.source_img, 5, 20)
        self.current_img = cv2.subtract(img, edge)
        img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_image_cv(img_rgb)
        self.display_image_size(*self.current_img.shape[:-1][::-1])

    def sub_color(self, img, k):
        z = img.reshape((-1, 3))
        z = np.float32(z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, label, center = cv2.kmeans(z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        return res.reshape((img.shape))

    @conversion
    def show_pixel_art(self, alpha=2, k=4):
        h, w, _ = self.source_img.shape
        img = cv2.resize(self.source_img, (int(w * alpha), int(h * alpha)))
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)
        self.current_img = self.sub_color(img, k)
        img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_image_cv(img_rgb)
        self.display_image_size(*self.current_img.shape[:-1][::-1])

    def get_border_mode(self):
        self.mode_id += 1
        if self.mode_id >= len(self.modes):
            self.mode_id = 0
        return self.modes[self.mode_id]

    @conversion
    def show_geometric_image(self):
        scale = self.scale_double.get()
        angle = self.angle_int.get()
        args = self.get_border_mode()
        if 'dst' in args:
            args['dst'] = self.source_img // 4
        h, w, _ = self.source_img.shape
        mat = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
        self.current_img = cv2.warpAffine(
            self.source_img, mat, (w, h), **args)
        img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_image_cv(img_rgb)
        self.display_image_size(*self.current_img.shape[:-1][::-1])

    def get_skew_angle(self):
        self.skew_angle_id += 1
        if self.skew_angle_id >= len(self.skew_angles):
            self.skew_angle_id = 0
        return self.skew_angles[self.skew_angle_id]

    @conversion
    def show_skewed_image(self):
        skew_angle = self.get_skew_angle()
        angle = math.tan(math.radians(skew_angle))
        h, w, _ = self.source_img.shape
        if self.xy_bool.get():
            mat = np.array([[1, angle, 0], [0, 1, 0]], dtype=np.float32)
            self.current_img = cv2.warpAffine(self.source_img, mat, (int(w + h * angle), h))
        else:
            mat = np.array([[1, 0, 0], [angle, 1, 0]], dtype=np.float32)
            self.current_img = cv2.warpAffine(self.source_img, mat, (w, int(h + w * angle)))
        img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_image_cv(img_rgb)
        self.display_image_size(*self.current_img.shape[:-1][::-1])

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
        """Display image, only when the imaged was
           dragged from the left canvas.
        """
        print('Dropped:', event.widget)
        if BaseBoard.drag_start:
            self.skew_angle_id = -1
            self.show_image(event.data)
            self.display_image_size(*self.current_img.shape[:-1][::-1])
            BaseBoard.drag_start = False
