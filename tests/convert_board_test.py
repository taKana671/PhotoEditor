import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tkinter as tk
from pathlib import Path
from unittest import TestCase, mock, main

import cv2
from TkinterDnD2 import *

from convert_board import EditorBoard, ERROR, RIGHT_CANVAS_MSG_1


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

    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Gray button is clicked and img_path is None.
        """
        self.editor.right_canvas.show_gray_image()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
    def test_image_path_is_not_none(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that gray image is displayed successfully
           when Gray button is clicked and img_path is not None.
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
    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Anime button is clicked and img_path is None.
        """
        self.editor.right_canvas.show_image_like_animation()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
    def test_image_path_is_not_none(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the converted image is displayed successfully
           when Anime button is clicked and img_path is not None.
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
    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Sepia button is clicked and img_path is None.
        """
        self.editor.right_canvas.show_sepia_image()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('convert_board.RightCanvas.enhance_contrast')
    @mock.patch('convert_board.RightCanvas.superimpose_noise')
    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
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

    @mock.patch('convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('convert_board.RightCanvas.enhance_contrast')
    @mock.patch('convert_board.RightCanvas.superimpose_noise')
    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
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

    @mock.patch('convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('convert_board.RightCanvas.enhance_contrast')
    @mock.patch('convert_board.RightCanvas.superimpose_noise')
    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
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

    @mock.patch('convert_board.RightCanvas.correct_peripheral_light')
    @mock.patch('convert_board.RightCanvas.enhance_contrast')
    @mock.patch('convert_board.RightCanvas.superimpose_noise')
    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
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
    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the display of a converted image fails
           when Pixel button is clicked and img_path is None.
        """
        self.editor.right_canvas.show_pixel_art()
        mock_create_image_cv.assert_not_called()
        mock_display_image_size.assert_not_called()
        mock_msgbox.assert_called_once()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('convert_board.RightCanvas.display_image_size')
    @mock.patch('convert_board.RightCanvas.create_image_cv')
    @mock.patch('convert_board.messagebox.showerror')
    def test_image_path_is_not_none(self, mock_msgbox, mock_create_image_cv, mock_display_image_size):
        """Check that the converted image is displayed
           when Pixel button is clicked and img_path is not None.
        """
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_pixel_art()
        mock_create_image_cv.assert_called_once()
        mock_display_image_size.assert_called_once_with(self.width, self.height)
        mock_msgbox.assert_not_called()


if __name__ == '__main__':
    main()
