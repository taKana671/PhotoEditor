import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../photoeditor'))

import tkinter as tk
from unittest import TestCase, mock, main

from PIL import Image
from TkinterDnD2 import *

from photoeditor.config import (SAVE_MSG_1, SAVE_MSG_2, INFO, ERROR,
    RIGHT_CANVAS_MSG_1, RIGHT_CANVAS_MSG_3, RIGHT_CANVAS_MSG_4)
from photoeditor.connect_board import EditorBoard, ConnectBoard


class ConnectBoardTestCase(TestCase):

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


class SaveTestCase(ConnectBoardTestCase):
    """Test for save_with_pil
    """

    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_filedialog):
        """Check that a converted image is not saved
           when Save button is clicked because img_path is None.
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
           when Save button is clicked because width entry is empty.
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
           when Save button is clicked because width is 0.
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
           when Save button is clicked because height entry is empty.
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
           when Save button is clicked because height is 0.
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
        """Check that a converted image is saved without resizing
           when Save button is clicked.
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
        """Check that a converted image is resized and saved
           when Save button is clicked.
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


class ShowRepeatedImageTestCase(ConnectBoardTestCase):
    """Test for show_repeated_image
    """

    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_current_img_is_none(self, mock_msgbox, mock_create_image_pil, mock_display_image_size):
        """Check that a repeated image is not made on the right canvas
           when Repeat button is clicked because current_img is None.
        """
        self.editor.right_canvas.show_repeated_image()
        mock_create_image_pil.assert_not_called()
        mock_display_image_size.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_columns_entry_is_empty(self, mock_msgbox, mock_create_image_pil, mock_display_image_size):
        """Check that a repeated image is not made on the right canvas
           when Repeat button is clicked because columns entry is empty.
        """
        int_var = mock.MagicMock()
        int_var.get.return_value = ''
        mock_col_var = int_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'col_var', mock_col_var):
                self.editor.right_canvas.show_repeated_image()
        mock_create_image_pil.assert_not_called()
        mock_display_image_size.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_3)

    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_columns_entry_is_0(self, mock_msgbox, mock_create_image_pil, mock_display_image_size):
        """Check that a repeated image is not made on the right canvas
           when Repeat button is clicked because columns entry is 0.
        """
        int_var = mock.MagicMock()
        int_var.get.return_value = 0
        mock_col_var = int_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'col_var', mock_col_var):
                self.editor.right_canvas.show_repeated_image()
        mock_create_image_pil.assert_not_called()
        mock_display_image_size.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_3)

    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_rows_entry_is_empty(self, mock_msgbox, mock_create_image_pil, mock_display_image_size):
        """Check that a repeated image is not made on the right canvas
           when Repeat button is clicked because rows entry is empty.
        """
        int_var = mock.MagicMock()
        int_var.get.return_value = ''
        mock_row_var = int_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'row_var', mock_row_var):
                self.editor.right_canvas.show_repeated_image()
        mock_create_image_pil.assert_not_called()
        mock_display_image_size.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_3)

    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_rows_entry_is_0(self, mock_msgbox, mock_create_image_pil, mock_display_image_size):
        """Check that a repeated image is not made on the right canvas
           when Repeat button is clicked because rows entry is 0.
        """
        int_var = mock.MagicMock()
        int_var.get.return_value = ''
        mock_row_var = int_var
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'row_var', mock_row_var):
                self.editor.right_canvas.show_repeated_image()
        mock_create_image_pil.assert_not_called()
        mock_display_image_size.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_3)

    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_show_repeated_image(self, mock_msgbox, mock_create_image_pil, mock_display_image_size):
        """Check that a repeated image is made on the right canvas
           when Repeat button is clicked.
        """
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            self.editor.right_canvas.show_repeated_image()
        mock_create_image_pil.assert_called_once()
        mock_display_image_size.assert_called_once_with(self.width, self.height)
        mock_msgbox.assert_not_called()


class ResetImageTestCase(ConnectBoardTestCase):
    """Test for reset_image
    """
    @mock.patch('photoeditor.base_board.tk.Canvas.delete')
    def test_reset_image(self, mock_delete):
        """Check that an image displayed on the right canvas
           is deleted when Reset button is clicked.
        """
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'concat_imgs', [self.test_img]):
                self.editor.right_canvas.reset_image()
                self.assertEqual(self.editor.right_canvas.current_img, None)
                self.assertEqual(self.editor.right_canvas.concat_imgs, [])
        mock_delete.assert_called_once_with('all')


class ShowConcatImageTestCase(ConnectBoardTestCase):
    """Test for show_concat_image
    """

    @mock.patch('photoeditor.connect_board.RightCanvas.concat_vertically')
    @mock.patch('photoeditor.connect_board.RightCanvas.concat_horizontally')
    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_current_img_is_none(self, mock_msgbox, mock_create_image_pil, mock_display_image_size,
                                 mock_concat_horizontally, mock_concat_vertically):
        """Check that a concat image is not made on the right canvas
           when Connect button is clicked because current_img is None.
        """
        self.editor.right_canvas.show_concat_image()
        mock_create_image_pil.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_concat_horizontally.assert_not_called()
        mock_concat_vertically.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.connect_board.RightCanvas.concat_vertically')
    @mock.patch('photoeditor.connect_board.RightCanvas.concat_horizontally')
    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_imgs_less_than_2(self, mock_msgbox, mock_create_image_pil, mock_display_image_size,
                              mock_concat_horizontally, mock_concat_vertically):
        """Check that a concat image is not made on the right canvas
           when Connect button is clicked because concat_imga has images less than 2.
        """
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'concat_imgs', [self.test_img]):
                self.editor.right_canvas.show_concat_image()
        mock_create_image_pil.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_concat_horizontally.assert_not_called()
        mock_concat_vertically.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_4)

    @mock.patch('photoeditor.connect_board.RightCanvas.concat_vertically')
    @mock.patch('photoeditor.connect_board.RightCanvas.concat_horizontally')
    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_show_horizontally_concat_image(self, mock_msgbox, mock_create_image_pil, mock_display_image_size,
                                            mock_concat_horizontally, mock_concat_vertically):
        """Check that a horizontally concatenated image is displayed
            on the right canvas when Connect button is clicked.
        """
        radio_bool = mock.MagicMock()
        radio_bool.get.return_value = True
        mock_radio_bool = radio_bool
        imgs = [self.test_img, self.test_img]
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'concat_imgs', imgs):
                with mock.patch.object(self.editor.right_canvas, 'radio_bool', mock_radio_bool):
                    self.editor.right_canvas.show_concat_image()
        mock_concat_horizontally.assert_called_once()
        mock_create_image_pil.assert_called_once()
        mock_display_image_size.assert_called_once()
        mock_concat_vertically.assert_not_called()
        mock_msgbox.assert_not_called()

    @mock.patch('photoeditor.connect_board.RightCanvas.concat_vertically')
    @mock.patch('photoeditor.connect_board.RightCanvas.concat_horizontally')
    @mock.patch('photoeditor.connect_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.connect_board.RightCanvas.create_image_pil')
    @mock.patch('photoeditor.connect_board.messagebox.showerror')
    def test_show_vertically_concat_image(self, mock_msgbox, mock_create_image_pil, mock_display_image_size,
                                          mock_concat_horizontally, mock_concat_vertically):
        """Check that a vertically concatenated image is displayed
           on the right canvas when Connect button is clicked.
        """
        radio_bool = mock.MagicMock()
        radio_bool.get.return_value = False
        mock_radio_bool = radio_bool
        imgs = [self.test_img, self.test_img]
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'concat_imgs', imgs):
                with mock.patch.object(self.editor.right_canvas, 'radio_bool', mock_radio_bool):
                    self.editor.right_canvas.show_concat_image()
        mock_concat_vertically.assert_called_once()
        mock_create_image_pil.assert_called_once()
        mock_display_image_size.assert_called_once()
        mock_concat_horizontally.assert_not_called()
        mock_msgbox.assert_not_called()


class ClearImagesTestCase(ConnectBoardTestCase):
    """Test for clear_images
    """

    @mock.patch('photoeditor.base_board.tk.Canvas.delete')
    def test_clear_image(self, mock_delete):
        """Check that images that the left canvas has
           are deleted when Clear button is clicked.
        """
        with mock.patch.object(self.editor.left_canvas, 'current_img', self.test_img):
            with mock.patch.object(ConnectBoard, 'sources', {1: self.test_img}):
                with mock.patch.object(ConnectBoard, 'source_idx', 1):
                    self.assertEqual(ConnectBoard.sources, {1: self.test_img})
                    self.assertEqual(ConnectBoard.source_idx, 1)
                    self.editor.left_canvas.clear_images()
                    self.assertEqual(ConnectBoard.sources, {})
                    self.assertEqual(ConnectBoard.source_idx, 0)
        mock_delete.assert_called_once_with('all')


class ChangeImagesTestCase(ConnectBoardTestCase):
    """Test for change_images
    """

    @mock.patch('photoeditor.connect_board.LeftCanvas.create_image_pil')
    def test_sources_dict_is_empty(self, mock_create_image_pil):
        """Check that no image is displayed when Change button is clicked
           because ConnectBoard.sources dict is empty.
        """
        self.editor.left_canvas.change_images()
        mock_create_image_pil.assert_not_called()

    @mock.patch('photoeditor.connect_board.LeftCanvas.create_image_pil')
    def test_change_images(self, mock_create_image_pil):
        """Check that images are changed on the left canvas
           when Change button is clicked.
        """
        sources = {1: self.test_img, 2: self.test_img}
        with mock.patch.object(ConnectBoard, 'sources', sources):
            self.editor.left_canvas.change_images()
            self.editor.left_canvas.change_images()
        mock_create_image_pil.assert_has_calls(
            [mock.call(self.test_img), mock.call(self.test_img)])


if __name__ == '__main__':
    main()
