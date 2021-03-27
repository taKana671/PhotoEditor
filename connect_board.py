import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import messagebox

import numpy as np
from TkinterDnD2 import *

from base_board import BaseBoard, InvalidSizeError


class EditorBoard(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.create_variables()
        self.create_ui()

    def create_variables(self):
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.col_var = tk.StringVar()
        self.row_var = tk.StringVar()
        self.radio_bool = tk.BooleanVar()

    def create_ui(self):
        base_frame = tk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        self.create_original_image_canvas(base_frame)
        self.create_connected_image_canvas(base_frame)
        self.create_controller(base_frame)

    def create_original_image_canvas(self, base_frame):
        self.original_image_canvas = OriginalImageCanvas(base_frame)
        self.original_image_canvas.grid(row=0, column=0, padx=(5, 1),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
           
    def create_connected_image_canvas(self, base_frame):
        self.connected_image_canvas = ConnectedImageCanvas(base_frame, self.width_var,
            self.height_var, self.col_var, self.row_var, self.radio_bool)
        self.connected_image_canvas.grid(row=0, column=1, padx=(1, 5),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(row=1, column=0, columnspan=2, 
            sticky=(tk.W, tk.E, tk.N, tk.S))
        # save image
        height_entry = ttk.Entry(controller_frame, width=10, textvariable=self.height_var)
        height_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
        height_label = ttk.Label(controller_frame, text='H:')
        height_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        width_entry = ttk.Entry(controller_frame, width=10, textvariable=self.width_var)
        width_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        width_label = ttk.Label(controller_frame, text='W:')
        width_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        save_button = ttk.Button(controller_frame, text='Save', 
            command=self.connected_image_canvas.save_with_pil)
        save_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(10, 1))
        # repeat the same image
        height_entry = ttk.Entry(
            controller_frame, width=5, textvariable=self.row_var)
        height_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 10))
        height_label = ttk.Label(controller_frame, text='x')
        height_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        width_entry = ttk.Entry(
            controller_frame, width=5, textvariable=self.col_var)
        width_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(5, 1))
        concat_repeat_button = ttk.Button(controller_frame, text='Repeat', 
            command=self.connected_image_canvas.show_concat_repeat_image)
        concat_repeat_button.pack(side=tk.RIGHT, pady=(3, 10))
        self.row_var.set(3)
        self.col_var.set(4)
        # connect image
        vertical_radio = ttk.Radiobutton(
            controller_frame, text='Vertical', value=False, variable=self.radio_bool)
        vertical_radio.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 10))
        horizontal_radio = ttk.Radiobutton(
            controller_frame, text='Horizontal', value=True, variable=self.radio_bool)
        horizontal_radio.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        reset_button = ttk.Button(controller_frame, text='Reset', 
            command=self.connected_image_canvas.reset_image)
        reset_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        concat_button = ttk.Button(controller_frame, text='Connect', 
            command=self.connected_image_canvas.show_concat_image)
        concat_button.pack(side=tk.RIGHT, pady=(3, 10))
        self.radio_bool.set(True)
        # change original images
        change_button = ttk.Button(controller_frame, text='Change', 
            command=self.original_image_canvas.change_images)
        change_button.pack(side=tk.LEFT, pady=(3, 10), padx=(5, 1))
        # clear original images
        clear_button = ttk.Button(controller_frame, text='Clear', 
            command=self.original_image_canvas.clear_images)
        clear_button.pack(side=tk.LEFT, pady=(3, 10), padx=1)


class ConnectBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)


class OriginalImageCanvas(ConnectBoard):

    def __init__(self, master):
        super().__init__(master)
        self.path_list = [] 
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

    def change_images(self):
        if len(self.path_list):
            index = self.path_list.index(self.img_path.as_posix())
            if index == len(self.path_list) - 1:
                index = 0
            else:
                index += 1
            self.show_image(self.path_list[index])

    def clear_images(self):
        self.delete('all')
        self.path_list = []
        self.img_path = None
        self.last_img = None
        self.current_img = None

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
        if event.data not in self.path_list:
            self.path_list.append(event.data)
        self.show_image(event.data)
        BaseBoard.drag_start = False
       
    def drag_init(self, event):
        print(f'Drag_start: {event.widget}')
        BaseBoard.drag_start = True
        data = (self.img_path, )
        return((ASK, COPY), (DND_FILES), data)

    def drag_end(self, event):
        print(f'Drag_ended: {event.widget}')

    def close(self):
        self.quit()


class ConnectedImageCanvas(ConnectBoard):

    def __init__(self, master, width_var, height_var, col_var, row_var, radio_bool):
        super().__init__(master, width_var, height_var)
        self.col_var = col_var
        self.row_var = row_var
        self.radio_bool = radio_bool
        self.create_bind()
        self.concat_imgs = []

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def reset_image(self):
        self.delete('all')
        self.concat_imgs = []
        self.img_path = None
        self.current_img = None

    def concat_horizontally_repeat(self, img, col):
        base = Image.new('RGB', (img.width * col, img.height))
        for x in range(col):
            base.paste(img, (x * img.width, 0))
        return base

    def concat_vertically_repeat(self, img, row):
        base = Image.new('RGB', (img.width, img.height * row))
        for y in range(row):
            base.paste(img, (0, y * img.height))
        return base
    
    def show_concat_repeat_image(self):
        try:
            col = int(self.col_var.get())
            row = int(self.row_var.get())
            if not col or not row:
                raise InvalidSizeError('Value of column or row is invalid.')
            img = self.current_img.resize((self.current_img.width//col, self.current_img.height//row))
            base_h = self.concat_horizontally_repeat(img, col)
            self.current_img = self.concat_vertically_repeat(base_h, row)
            self.display_img = ImageTk.PhotoImage(self.current_img.resize((600, 500)))
            self.delete('all')
            self.create_image(0, 0, image=self.display_img, anchor=tk.NW)
            self.display_image_size(*self.current_img.size)
        except Exception as e:
            messagebox.showerror('Error', e)
    
    def concat_vertically(self, resample=Image.BICUBIC):
        min_width = min(img.width for img in self.concat_imgs)
        resized_imgs = [img.resize(
            (min_width, int(img.height * min_width / img.width)), resample=resample) for img in self.concat_imgs]
        total_height = sum(img.height for img in resized_imgs)
        base = Image.new('RGB', (min_width, total_height))
        pos_y = 0
        for img in resized_imgs:
            base.paste(img, (0, pos_y))
            pos_y += img.height
        return base
    
    def concat_horizontally(self, resample=Image.BICUBIC):
        min_height = min(img.height for img in self.concat_imgs)
        resized_imgs = [img.resize(
            (int(img.width * min_height / img.height), min_height), resample=resample) for img in self.concat_imgs]
        total_width = sum(img.width for img in resized_imgs)
        base = Image.new('RGB', (total_width, min_height))
        pos_x = 0
        for img in resized_imgs:
            base.paste(img, (pos_x, 0))
            pos_x += img.width
        return base

    def show_concat_image(self):
        if self.concat_imgs:
            if self.radio_bool.get():
                self.current_img = self.concat_horizontally()
            else:
                self.current_img = self.concat_vertically()
            self.display_img = ImageTk.PhotoImage(self.current_img.resize((600, 500)))
            self.delete('all')
            self.create_image(0, 0, image=self.display_img, anchor=tk.NW)
            self.display_image_size(*self.current_img.size) 
        
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
            self.display_image_size(*self.current_img.size)
            self.concat_imgs.append(self.current_img)
            BaseBoard.drag_start = False
      
    def close(self):
        self.quit()

