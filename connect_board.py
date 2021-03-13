import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path

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
        self.connected_image_canvas = ConnectedImageCanvas(
            base_frame, self.width_var, self.height_var, self.col_var, self.row_var)
        self.connected_image_canvas.grid(row=0, column=1, padx=(1, 5),
            pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_controller(self, base_frame):
        controller_frame = tk.Frame(base_frame)
        controller_frame.grid(row=1, column=0, columnspan=2, 
            sticky=(tk.W, tk.E, tk.N, tk.S))
        # save image
        height_entry = ttk.Entry(controller_frame, width=10, textvariable=self.height_var)
        height_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
        height_label = ttk.Label(controller_frame, text='Height:')
        height_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        width_entry = ttk.Entry(controller_frame, width=10, textvariable=self.width_var)
        width_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        width_label = ttk.Label(controller_frame, text='Width:')
        width_label.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 1))
        save_button = ttk.Button(controller_frame, text='Save', 
            command=self.connected_image_canvas.save_image)
        save_button.pack(side=tk.RIGHT, pady=(3, 10), padx=(5, 1))
        # repeat the same image
        height_entry = ttk.Entry(
            controller_frame, width=5, textvariable=self.row_var)
        height_entry.pack(side=tk.RIGHT, pady=(3, 10), padx=(1, 5))
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


class ConnectBoard(BaseBoard):

    def __init__(self, master, width_var=None, height_var=None,
            col_var=None, row_var=None):
        self.col_var = col_var
        self.row_var = row_var
        super().__init__(master, width_var, height_var)


class OriginalImageCanvas(ConnectBoard):

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

    def __init__(self, master, width_var, height_var, col_var, row_var):
        super().__init__(master, width_var, height_var, col_var, row_var)
        self.create_bind()

    def create_bind(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)
 
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
            img = self.original_img.resize((self.original_img.width//col, self.original_img.height//row))
            base_h = self.concat_horizontally_repeat(img, col)
            self.original_img = self.concat_vertically_repeat(base_h, row)
            self.display_img = ImageTk.PhotoImage(self.original_img.resize((600, 500)))
            self.delete('all')
            self.create_image(0, 0, image=self.display_img, anchor=tk.NW)
        except Exception as e:
            messagebox.showerror('Error', e)
 
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
            width, height = self.original_img.size
            self.width_var.set(width)
            self.height_var.set(height)
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

