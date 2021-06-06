import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../photoeditor'))

import tkinter as tk
from pathlib import Path
from unittest import TestCase, mock, main

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from TkinterDnD2 import *

from photoeditor.config import (SAVE_MSG_1, SAVE_MSG_2, INFO, ERROR, RIGHT_CANVAS_MSG_1,
    LEFT_CANVAS_MSG_1, LEFT_CANVAS_MSG_2, LEFT_CANVAS_MSG_3)
from photoeditor.composite_board import EditorBoard, Corner, CompositeBoard
from photoeditor.base_board import BaseBoard


class CompositeBoardTestCase(TestCase):

    def setUp(self):
        self.test_path = 'test.jpg'
        self.test_img = Image.open(self.test_path)
        self.width, self.height = self.test_img.size
        self.app = TkinterDnD.Tk()
        self.app.withdraw()
        self.editor = EditorBoard(self.app)
        self.pump_events()

    def tearDown(self):
        self.test_img.close()
        if self.app:
            self.app.destroy()
            self.pump_events()

    def pump_events(self):
        while self.app.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass


class SaveTestCase(CompositeBoardTestCase):
    """Test for save_with_pil
    """

    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_filedialog):
        """Check that a converted image is not saved
           when Save button is clicked and img_path is None.
        """

        self.editor.right_canvas.save_with_pil()
        mock_msgbox.assert_called_once()
        mock_filedialog.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_width_entry_is_empty(self, mock_msgbox, mock_filedialog):
        """Check that a converted image is not saved
           when Save button is clicked and width entry is empty.
        """
        height_var = mock.MagicMock()
        height_var.get.return_value = self.height
        mock_height_var = height_var
        width_var = mock.MagicMock()
        width_var.get.return_value = ''
        mock_width_var = width_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_with_pil()
        mock_msgbox.assert_called_once()
        mock_filedialog.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), SAVE_MSG_1)

    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_width_entry_is_0(self, mock_msgbox, mock_filedialog):
        """Check that a converted image is not saved
           when Save button is clicked and width entry is 0.
        """
        height_var = mock.MagicMock()
        height_var.get.return_value = self.height
        mock_height_var = height_var
        width_var = mock.MagicMock()
        width_var.get.return_value = 0
        mock_width_var = width_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_with_pil()
        mock_msgbox.assert_called_once()
        mock_filedialog.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), SAVE_MSG_1)

    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_height_entry_is_empty(self, mock_msgbox, mock_filedialog):
        """Check that a converted image is not saved
           when Save button is clicked and height_entry is empty.
        """
        height_var = mock.MagicMock()
        height_var.get.return_value = ''
        mock_height_var = height_var
        width_var = mock.MagicMock()
        width_var.get.return_value = self.width
        mock_width_var = width_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_with_pil()
        mock_msgbox.assert_called_once()
        mock_filedialog.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), SAVE_MSG_1)

    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_height_entry_is_0(self, mock_msgbox, mock_filedialog):
        """Check that a converted image is not saved
           when Save button is clicked and height_entry is 0.
        """
        height_var = mock.MagicMock()
        height_var.get.return_value = 0
        mock_height_var = height_var
        width_var = mock.MagicMock()
        width_var.get.return_value = self.width
        mock_width_var = width_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_with_pil()
        mock_msgbox.assert_called_once()
        mock_filedialog.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), SAVE_MSG_1)

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_save_path_is_selected(self, mock_err_msgbox, mock_filedialog, mock_info_msgbox):
        """Check that a converted image is saved
           when Save button is clicked and the image is not risezed.
        """
        width_var = mock.MagicMock()
        width_var.get.return_value = self.width
        mock_width_var = width_var
        height_var = mock.MagicMock()
        height_var.get.return_value = self.height
        mock_height_var = height_var
        mock_filedialog.return_value = 'test'
        mock_current_img = mock.MagicMock(size=(self.width, self.height))
        mock_current_save = mock.MagicMock()
        mock_thumbnail = mock.MagicMock()
        mock_thumbnail_save = mock.MagicMock()
        mock_current_img.save = mock_current_save
        mock_current_img.copy.return_value.thumbnail = mock_thumbnail
        mock_current_img.copy.return_value.save = mock_thumbnail_save
        with mock.patch.object(self.editor.right_canvas, 'current_img', mock_current_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_with_pil()
        mock_err_msgbox.assert_not_called()
        mock_filedialog.assert_called_once()
        mock_current_save.assert_called_once_with('test')
        mock_info_msgbox.assert_called_once_with(INFO, SAVE_MSG_2)
        mock_thumbnail.assert_not_called()
        mock_thumbnail_save.assert_not_called()

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_save_path_is_selected_and_resized(self, mock_err_msgbox, mock_filedialog, mock_info_msgbox):
        """Check that a converted image is saved
           when Save button is clicked and the image risezed.
        """
        width_var = mock.MagicMock()
        width_var.get.return_value = self.width * 2
        mock_width_var = width_var
        height_var = mock.MagicMock()
        height_var.get.return_value = self.height * 2
        mock_height_var = height_var
        mock_filedialog.return_value = 'test'
        mock_current_img = mock.MagicMock(size=(self.width, self.height))
        mock_current_save = mock.MagicMock()
        mock_thumbnail = mock.MagicMock()
        mock_thumbnail_save = mock.MagicMock()
        mock_current_img.save = mock_current_save
        mock_current_img.copy.return_value.thumbnail = mock_thumbnail
        mock_current_img.copy.return_value.save = mock_thumbnail_save
        with mock.patch.object(self.editor.right_canvas, 'current_img', mock_current_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_with_pil()
        mock_err_msgbox.assert_not_called()
        mock_filedialog.assert_called_once()
        mock_current_save.assert_not_called()
        mock_info_msgbox.assert_called_once_with(INFO, SAVE_MSG_2)
        mock_thumbnail.assert_called_once()
        mock_thumbnail_save.assert_called_once()


class ClearImageTestCase(CompositeBoardTestCase):
    """Test for clear_image
    """

    @mock.patch('photoeditor.base_board.tk.Canvas.delete')
    def test_clear_image(self, mock_delete):
        """Check that the images that the right canvas have are deleted
           when Clear button is clicked.
        """
        with mock.patch.object(self.editor.right_canvas, 'composite_images', ['test1']):
            with mock.patch.object(self.editor.right_canvas, 'holder_id', 1):
                self.editor.right_canvas.clear_image()
                self.assertEqual(self.editor.right_canvas.holder_id, None)
                self.assertEqual(self.editor.right_canvas.composite_images, [])
        mock_delete.assert_called_once_with('all')


class DeleteShapesTestCase(CompositeBoardTestCase):
    """Test for delete_shapes
    """
    @mock.patch('photoeditor.base_board.tk.Canvas.delete')
    def test_delete_shapes(self, mock_delete):
        """Check that the shapes drawn on the left canvas are deleted
           when Reset button is clicked.
        """
        with mock.patch.object(self.editor.left_canvas, 'corners', [Corner(300, 300)]):
            self.editor.left_canvas.delete_shapes()
            self.assertEqual(self.editor.left_canvas.corners, [])
        mock_delete.assert_called_once()


class CreateNewMaskTestCase(CompositeBoardTestCase):
    """Test for create_new_mask
    """

    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_img_path_is_None(self, mock_msgbox, mock_draw_shape):
        """Check that a mask image is not made on the left canvas
           when Create button is clicked and img_path is None.
        """
        self.editor.left_canvas.create_new_mask()
        mock_msgbox.assert_called_once()
        mock_draw_shape.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), LEFT_CANVAS_MSG_1)

    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_corners_is_empty(self, mock_msgbox, mock_draw_shape):
        """Check that a mask image is not made on the left canvas
           when Create button is clicked and no shapes are drawn.
        """
        with mock.patch.object(self.editor.left_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.left_canvas, 'corners', []):
                self.editor.left_canvas.create_new_mask()
        mock_msgbox.assert_called_once()
        mock_draw_shape.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), LEFT_CANVAS_MSG_2)

    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_shape3_and_corners_is_less_than_3(self, mock_msgbox, mock_draw_shape):
        """Check that a mask image is not made on the left canvas
           when Create button is clicked and shape3 cannot be drawn.
        """
        mock_intvar = mock.MagicMock()
        mock_intvar.get.return_value = 3
        mock_which_shapes = mock_intvar
        with mock.patch.object(self.editor.left_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.left_canvas, 'corners', [Corner(300, 300), Corner(320, 320)]):
                with mock.patch.object(self.editor.left_canvas, 'which_shapes', mock_which_shapes):
                    self.editor.left_canvas.create_new_mask()
        mock_msgbox.assert_called_once()
        mock_draw_shape.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), LEFT_CANVAS_MSG_3)

    @mock.patch('photoeditor.composite_board.LeftCanvas.create_image_pil')
    @mock.patch('photoeditor.composite_board.LeftCanvas.delete_shapes')
    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_create_new_mask(self, mock_msgbox, mock_draw_shape, mock_delete_shapes,
                             mock_create_image_pil):
        """Check that a mask image is made on the left canvas
           when Create button is clicked.
        """
        mock_draw_shape.return_value = self.test_img
        mock_intvar = mock.MagicMock()
        mock_intvar.get.return_value = 2
        mock_which_shapes = mock_intvar
        with mock.patch.object(self.editor.left_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.left_canvas, 'corners', [Corner(300, 300), Corner(320, 320)]):
                with mock.patch.object(self.editor.left_canvas, 'which_shapes', mock_which_shapes):
                    self.editor.left_canvas.create_new_mask()
        mock_msgbox.assert_not_called()
        mock_delete_shapes.assert_called_once()
        mock_create_image_pil.assert_called_once_with(self.test_img)
        self.assertEqual(
            CompositeBoard.holder[CompositeBoard.created_mask_id], self.test_img)


class ToggleMaskTestCase(CompositeBoardTestCase):
    """Test for toggle_mask
    """

    @mock.patch('photoeditor.composite_board.LeftCanvas.create_image_pil')
    def test_toggle_mask(self, mock_create_image_pil):
        """Check that mask images are changed on the left canvas
           when Change button is clicked.
        """
        self.editor.left_canvas.toggle_mask()
        self.editor.left_canvas.toggle_mask()
        mock_create_image_pil.assert_has_calls(
            [mock.call(CompositeBoard.holder[1]), mock.call(CompositeBoard.holder[2])])


class CropImageTestCase(CompositeBoardTestCase):
    """Test for crop_image
    """

    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_img_path_is_None(self, mock_msgbox, mock_draw_shape):
        """Check that a cropped image is not made on the left canvas
           when Crop button is clicked and img_path is None.
        """
        self.editor.left_canvas.crop_image()
        mock_msgbox.assert_called_once()
        mock_draw_shape.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), LEFT_CANVAS_MSG_1)

    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_corners_is_empty(self, mock_msgbox, mock_draw_shape):
        """Check that a cropped image is not made on the left canvas
           when Crop button is clicked with no shapes drawn.
        """
        with mock.patch.object(self.editor.left_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.left_canvas, 'corners', []):
                self.editor.left_canvas.crop_image()
        mock_msgbox.assert_called_once()
        mock_draw_shape.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), LEFT_CANVAS_MSG_2)

    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_shape3_and_corners_is_less_than_3(self, mock_msgbox, mock_draw_shape):
        """Check that a cropped image is not made on the left canvas
           when Crop button is clicked and shape3 cannot be drawn.
        """
        mock_intvar = mock.MagicMock()
        mock_intvar.get.return_value = 3
        mock_which_shapes = mock_intvar
        with mock.patch.object(self.editor.left_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.left_canvas, 'corners', [Corner(300, 300), Corner(320, 320)]):
                with mock.patch.object(self.editor.left_canvas, 'which_shapes', mock_which_shapes):
                    self.editor.left_canvas.crop_image()
        mock_msgbox.assert_called_once()
        mock_draw_shape.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), LEFT_CANVAS_MSG_3)

    @mock.patch('photoeditor.composite_board.LeftCanvas.create_image_pil')
    @mock.patch('photoeditor.composite_board.LeftCanvas.delete_shapes')
    @mock.patch('photoeditor.composite_board.LeftCanvas.draw_shape')
    @mock.patch('photoeditor.composite_board.messagebox.showerror')
    def test_create_new_mask(self, mock_msgbox, mock_draw_shape, mock_delete_shapes,
                             mock_create_image_pil):
        """Check that a mask image is made on the left canvas
           when Crop button is clicked.
        """
        mock_draw_shape.return_value = self.test_img
        mock_intvar = mock.MagicMock()
        mock_intvar.get.return_value = 2
        mock_which_shapes = mock_intvar
        with mock.patch.object(self.editor.left_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.left_canvas, 'corners', [Corner(300, 300), Corner(320, 320)]):
                with mock.patch.object(self.editor.left_canvas, 'which_shapes', mock_which_shapes):
                    self.editor.left_canvas.create_new_mask()
        mock_msgbox.assert_not_called()
        mock_delete_shapes.assert_called_once()
        mock_create_image_pil.assert_called_once_with(self.test_img)
        self.assertEqual(
            CompositeBoard.holder[CompositeBoard.created_mask_id], self.test_img)


if __name__ == '__main__':
    main()
