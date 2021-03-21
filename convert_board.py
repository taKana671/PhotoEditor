import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from PIL import Image, ImageTk

import cv2
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
        self.create_original_image_canvas(base_frame)
        self.create_convert_image_canvas(base_frame)
        self.create_controller(base_frame)

    def create_original_image_canvas(self, base_frame):
        self.original_image_canvas = OriginalImageCanvas(base_frame)
        self.original_image_canvas.grid(row=0, column=0, padx=(5, 1),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
           
    def create_convert_image_canvas(self, base_frame):
        self.convert_image_canvas = ConvertImageCanvas(
            base_frame, self.width_var, self.height_var)
        self.convert_image_canvas.grid(row=0, column=1, padx=(1, 5),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(row=1, column=0, columnspan=2, 
            sticky=(tk.W, tk.E, tk.N, tk.S))
        height_entry = ttk.Entry(controller_frame, width=10, textvariable=self.height_var)
        height_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
        height_label = ttk.Label(controller_frame, text='H:')
        height_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(5, 1))
        width_entry = ttk.Entry(controller_frame, width=10, textvariable=self.width_var)
        width_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
        width_label = ttk.Label(controller_frame, text='W:')
        width_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(5, 1))
        save_button = ttk.Button(controller_frame, text='Save image', 
            command=self.convert_image_canvas.save_image)
        save_button.pack(side=tk.RIGHT, pady=(3, 10), padx=5)
        mask_button = ttk.Button(controller_frame, text='Gray scale', 
            command=self.convert_image_canvas.show_gray_image)
        mask_button.pack(side=tk.RIGHT, pady=(3, 10))


class ConvertBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None):
        super().__init__(master, width_var, height_var)

    def show_image(self, path):
        self.current_img = cv2.imread(path)
        self.img_path = Path(path)
        img_rgb  = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        self.display_img = ImageTk.PhotoImage(img_pil.resize((600, 500)))
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)


class OriginalImageCanvas(ConvertBoard):

    def __init__(self, master):
        super().__init__(master)
        # self.get_mask_images()
        self.create_bind()
        # self.counter = 0

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

    def close(self):
        self.quit()


class ConvertImageCanvas(ConvertBoard):

    def __init__(self, master, width_var, height_var):
        super().__init__(master, width_var, height_var)
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)

    def show_gray_image(self):
        img_gray = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2GRAY)
        img_pil = Image.fromarray(img_gray)
        self.display_img = ImageTk.PhotoImage(img_pil.resize((600, 500)))
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
            self.show_image(event.data)
            self.display_image_size(*self.current_img.shape[:-1])
            BaseBoard.drag_start = False
    
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

