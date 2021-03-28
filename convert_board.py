import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageTk
from scipy.interpolate import splrep, splev
from TkinterDnD2 import *

from base_board import BaseBoard


class EditorBoard(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.create_variables()
        self.create_ui()

    def create_variables(self):
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.noise_bool = tk.BooleanVar()
        self.light_bool = tk.BooleanVar()
        self.contrast_bool = tk.BooleanVar()
        self.angle_int = tk.IntVar()
        self.scale_double = tk.DoubleVar()

    def create_ui(self):
        base_frame = tk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        self.create_original_image_canvas(base_frame)
        self.create_convert_image_canvas(base_frame)
        self.create_controller(base_frame)

    def create_original_image_canvas(self, base_frame):
        self.original_image_canvas = OriginalImageCanvas(base_frame)
        self.original_image_canvas.grid(row=0, column=0, padx=(5, 1),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
           
    def create_convert_image_canvas(self, base_frame):
        self.convert_image_canvas = ConvertImageCanvas(base_frame,
            self.width_var, self.height_var, self.noise_bool, self.light_bool, 
            self.contrast_bool, self.scale_double, self.angle_int)
        self.convert_image_canvas.grid(row=0, column=1, padx=(1, 5),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(row=1, column=0, columnspan=2, 
            sticky=(tk.W, tk.E, tk.N, tk.S))
        # save
        height_entry = ttk.Entry(controller_frame, width=10, textvariable=self.height_var)
        height_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
        height_label = ttk.Label(controller_frame, text='H:')
        height_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        width_entry = ttk.Entry(controller_frame, width=10, textvariable=self.width_var)
        width_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        width_label = ttk.Label(controller_frame, text='W:')
        width_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        save_button = ttk.Button(controller_frame, text='Save image', 
            command=self.convert_image_canvas.save_open_cv)
        save_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(10, 1))
        # gray
        gray_button = ttk.Button(controller_frame, text='Gray', 
            command=self.convert_image_canvas.show_gray_image)
        # sepia
        gray_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(10, 1))
        check_noise = ttk.Checkbutton(controller_frame, text='Noise', variable=self.noise_bool,
            onvalue=True, offvalue=False)
        check_noise.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        check_contrast = ttk.Checkbutton(controller_frame, text='Contrast', variable=self.contrast_bool,
            onvalue=True, offvalue=False)
        check_contrast.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        check_light = ttk.Checkbutton(controller_frame, text='Light', variable=self.light_bool,
            onvalue=True, offvalue=False)
        check_light.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        sepia_button = ttk.Button(controller_frame, text='Sepia', 
            command=self.convert_image_canvas.show_sepia_image)
        sepia_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(10, 1))
        # image like animation
        anime_button = ttk.Button(controller_frame, text='Anime', 
            command=self.convert_image_canvas.show_image_like_animation)
        anime_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(10, 1))
        # image like pixel art
        pixel_button = ttk.Button(controller_frame, text='Pixel', 
            command=self.convert_image_canvas.show_pixel_art)
        pixel_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(10, 1))
        # rotate
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
        repeat_button = ttk.Button(controller_frame, text='Repeat', 
            command=self.convert_image_canvas.show_repeated_image)
        repeat_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        rotate_button = ttk.Button(controller_frame, text='Rotate', 
            command=self.convert_image_canvas.show_rotated_image)
        rotate_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(10, 1))


class ConvertBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)

    def show_image(self, path):
        self.current_img = cv2.imread(path)
        self.img_path = Path(path)
        img_rgb  = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        self.create_photo_image(img_rgb)
        
    def create_photo_image(self, img_rgb):
        nw, nh = self.get_cv_aspect()
        img_pil = Image.fromarray(img_rgb)
        self.display_img = ImageTk.PhotoImage(img_pil.resize((nw, nh)))
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)


class OriginalImageCanvas(ConvertBoard):

    def __init__(self, master):
        super().__init__(master)
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
        self.show_image(event.data)
        self.drag_start = False
       
    def drag_init(self, event):
        print(f'Drag_start: {event.widget}')
        BaseBoard.drag_start = True
        data = (self.img_path, )
        return((ASK, COPY), (DND_FILES), data)

    def drag_end(self, event):
        print(f'Drag_ended: {event.widget}')


class ConvertImageCanvas(ConvertBoard):

    def __init__(self, master, width_var, height_var, noise_bool,
                 light_bool, contrast_bool, scale_double, angle_int):
        super().__init__(master, width_var, height_var)
        self.noise_bool = noise_bool
        self.light_bool = light_bool
        self.contrast_bool = contrast_bool
        self.scale_double = scale_double
        self.angle_int = angle_int
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def show_gray_image(self):
        """Display gray image.
        """
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
        """Display sepia image.
        """
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
        ret, label, center = cv2.kmeans(z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        return res.reshape((img.shape))

    def show_pixel_art(self, alpha=2, k=4):
        if self.img_path:
            img = cv2.imread(self.img_path.as_posix())
            h, w, ch = img.shape
            img = cv2.resize(img, (int(w*alpha), int(h*alpha)))
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
    
    def show_repeated_image(self):
        if self.img_path:
            scale, angle = self.get_scale_and_angle()
            if scale is not None and angle is not None:
                img = cv2.imread(self.img_path.as_posix())
                h, w, ch = img.shape
                mat = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
                self.current_img = cv2.warpAffine(img, mat, (w, h), borderMode=cv2.BORDER_WRAP)
                img_rgb = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
                self.create_photo_image(img_rgb)

    def show_rotated_image(self):
        if self.img_path:
            scale, angle = self.get_scale_and_angle()
            if scale is not None and angle is not None:
                img = cv2.imread(self.img_path.as_posix())
                dst = img // 4
                h, w, ch = img.shape
                mat = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
                self.current_img = cv2.warpAffine(img, mat, (w, h), borderMode=cv2.BORDER_TRANSPARENT, dst=dst)
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
        print('Dropped:', event.widget)
        if BaseBoard.drag_start:
            self.show_image(event.data)
            self.display_image_size(*self.current_img.shape[:-1])
            BaseBoard.drag_start = False


if __name__ == '__main__':
    app = TkinterDnD.Tk()
    # app.geometry('650x500')
    # app.withdraw()
    app.title('Image Editor')
    window = EditorBoard(app)
    app.protocol('WM_DELETE_WINDOW', window.close)
    app.mainloop()

