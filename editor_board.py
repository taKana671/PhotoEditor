import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk

from pathlib import Path

from TkinterDnD2 import *


class CompositeBoard(tk.Canvas):

    drag_start = False

    def __init__(self, master):
        self.img_path = ''
        super().__init__(master, width=600, height=500, bg='snow')
     
      
class CoverImageCanvas(CompositeBoard):

    def __init__(self, master):
        super().__init__(master)
        self.mask_images = {}
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

    def show_image(self, path):
        img = Image.open(path)
        self.img_path = Path(path)
        self.display_img = ImageTk.PhotoImage(img.resize((600, 500)))
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)

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
        params = [
            [(255, 255, 255), (0, 0, 0), (False, False, False)],
            [(0, 0, 0), (255, 255, 255), (False, False, False)],
            [(255, 255, 255), (0, 0, 0), (True, True, True)],
            [(0, 0, 0), (255, 255, 255), (True, True, True)],
            [(0, 0, 192), (255, 255, 64), (True, False, False)]
        ]
        for i, param in enumerate(params):
            start, stop, is_horizontal = param
            array = self.get_3d_dradient(start, stop, is_horizontal)
            self.mask_images[i] = Image.fromarray((np.uint8(array)))

    def toggle_mask(self):
        pass

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
        CompositeBoard.drag_start = True
        data = (self.img_path, )
        return((ASK, COPY), (DND_FILES), data)

    def drag_end(self, event):
        print(f'Drag_ended: {event.widget}')

    def close(self):
        self.quit()


class BaseImageCanvas(CompositeBoard):

    def __init__(self, master):
        super().__init__(master)
        self.original_img = None
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        # self.drag_source_register(1, DND_TEXT, DND_FILES)
        # self.drag_source_register(1, '*')
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)
        
    def show_image(self, path):
        self.original_img = Image.open(path)
        self.img_path = Path(path)
        self.display_img = ImageTk.PhotoImage(self.original_img.resize((600, 500)))
        self.create_image(0, 0, image=self.display_img, anchor=tk.NW)
        
    def show_composite_image(self, path):
        if self.original_img:
            img = Image.open(path).resize(self.original_img.size)
            mask = Image.new("L", self.original_img.size, 128)
            self.original_img = Image.composite(self.original_img, img, mask)
            self.display_img = ImageTk.PhotoImage(self.original_img.resize((600, 500)))
            self.delete('all')
            self.create_image(0, 0, image=self.display_img, anchor=tk.NW)

    def save_image(self):
        save_path = filedialog.asksaveasfilename(
            # initialdir=self.img_path
            initialdir=self.img_path.parent,
            title='Save as',
            filetypes=[('jpg', '*.jpg'), ('png', '*.png')]
        )
        if save_path:
            self.original_img.save(save_path)
        
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
        if self.drag_start:
            self.show_composite_image(event.data)
            CompositeBoard.drag_start = False
        else:
            self.show_image(event.data)
    

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

