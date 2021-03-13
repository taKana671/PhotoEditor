import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from PIL import Image, ImageTk

import numpy as np
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

    def create_ui(self):
        base_frame = tk.Frame(self.master)
        base_frame.pack(fill=tk.BOTH, expand=True)
        self.create_cover_image_canvas(base_frame)
        self.create_base_image_canvas(base_frame)
        self.create_controller(base_frame)

    def create_cover_image_canvas(self, base_frame):
        self.cover_image_canvas = CoverImageCanvas(base_frame)
        self.cover_image_canvas.grid(row=0, column=0, padx=(5, 1),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
           
    def create_base_image_canvas(self, base_frame):
        self.base_image_canvas = BaseImageCanvas(
            base_frame, self.width_var, self.height_var)
        self.base_image_canvas.grid(row=0, column=1, padx=(1, 5),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(row=1, column=0, columnspan=2, 
            sticky=(tk.W, tk.E, tk.N, tk.S))
        height_entry = ttk.Entry(controller_frame, width=10, textvariable=self.height_var)
        height_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
        height_label = ttk.Label(controller_frame, text='Height:')
        height_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(5, 1))
        width_entry = ttk.Entry(controller_frame, width=10, textvariable=self.width_var)
        width_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
        width_label = ttk.Label(controller_frame, text='Width:')
        width_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(5, 1))
        save_button = ttk.Button(controller_frame, text='Save image', 
            command=self.base_image_canvas.save_image)
        save_button.pack(side=tk.RIGHT, pady=(3, 10), padx=5)
        mask_button = ttk.Button(controller_frame, text='Change mask', 
            command=self.cover_image_canvas.toggle_mask)
        mask_button.pack(side=tk.RIGHT, pady=(3, 10))


class CompositeBoard(BaseBoard):

    mask_id = 0
    mask_images = {}

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)


class CoverImageCanvas(CompositeBoard):

    def __init__(self, master):
        super().__init__(master)
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

    def get_3d_dradient(self, start_tuple, stop_tuple, is_horizontal_tuple,
            width=600, height=500):
        array = np.zeros((height, width, len(start_tuple)), dtype=np.float)
        for i, (start, stop, is_horizontal) in enumerate(zip(start_tuple, stop_tuple, is_horizontal_tuple)):
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
            array = self.get_3d_dradient(start, stop, is_horizontal)
            yield Image.fromarray(np.uint8(array)).convert('L')

    def get_mask_images(self):
        for i, image in enumerate(self.create_mask_images()):
            CompositeBoard.mask_images[i] = image

    def toggle_mask(self):
        self.counter += 1
        CompositeBoard.mask_id = self.counter % (len(CompositeBoard.mask_images))
        mask_image = CompositeBoard.mask_images[CompositeBoard.mask_id]
        self.display_img = ImageTk.PhotoImage(mask_image)
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)

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

    def close(self):
        self.quit()


class BaseImageCanvas(CompositeBoard):

    def __init__(self, master, width_var, height_var):
        super().__init__(master, width_var, height_var)
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def show_composite_image(self, path):
        if self.current_img:
            img = Image.open(path).resize(self.current_img.size)
            mask = CompositeBoard.mask_images[CompositeBoard.mask_id].resize(
                self.current_img.size)
            self.current_img = Image.composite(self.current_img, img, mask)
            self.display_img = ImageTk.PhotoImage(self.current_img.resize((600, 500)))
            self.delete('all')
            self.create_image(0, 0, image=self.display_img, anchor=tk.NW)

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
            self.show_composite_image(event.data)
            BaseBoard.drag_start = False
        else:
            self.show_image(event.data)
            width, height = self.current_img.size
            self.width_var.set(width)
            self.height_var.set(height)
    
    def close(self):
        self.quit()

if __name__ == '__main__':
    app = TkinterDnD.Tk()
    # app.geometry('650x500')
    # app.withdraw()
    app.title('Image Editor')
    window = EditorBoard(app)
    app.protocol('WM_DELETE_WINDOW', window.close)
    app.mainloop()

