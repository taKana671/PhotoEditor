import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../photoeditor'))

import math
import tkinter as tk
from unittest import TestCase, mock, main

import cv2
import numpy as np
from TkinterDnD2 import *

from photoeditor.config import SAVE_MSG_1, SAVE_MSG_2, INFO, ERROR, RIGHT_CANVAS_MSG_1
from photoeditor.convert_board import EditorBoard


class ConvertBoardTestCase(TestCase):

    def setUp(self):
        self.test_path = 'test.jpg'
        self.test_img = cv2.imread(self.test_path)
        self.height, self.width, _ = self.test_img.shape
        self.app = TkinterDnD.Tk()
        self.app.withdraw()
        self.editor = EditorBoard(self.app)
        self.pump_events()

    def tearDown(self):
        if self.app:
            self.app.destroy()
            self.pump_events()

    def pump_events(self):
        while self.app.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass


class ShowGrayImageTestCase(ConvertBoardTestCase):
    """Test for show_gray_image
    """

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Gray button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_gray_image()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_not_none(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that gray image is displayed successfully
           when Gray button is clicked.
        """
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_gray_image()
        mock_create_image_cv.assert_called_once()
        self.assertTrue(
            (mock_create_image_cv.call_args_list[0][0] == cv2.cvtColor(self.test_img, cv2.COLOR_BGR2GRAY)).all())
        mock_display_image_size.assert_called_once_with(self.width, self.height)
        mock_msgbox.assert_not_called()


class ShowImageLikeAnimationTestCase(ConvertBoardTestCase):
    """Test for show_image_like_animation
    """

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Anime button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_image_like_animation()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_not_none(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the converted image is displayed successfully
           when Anime button is clicked.
        """
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_image_like_animation()
        mock_create_image_cv.assert_called_once()
        mock_display_image_size.assert_called_once_with(self.width, self.height)
        mock_msgbox.assert_not_called()


class ShowSepiaImageTestCase(ConvertBoardTestCase):
    """Test for show_sepia_image
    """

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Sepia button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_sepia_image()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('photoeditor.convert_board.RightCanvas.enhance_contrast')
    @mock.patch('photoeditor.convert_board.RightCanvas.superimpose_noise')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_no_checkbox_are_checked(self, mock_msgbox, mock_create_image_cv, mock_display_image_size,
                                     mock_impose, mock_contrast, mock_light):
        """Check that the display of a converted image
           when Sepia button is clicked with no check boxes checked.
        """
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_sepia_image()
            mock_msgbox.assert_not_called()
            mock_impose.assert_not_called()
            mock_contrast.assert_not_called()
            mock_light.assert_not_called()
            mock_create_image_cv.assert_called_once()
            mock_display_image_size.assert_called_once_with(self.width, self.height)

    @mock.patch('photoeditor.convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('photoeditor.convert_board.RightCanvas.enhance_contrast')
    @mock.patch('photoeditor.convert_board.RightCanvas.superimpose_noise')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_noise_checkbox_is_checked(self, mock_msgbox, mock_create_image_cv, mock_display_image_size,
                                       mock_impose, mock_contrast, mock_light):
        """Check that the display of a converted image
           when Sepia button is clicked with noise box checked.
        """
        mock_boolvar = mock.MagicMock()
        mock_boolvar.get.return_value = True
        mock_noise = mock_boolvar
        mock_impose.return_value = cv2.cvtColor(self.test_img, cv2.COLOR_BGR2GRAY)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'noise_bool', mock_noise):
                    self.editor.right_canvas.show_sepia_image()
        mock_msgbox.assert_not_called()
        mock_impose.assert_called_once()
        mock_contrast.assert_not_called()
        mock_light.assert_not_called()
        mock_create_image_cv.assert_called_once()
        mock_display_image_size.assert_called_once_with(self.width, self.height)

    @mock.patch('photoeditor.convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('photoeditor.convert_board.RightCanvas.enhance_contrast')
    @mock.patch('photoeditor.convert_board.RightCanvas.superimpose_noise')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_light_checkbox_is_checked(self, mock_msgbox, mock_create_image_cv, mock_display_image_size,
                                       mock_impose, mock_contrast, mock_light):
        """Check that the display of a converted image
           when Sepia button is clicked with light box checked.
        """
        mock_boolvar = mock.MagicMock()
        mock_boolvar.get.return_value = True
        mock_lightvar = mock_boolvar
        mock_light.return_value = cv2.cvtColor(self.test_img, cv2.COLOR_BGR2GRAY)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'light_bool', mock_lightvar):
                    self.editor.right_canvas.show_sepia_image()
        mock_msgbox.assert_not_called()
        mock_impose.assert_not_called()
        mock_contrast.assert_not_called()
        mock_light.assert_called_once()
        mock_create_image_cv.assert_called_once()
        mock_display_image_size.assert_called_once_with(self.width, self.height)

    @mock.patch('photoeditor.convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('photoeditor.convert_board.RightCanvas.enhance_contrast')
    @mock.patch('photoeditor.convert_board.RightCanvas.superimpose_noise')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_contrast_checkbox_is_checked(self, mock_msgbox, mock_create_image_cv, mock_display_image_size,
                                          mock_impose, mock_contrast, mock_light):
        """Check that the display of a converted image
           when Sepia button is clicked with contrast box checked.
        """
        mock_boolvar = mock.MagicMock()
        mock_boolvar.get.return_value = True
        mock_contrast_var = mock_boolvar
        mock_contrast.return_value = cv2.cvtColor(self.test_img, cv2.COLOR_BGR2GRAY)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'contrast_bool', mock_contrast_var):
                    self.editor.right_canvas.show_sepia_image()
        mock_msgbox.assert_not_called()
        mock_impose.assert_not_called()
        mock_contrast.assert_called_once()
        mock_light.assert_not_called()
        mock_create_image_cv.assert_called_once()
        mock_display_image_size.assert_called_once_with(self.width, self.height)


class ShowPixelArtTestCase(ConvertBoardTestCase):
    """Test for show_pixel_art
    """
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Pixel button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_pixel_art()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_not_none(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the converted image is displayed
           when Pixel button is clicked.
        """
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_pixel_art()
        mock_create_image_cv.assert_called_once()
        mock_display_image_size.assert_called_once_with(self.width, self.height)
        mock_msgbox.assert_not_called()


class ShowGeometricImageTestCase(ConvertBoardTestCase):
    """Test for show_geometric_image
    """

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Geometric button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_geometric_image()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_scale_entry_is_empty(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Geometric button is clicked because scale entry is empty.
        """
        mock_double_var = mock.MagicMock()
        msg = 'expected floating-point number but got ""'
        mock_double_var.get.side_effect = tk._tkinter.TclError(msg)
        mock_scale = mock_double_var
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'scale_double', mock_scale):
                    self.editor.right_canvas.show_geometric_image()
        # error message
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), msg)

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_angle_engry_is_empty(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Geometric button is clicked because angle entry is empty.
        """
        mock_int_var = mock.MagicMock()
        msg = 'expected intger-point number but got ""'
        mock_int_var.get.side_effect = tk._tkinter.TclError(msg)
        mock_angle = mock_int_var
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'angle_int', mock_angle):
                    self.editor.right_canvas.show_geometric_image()
        # error message
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), msg)

    @mock.patch('photoeditor.convert_board.RightCanvas.get_border_mode')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_args_containing_dst(self, mock_msgbox, mock_create_image_cv,
                                 mock_display_image_size, get_mode):
        """Check that the display of a converted image fails
           when args contains dst and Geometric button is clicked.
        """
        mat = cv2.getRotationMatrix2D((self.width / 2, self.height / 2), 45, 0.5)
        img = cv2.warpAffine(
            self.test_img, mat, (self.width, self.height), borderMode=cv2.BORDER_TRANSPARENT, dst=self.test_img // 4)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        get_mode.return_value = dict(borderMode=cv2.BORDER_TRANSPARENT, dst=None)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_geometric_image()
        self.assertTrue(
            (mock_create_image_cv.call_args_list[0][0] == img_rgb).all())
        mock_display_image_size.assert_called_once_with(self.width, self.height)
        mock_msgbox.assert_not_called()

    @mock.patch('photoeditor.convert_board.RightCanvas.get_border_mode')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_args_not_containing_dst(self, mock_msgbox, mock_create_image_cv,
                                     mock_display_image_size, get_mode):
        """Check that the display of a converted image fails
           when Geometric button is clicked.
        """
        mat = cv2.getRotationMatrix2D((self.width / 2, self.height / 2), 45, 0.5)
        img = cv2.warpAffine(
            self.test_img, mat, (self.width, self.height), borderMode=cv2.BORDER_CONSTANT)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        get_mode.return_value = dict(borderMode=cv2.BORDER_CONSTANT)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_geometric_image()
        self.assertTrue(
            (mock_create_image_cv.call_args_list[0][0] == img_rgb).all())
        mock_display_image_size.assert_called_once_with(self.width, self.height)
        mock_msgbox.assert_not_called()


class ShowSkewesImageTestCase(ConvertBoardTestCase):
    """Test for show_skews_image
    """

    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Skew button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_skewed_image()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.convert_board.RightCanvas.get_skew_angle')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_x_is_selected(self, mock_msgbox, mock_create_image_cv,
                           mock_display_image_size, mock_get_angle):
        """Check that a converted image is displayed
           when Skew button is clicked with x selected.
        """
        xy_bool = mock.MagicMock()
        xy_bool.get.return_value = True
        mock_xy = xy_bool
        mock_get_angle.return_value = 45
        angle = math.tan(math.radians(45))
        mat = np.array([[1, angle, 0], [0, 1, 0]], dtype=np.float32)
        img = cv2.warpAffine(
            self.test_img, mat, (int(self.width + self.height * angle), self.height))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'xy_bool', mock_xy):
                    self.editor.right_canvas.show_skewed_image()
        self.assertTrue(
            (mock_create_image_cv.call_args_list[0][0] == img_rgb).all())
        mock_display_image_size.assert_called_once_with(*img.shape[:-1][::-1])
        mock_msgbox.assert_not_called()

    @mock.patch('photoeditor.convert_board.RightCanvas.get_skew_angle')
    @mock.patch('photoeditor.convert_board.RightCanvas.display_image_size')
    @mock.patch('photoeditor.convert_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.convert_board.messagebox.showerror')
    def test_y_is_selected(self, mock_msgbox, mock_create_image_cv,
                           mock_display_image_size, mock_get_angle):
        """Check that a converted image is displayed
           when Skew button is clicked with y selected.
        """
        xy_bool = mock.MagicMock()
        xy_bool.get.return_value = False
        mock_xy = xy_bool
        mock_get_angle.return_value = 45
        angle = math.tan(math.radians(45))
        mat = np.array([[1, 0, 0], [angle, 1, 0]], dtype=np.float32)
        img = cv2.warpAffine(
            self.test_img, mat, (self.width, int(self.height + self.width * angle)))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'xy_bool', mock_xy):
                    self.editor.right_canvas.show_skewed_image()
        self.assertTrue(
            (mock_create_image_cv.call_args_list[0][0] == img_rgb).all())
        mock_display_image_size.assert_called_once_with(*img.shape[:-1][::-1])
        mock_msgbox.assert_not_called()


class SaveTestCase(ConvertBoardTestCase):
    """Test for save_open_cv
    """

    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_filedialog):
        """Check that a converted image is not saved
           when Save button is clicked because img_path is None.
        """
        self.editor.right_canvas.save_open_cv()
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
                    self.editor.right_canvas.save_open_cv()
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
                    self.editor.right_canvas.save_open_cv()
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
                    self.editor.right_canvas.save_open_cv()
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
                    self.editor.right_canvas.save_open_cv()
        mock_msgbox.assert_called_once()
        mock_filedialog.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), SAVE_MSG_1)

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.base_board.cv2.imwrite')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_save_path_is_not_selected(self, mock_err_msgbox, mock_filedialog,
                                       mock_imwrite, mock_info_msgbox):
        """Check that a converted image is not saved
           when Save button is clicked because dir is not selected.
        """
        width_var = mock.MagicMock()
        width_var.get.return_value = self.width
        mock_width_var = width_var
        height_var = mock.MagicMock()
        height_var.get.return_value = self.height
        mock_height_var = height_var
        mock_filedialog.return_value = ''
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_open_cv()
        mock_err_msgbox.assert_not_called()
        mock_filedialog.assert_called_once()
        mock_imwrite.assert_not_called()
        mock_info_msgbox.assert_not_called()

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.base_board.cv2.resize')
    @mock.patch('photoeditor.base_board.cv2.imwrite')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_save_path_is_selected(self, mock_err_msgbox, mock_filedialog,
                                   mock_imwrite, mock_resize, mock_info_msgbox):
        """Check that a converted image is saved without resizing
           when Save button is clicked.
        """
        width_var = mock.MagicMock()
        width_var.get.return_value = self.width
        mock_width_var = width_var
        height_var = mock.MagicMock()
        height_var.get.return_value = self.height
        mock_height_var = height_var
        mock_filedialog.return_value = 'tests'
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_open_cv()
        mock_err_msgbox.assert_not_called()
        mock_filedialog.assert_called_once()
        mock_resize.assert_not_called()
        mock_imwrite.assert_called_once()
        mock_info_msgbox.assert_called_once_with(INFO, SAVE_MSG_2)

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.base_board.cv2.resize')
    @mock.patch('photoeditor.base_board.cv2.imwrite')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_save_path_is_selected_and_resize(self, mock_err_msgbox, mock_filedialog,
                                              mock_imwrite, mock_resize, mock_info_msgbox):
        """Check that a converted image is resized and saved
           when Save button is clicked.
        """
        width_var = mock.MagicMock()
        width_var.get.return_value = self.width * 2
        mock_width_var = width_var
        height_var = mock.MagicMock()
        height_var.get.return_value = self.height * 2
        mock_height_var = height_var
        mock_filedialog.return_value = 'tests'
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            with mock.patch.object(self.editor.right_canvas, 'width_var', mock_width_var):
                with mock.patch.object(self.editor.right_canvas, 'height_var', mock_height_var):
                    self.editor.right_canvas.save_open_cv()
        mock_err_msgbox.assert_not_called()
        mock_filedialog.assert_called_once()
        mock_resize.assert_called_once()
        mock_imwrite.assert_called_once()
        mock_info_msgbox.assert_called_once_with(INFO, SAVE_MSG_2)


if __name__ == '__main__':
    main()
