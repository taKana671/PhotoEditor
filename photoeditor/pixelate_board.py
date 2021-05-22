import math
import tkinter as tk
import tkinter.ttk as ttk
from collections import namedtuple
from functools import wraps
from pathlib import Path
from tkinter import messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
from scipy.interpolate import splrep, splev
from TkinterDnD2 import *

from base_board import BaseBoard
from board_window import BoardWindow
from config import PADY, FACE_CASCADE_PATH, EYE_CASCADE_PATH


Corner = namedtuple('Corner', 'x y')
DetectArgs = namedtuple('DetectArgs', 'scale_factor min_neighbors')


class EditorBoard(BoardWindow):

    def create_board_variables(self):
        self.ratio = tk.DoubleVar()
        self.min_neighbors = tk.IntVar()
        self.scale_factor = tk.DoubleVar()

    def create_left_canvas(self, base_frame):
        self.left_canvas = LeftCanvas(base_frame)
        self.left_canvas.grid(
            row=0, column=0, padx=(5, 1), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_right_canvas(self, base_frame):
        self.right_canvas = RightCanvas(
            base_frame, self.width_var, self.height_var, self.ratio,
            self.scale_factor, self.min_neighbors)
        self.right_canvas.grid(
            row=0, column=1, padx=(1, 5), pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_save_widgets(controller_frame, self.right_canvas.save_open_cv)
        self.create_pixelate_widgets(controller_frame)
        self.create_detect_widgets(controller_frame)
        self.create_gif_widgets(controller_frame)
        self.compare_images_widgets(controller_frame)

    def create_pixelate_widgets(self, controller_frame):
        ratio_list = [0.1, 0.05, 0.025]
        for ratio in ratio_list:
            radio = ttk.Radiobutton(
                controller_frame, text=str(ratio), value=ratio, variable=self.ratio)
            radio.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        self.ratio.set(ratio_list[0])
        entire_button = ttk.Button(
            controller_frame, text='Entire', command=self.right_canvas.show_pixelated_entire)
        entire_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        area_button = ttk.Button(
            controller_frame, text='Area', command=self.right_canvas.show_pixelated_area)
        area_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))

    def create_detect_widgets(self, controller_frame):
        min_neighbors = ttk.Entry(controller_frame, width=5, textvariable=self.min_neighbors)
        min_neighbors.pack(side=tk.RIGHT, pady=PADY, padx=(1, 20))
        neighbors_label = ttk.Label(controller_frame, text='minNeighbors:')
        neighbors_label.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        scale_factor = ttk.Entry(controller_frame, width=5, textvariable=self.scale_factor)
        scale_factor.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        factor_label = ttk.Label(controller_frame, text='scaleFactor:')
        factor_label.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        self.scale_factor.set(1.05)
        self.min_neighbors.set(2)
        face_detect_button = ttk.Button(
            controller_frame, text='Face Detect', command=self.right_canvas.detect_face)
        face_detect_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))
        eye_detect_button = ttk.Button(
            controller_frame, text='Eye Detect', command=self.right_canvas.detect_eye)
        eye_detect_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))

    def create_gif_widgets(self, controller_frame):
        gif_button = ttk.Button(
            controller_frame, text='Save Gif', command=self.right_canvas.save_gif_file)
        gif_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 20))

    def compare_images_widgets(self, controller_frame):
        compare_button = ttk.Button(
            controller_frame,
            text='Compare',
            command=lambda: self.right_canvas.compare_images(self.left_canvas.source_img))
        compare_button.pack(side=tk.RIGHT, pady=PADY, padx=(1, 1))


class PixelateBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)
        self.source_img = None

    def show_image(self, path):
        """Display an image on a canvas when the image was dropped.
        """
        self.source_img = cv2.imread(path)
        self.current_img = self.source_img.copy()
        self.img_path = Path(path)
        self.create_image_cv(self.current_img)

    def create_image_cv(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        super().create_image_cv(img_rgb)


class LeftCanvas(PixelateBoard):
    """The left canvas to show an source image.
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
    def __init__(self, master, width_var, height_var, ratio, scale_factor, min_neighbors):
        super().__init__(master, width_var, height_var)
        self.rectangle_tag = 'rect'
        self.corners = []
        self.ratio = ratio
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)
        self.bind('<ButtonPress-3>', self.start_drawing)
        self.bind('<Button3-Motion>', self.draw_rectangle)
        self.bind('<ButtonRelease-3>', self.end_drawing)

    def pixelate(self, img, ratio):
        smaller = cv2.resize(
            img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(smaller, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def show_pixelated_entire(self):
        if self.img_path:
            self.current_img = self.pixelate(self.source_img, self.ratio.get())
            self.create_image_cv(self.current_img)

    def get_current_img_corners(self, corners):
        current_h, current_w = self.current_img.shape[:2]
        display_w, display_h = self.display_img.size
        # get magnification ratio
        scale_x = current_w / display_w
        scale_y = current_h / display_h
        for corner in corners:
            yield Corner(int(corner[0] * scale_x), int(corner[1] * scale_y))

    def show_pixelated_area(self):
        if self.corners:
            left, right = self.corners
            ratio = self.ratio.get()
            self.current_img[left.y:right.y, left.x:right.x] = \
                self.pixelate(self.current_img[left.y:right.y, left.x:right.x], ratio)
            self.create_image_cv(self.current_img)
            self.clear_rectangle()

    def create_gif_image(self):
        if self.img_path:
            img = cv2.cvtColor(self.source_img, cv2.COLOR_BGR2RGB)
            imgs = [Image.fromarray(self.pixelate(img, 1 / i)) for i in range(1, 25)]
            imgs += imgs[-2::-1] + [Image.fromarray(img)] * 5
            return imgs

    def get_detect_args(self):
        return self.scale_factor.get(), self.min_neighbors.get()

    def get_faces(self, img_gray, scale_factor, min_neighbors):
        face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
        faces = face_cascade.detectMultiScale(
            img_gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)
        return faces

    def detection(func):
        @wraps(func)
        def decorator(self):
            if self.img_path:
                try:
                    func(self)
                except Exception as e:
                    messagebox.showerror('error', e)
        return decorator

    @detection
    def detect_face(self):
        scale_factor, min_neighbors = self.get_detect_args()
        img_gray = cv2.cvtColor(self.source_img, cv2.COLOR_BGR2GRAY)
        faces = self.get_faces(img_gray, scale_factor, min_neighbors)
        for x, y, w, h in faces:
            self.current_img[y: y + h, x: x + w] = self.pixelate(
                self.current_img[y: y + h, x: x + w], 0.1)
        self.create_image_cv(self.current_img)

    @detection
    def detect_eye(self):
        scale_factor, min_neighbors = self.get_detect_args()
        img_gray = cv2.cvtColor(self.source_img, cv2.COLOR_BGR2GRAY)
        faces = self.get_faces(img_gray, scale_factor, min_neighbors)
        eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_PATH)
        for x, y, h, w in faces:
            face = self.current_img[y: y + h, x: x + w]
            face_gray = img_gray[y: y + h, x: x + w]
            eyes = eye_cascade.detectMultiScale(
                face_gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)
            for ex, ey, ew, eh in eyes:
                face[ey: ey + eh, ex: ex + ew] = self.pixelate(
                    face[ey: ey + eh, ex: ex + ew], 0.1)
        self.create_image_cv(self.current_img)

    def compare_images(self, left_img):
        if left_img is not None and self.source_img is not None and \
                left_img.shape == self.source_img.shape:
            gray_img_ref = cv2.cvtColor(left_img, cv2.COLOR_BGRA2GRAY)
            gray_img_comp = cv2.cvtColor(self.source_img, cv2.COLOR_BGR2GRAY)
            img_diff = cv2.absdiff(gray_img_ref, gray_img_comp)
            _, img_bin = cv2.threshold(img_diff, 50, 255, 0)
            contours, _ = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(self.current_img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            self.create_image_cv(self.current_img)

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

    def start_drawing(self, event):
        """Get x, y at the clicked point.
        """
        if self.display_img:
            self.clear_rectangle()
            img_width, img_height = self.display_img.size
            if event.x < img_width and event.y < img_height:
                self.create_rectangle(
                    event.x, event.y, event.x, event.y, outline='white', tag=self.rectangle_tag)
                self.start_x = event.x
                self.start_y = event.y

    def draw_rectangle(self, event):
        """Draw rectangle.
        """
        if self.display_img:
            img_width, img_height = self.display_img.size
            end_x = min(img_width, event.x)
            end_y = min(img_height, event.y)
            self.coords(
                self.rectangle_tag, self.start_x, self.start_y, end_x, end_y)

    def end_drawing(self, event):
        """Get the left top and right bottom of the rectangle.
        """
        if self.display_img:
            left_top_x, left_top_y, right_bottom_x, right_bottom_y = \
                self.coords(self.rectangle_tag)
            self.corners = [corner for corner in self.get_current_img_corners(
                [(left_top_x, left_top_y), (right_bottom_x, right_bottom_y)])]

    def clear_rectangle(self):
        """Delete rectangle.
        """
        self.delete(self.rectangle_tag)
        self.corners = []
