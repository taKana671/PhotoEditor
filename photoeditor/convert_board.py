import math
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageTk
from scipy.interpolate import splrep, splev
from TkinterDnD2 import *

from base_board import BaseBoard
from board_window import BoardWindow


class EditorBoard(BoardWindow):

    def create_board_variables(self):
        self.noise_bool = tk.BooleanVar()
        self.light_bool = tk.BooleanVar()
        self.contrast_bool = tk.BooleanVar()
        self.angle_int = tk.IntVar()
        self.scale_double = tk.DoubleVar()
        self.xy_bool = tk.BooleanVar()

    def create_left_canvas(self, base_frame):
        self.left_canvas = LeftCanvas(base_frame)
        self.left_canvas.grid(
            row=0, column=0, padx=(5, 1), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_right_canvas(self, base_frame):
        self.right_canvas = RightCanvas(
            base_frame, self.width_var, self.height_var, self.noise_bool, self.light_bool,
            self.contrast_bool, self.scale_double, self.angle_int, self.xy_bool)
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
        check_noise = ttk.Checkbutton(
            controller_frame, text='Noise', variable=self.noise_bool, onvalue=True, offvalue=False)
        check_noise.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        check_contrast = ttk.Checkbutton(
            controller_frame, text='Contrast', variable=self.contrast_bool, onvalue=True, offvalue=False)
        check_contrast.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        check_light = ttk.Checkbutton(
            controller_frame, text='Light', variable=self.light_bool, onvalue=True, offvalue=False)
        check_light.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        sepia_button = ttk.Button(
            controller_frame, text='Sepia', command=self.right_canvas.show_sepia_image)
        sepia_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(20, 1))

    def create_convert_widgets(self, controller_frame):
        # gray
        gray_button = ttk.Button(
            controller_frame, text='Gray', command=self.right_canvas.show_gray_image)
        gray_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        # image like animation
        anime_button = ttk.Button(
            controller_frame, text='Anime', command=self.right_canvas.show_image_like_animation)
        anime_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        # image like pixel art
        pixel_button = ttk.Button(
            controller_frame, text='Pixel', command=self.right_canvas.show_pixel_art)
        pixel_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(20, 1))

    def change_mode_widgets(self, controller_frame):
        scale_entry = ttk.Entry(controller_frame, width=5, textvariable=self.scale_double)
        scale_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        scale_label = ttk.Label(controller_frame, text='Scale')
        scale_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        angle_entry = ttk.Entry(controller_frame, width=5, textvariable=self.angle_int)
        angle_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        angle_label = ttk.Label(controller_frame, text='Angle')
        angle_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        self.scale_double.set(0.5)
        self.angle_int.set(45)
        repeat_button = ttk.Button(
            controller_frame, text='Change Mode', command=self.right_canvas.change_border_mode)
        repeat_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))

    def create_skew_widgets(self, controller_frame):
        y_radio = ttk.Radiobutton(
            controller_frame, text='Y', value=False, variable=self.xy_bool)
        y_radio.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 10))
        x_radio = ttk.Radiobutton(
            controller_frame, text='X', value=True, variable=self.xy_bool)
        x_radio.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        skew_button = ttk.Button(
            controller_frame, text='Skew', command=self.right_canvas.show_skewed_image)
        skew_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        self.xy_bool.set(True)


class ConvertBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)

    def show_image(self, path):
        """Display an image on a canvas when the image was dropped.
        """
        self.delete('all')
        self.current_img = cv2.imread(path)
        self.img_path = Path(path)
        img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_photo_image(img_rgb)

    def create_photo_image(self, img_rgb):
        h, w = self.current_img.shape[:2]
        img_pil = Image.fromarray(img_rgb)
        if w <= 600 and h <= 500:
            self.display_img = ImageTk.PhotoImage(img_pil)
        else:
            nw, nh = self.get_cv_aspect()
            self.display_img = ImageTk.PhotoImage(img_pil.resize((nw, nh)))
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)


class LeftCanvas(ConvertBoard):
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
            self.show_border_transparent,
            lambda mode=cv2.BORDER_CONSTANT: self.show_geometric_image(mode),
            lambda mode=cv2.BORDER_REPLICATE: self.show_geometric_image(mode),
            lambda mode=cv2.BORDER_REFLECT: self.show_geometric_image(mode),
            lambda mode=cv2.BORDER_WRAP: self.show_geometric_image(mode),
            lambda mode=cv2.BORDER_REFLECT_101: self.show_geometric_image(mode),
        ]
        self.mode_id = -1
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def show_gray_image(self):
        if self.img_path:
            img = cv2.imread(self.img_path.as_posix())
            self.current_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.create_photo_image(self.current_img)

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

    def show_sepia_image(self):
        if self.img_path:
            img = cv2.imread(self.img_path.as_posix())
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if self.noise_bool.get():
                gray = self.superimpose_noise(gray)
            if self.contrast_bool.get():
                gray = self.enhance_contrast(gray)
            if self.light_bool.get():
                gray = self.correct_peripheral_light(gray, -0.4).astype(np.uint8)
            img_hsv = np.zeros_like(img)
            img_hsv[:, :, 0] = np.full_like(img_hsv[:, :, 0], 15, dtype=np.uint8)
            img_hsv[:, :, 1] = np.full_like(img_hsv[:, :, 1], 153, dtype=np.uint8)
            img_hsv[:, :, 2] = gray
            self.current_img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
            img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
            self.create_photo_image(img_rgb)

    def show_image_like_animation(self, k=30):
        if self.img_path:
            img = cv2.imread(self.img_path.as_posix())
            gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            edge = cv2.blur(gray, (3, 3))
            edge = cv2.Canny(edge, 50, 150, apertureSize=3)
            edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
            img = cv2.pyrMeanShiftFiltering(img, 5, 20)
            self.current_img = cv2.subtract(img, edge)
            img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
            self.create_photo_image(img_rgb)

    def sub_color(self, img, k):
        z = img.reshape((-1, 3))
        z = np.float32(z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, label, center = cv2.kmeans(z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        return res.reshape((img.shape))

    def show_pixel_art(self, alpha=2, k=4):
        if self.img_path:
            img = cv2.imread(self.img_path.as_posix())
            h, w, _ = img.shape
            img = cv2.resize(img, (int(w * alpha), int(h * alpha)))
            img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)
            self.current_img = self.sub_color(img, k)
            img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
            self.create_photo_image(img_rgb)

    def get_scale_and_angle(self):
        try:
            scale = self.scale_double.get()
            angle = self.angle_int.get()
        except Exception:
            return None, None
        else:
            return scale, angle

    def change_border_mode(self):
        self.mode_id += 1
        if self.mode_id >= len(self.modes):
            self.mode_id = 0
        func = self.modes[self.mode_id]
        func()

    def show_border_transparent(self):
        if self.img_path:
            scale, angle = self.get_scale_and_angle()
            if scale is not None and angle is not None:
                img = cv2.imread(self.img_path.as_posix())
                dst = img // 4
                h, w, _ = img.shape
                mat = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
                self.current_img = cv2.warpAffine(
                    img, mat, (w, h), borderMode=cv2.BORDER_TRANSPARENT, dst=dst)
                img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
                self.create_photo_image(img_rgb)

    def show_geometric_image(self, mode):
        if self.img_path:
            scale, angle = self.get_scale_and_angle()
            if scale is not None and angle is not None:
                img = cv2.imread(self.img_path.as_posix())
                h, w, _ = img.shape
                mat = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
                self.current_img = cv2.warpAffine(
                    img, mat, (w, h), borderMode=mode)
                img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
                self.create_photo_image(img_rgb)

    def get_skew_angle(self):
        self.skew_angle_id += 1
        if self.skew_angle_id >= len(self.skew_angles):
            self.skew_angle_id = 0
        return self.skew_angles[self.skew_angle_id]

    def show_skewed_image(self):
        if self.img_path:
            skew_angle = self.get_skew_angle()
            img = cv2.imread(self.img_path.as_posix())
            angle = math.tan(math.radians(skew_angle))
            h, w, _ = img.shape
            if self.xy_bool.get():
                mat = np.array([[1, angle, 0], [0, 1, 0]], dtype=np.float32)
                self.current_img = cv2.warpAffine(img, mat, (int(w + h * angle), h))
            else:
                mat = np.array([[1, 0, 0], [angle, 1, 0]], dtype=np.float32)
                self.current_img = cv2.warpAffine(img, mat, (w, int(h + w * angle)))
            img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
            self.create_photo_image(img_rgb)

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
            self.display_image_size(*self.current_img.shape[:-1])
            BaseBoard.drag_start = False
