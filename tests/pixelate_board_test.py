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

from photoeditor.config import (SAVE_MSG_1, SAVE_MSG_2, INFO, ERROR, RIGHT_CANVAS_MSG_1,
    RIGHT_CANVAS_MSG_2, EYE_CASCADE_PATH, IMAGE_SIZE_MSG_1)
from photoeditor.pixelate_board import EditorBoard, Corner


class PixelateBoardTestCase(TestCase):

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


class SaveTestCase(PixelateBoardTestCase):
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
        """Check that a converted image is not risezed and saved
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
        """Check that a converted image is risezed and saved
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


class ShowPixelatedEntireTestCase(PixelateBoardTestCase):
    """Test for show_pixelated_entire
    """

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.pixelate')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_no_img_path(self, mock_msgbox, mock_pixelate, mock_create_image_cv):
        """Check that the display of a converted image fails
           when Entire button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_pixelated_entire()
        mock_pixelate.assert_not_called()
        mock_create_image_cv.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.pixelate')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_show_pixelated_entire(self, mock_msgbox, mock_pixelate, mock_create_image_cv):
        """Check that a converted image displayed successfully
           when Entire button is clicked.
        """
        mock_pixelate.return_value = self.test_img
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.show_pixelated_entire()
        mock_pixelate.assert_called_once_with(self.test_img, 0.1)
        mock_create_image_cv.assert_called_once_with(self.test_img)
        mock_msgbox.assert_not_called()


class ShowPixelatedAreaTestCase(PixelateBoardTestCase):
    """Test for show_pixelated_area
    """

    @mock.patch('photoeditor.pixelate_board.RightCanvas.clear_rectangle')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.pixelate')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_no_img_path(self, mock_msgbox, mock_pixelate, mock_create_image_cv,
                         mock_clear_rectangle):
        """Check that the display of a converted image fails
           when Area button is clicked because img_path is None.
        """
        self.editor.right_canvas.show_pixelated_area()
        mock_pixelate.assert_not_called()
        mock_create_image_cv.assert_not_called()
        mock_clear_rectangle.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.pixelate_board.RightCanvas.clear_rectangle')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.pixelate')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_corners_list_is_empty(self, mock_msgbox, mock_pixelate, mock_create_image_cv,
                                   mock_clear_rectangle):
        """Check that the display of a converted image fails
           when Area button is clicked because self.corners is empty.
        """
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'corners', []):
                    self.editor.right_canvas.show_pixelated_area()
        mock_pixelate.assert_not_called()
        mock_create_image_cv.assert_not_called()
        mock_clear_rectangle.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_2)

    @mock.patch('photoeditor.pixelate_board.RightCanvas.clear_rectangle')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.pixelate')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_show_pixelated_area(self, mock_msgbox, mock_pixelate, mock_create_image_cv,
                                 mock_clear_rectangle):
        """Check that a converted image is displayed
           when Area button is clicked.
        """
        test_corners = [Corner(200, 150), Corner(250, 200)]
        mock_pixelate.return_value = self.test_img[150:200, 200:250]
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'corners', test_corners):
                    self.editor.right_canvas.show_pixelated_area()
        mock_pixelate.assert_called_once()
        mock_create_image_cv.assert_called_once()
        mock_clear_rectangle.assert_called_once()
        mock_msgbox.assert_not_called()


class DetectFaceTestCase(PixelateBoardTestCase):
    """Test for detect_face
    """

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_no_img_path(self, mock_msgbox, mock_create_image_cv):
        """Check that face detection fails
           when Face Detect button is clicked because img_path is None.
        """
        self.editor.right_canvas.detect_face()
        mock_create_image_cv.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.get_faces')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_detect_face(self, mock_msgbox, mock_get_faces, mock_create_image_cv):
        """Check that faces are detected
           when Face Detect button is clicked.
        """
        faces = np.array([[177, 77, 68, 68]])
        img_gray = cv2.cvtColor(self.test_img, cv2.COLOR_BGR2GRAY)
        mock_get_faces.return_value = (faces, img_gray)
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
                    self.editor.right_canvas.detect_face()
        mock_get_faces.assert_called_once_with(self.test_img, 1.1, 3)
        mock_create_image_cv.assert_called_once_with(self.test_img)
        mock_msgbox.assert_not_called()


class DetectEyeTestCase(PixelateBoardTestCase):
    """Test for detect_eye
    """

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_no_img_path(self, mock_msgbox, mock_create_image_cv):
        """Check that eye detection fails
           when Eye Detect button is clicked because img_path is None.
        """
        self.editor.right_canvas.detect_face()
        mock_create_image_cv.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.pixelate_board.cv2.CascadeClassifier')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.get_faces')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_detect_eye(self, mock_msgbox, mock_get_faces, mock_create_image_cv,
                        mock_classifier):
        """Check that eyes are detected
           when Eye Detect button is clicked.
        """
        faces = np.array([[177, 77, 68, 68]])
        img_gray = cv2.cvtColor(self.test_img, cv2.COLOR_BGR2GRAY)
        mock_get_faces.return_value = (faces, img_gray)
        mock_cascade = mock.MagicMock()
        mock_detect_multi_scale = mock.MagicMock()
        mock_detect_multi_scale.return_value = np.array([[11, 16, 21, 21]])
        mock_cascade.detectMultiScale = mock_detect_multi_scale
        mock_classifier.return_value = mock_cascade
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
                    self.editor.right_canvas.detect_eye()
        mock_get_faces.assert_called_once_with(self.test_img, 1.1, 3)
        mock_classifier.assert_called_once_with(EYE_CASCADE_PATH)
        mock_detect_multi_scale.assert_called_once()
        mock_create_image_cv.assert_called_once_with(self.test_img)
        mock_msgbox.assert_not_called()


class CompareImagesTestCase(PixelateBoardTestCase):
    """Test for compare_images
    """

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_no_img_path(self, mock_msgbox, mock_create_image_cv):
        """Check that the comparison of image fails
           when Compare button is clicked because img_path is None.
        """
        self.editor.right_canvas.compare_images()
        mock_create_image_cv.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_sizes_not_same(self, mock_msgbox, mock_create_image_cv):
        """Check that the comparison of image fails when Compare button
           is clicked because the images don't have the same size.
        """
        mock_source_img = mock.MagicMock(shape=(1000, 1000, 3))
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', mock_source_img):
                self.editor.right_canvas.compare_images(self.test_img)
        mock_create_image_cv.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), IMAGE_SIZE_MSG_1)

    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_image_cv')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_compare_images(self, mock_msgbox, mock_create_image_cv):
        """Check that the comparison of image is carried out
           when Compare button is clicked.
        """
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            with mock.patch.object(self.editor.right_canvas, 'source_img', self.test_img):
                self.editor.right_canvas.compare_images(self.test_img)
        mock_create_image_cv.assert_called_once()
        mock_msgbox.assert_not_called()


class SaveGifFileTestClass(PixelateBoardTestCase):
    """Test for save_gif_file
    """

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_animated_gif')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_image_path_is_None(self, mock_msgbox, mock_filedialog, mock_create_animated_gif,
                                mock_info):
        """Check that a GIF file is not created or saved
           when Save GIF button is clicked because img_path is None.
        """
        mock_image = mock.MagicMock()
        mock_image.save = mock.MagicMock()
        mock_create_animated_gif.return_value = [mock_image]
        mock_filedialog.return_value = ''
        self.editor.right_canvas.save_gif_file()
        mock_filedialog.assert_not_called()
        mock_info.assert_not_called()
        mock_create_animated_gif.assert_not_called()
        mock_image.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_animated_gif')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_dir_not_selected(self, mock_msgbox, mock_filedialog, mock_create_animated_gif,
                              mock_info):
        """Check that a GIF file is not created or saved
           when Save GIF button is clicked because file dir is not selected.
        """
        mock_image = mock.MagicMock()
        mock_image.save = mock.MagicMock()
        mock_create_animated_gif.return_value = [mock_image]
        mock_filedialog.return_value = ''
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            self.editor.right_canvas.save_gif_file()
        mock_filedialog.assert_called_once()
        mock_msgbox.assert_not_called()
        mock_info.assert_not_called()
        mock_create_animated_gif.assert_not_called()
        mock_image.assert_not_called()

    @mock.patch('photoeditor.base_board.messagebox.showinfo')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_animated_gif')
    @mock.patch('photoeditor.base_board.filedialog.asksaveasfilename')
    @mock.patch('photoeditor.base_board.messagebox.showerror')
    def test_save_gif_file(self, mock_msgbox, mock_filedialog, mock_create_animated_gif,
                           mock_info):
        """Check that a GIF file is created or saved
           when Save GIF button is clicked.
        """
        mock_image = mock.MagicMock()
        mock_save = mock.MagicMock()
        mock_image.save = mock_save
        imgs = [mock_image, mock_image]
        mock_create_animated_gif.return_value = imgs
        test_dir = 'tests'
        mock_filedialog.return_value = test_dir
        with mock.patch.object(self.editor.right_canvas, 'current_img', self.test_img):
            self.editor.right_canvas.save_gif_file()
        mock_filedialog.assert_called_once()
        mock_msgbox.assert_not_called()
        mock_info.assert_called_once_with(INFO, SAVE_MSG_2)
        mock_create_animated_gif.assert_called_once()
        mock_save.assert_called_once_with(
            test_dir,
            save_all=True,
            append_images=imgs[1:],
            optimize=False,
            duration=50,
            loop=0)


class RunAnimatedGif(PixelateBoardTestCase):
    """Test for run_anumated_gif
    """

    @mock.patch('photoeditor.base_board.tk.Canvas.after')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_animated_gif')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_no_img_path(self, mock_msgbox, mock_create_animated_gif, mock_after):
        """Check that run of a animated gif fails
           when Run GIF button is clicked because img_path is None.
        """
        self.editor.right_canvas.run_animated_gif()
        mock_create_animated_gif.assert_not_called()
        mock_after.assert_not_called()
        # error message
        call_args = mock_msgbox.call_args_list[0]
        self.assertEqual(call_args[0][0], ERROR)
        self.assertEqual(str(call_args[0][1]), RIGHT_CANVAS_MSG_1)

    @mock.patch('photoeditor.base_board.tk.Canvas.after')
    @mock.patch('photoeditor.pixelate_board.RightCanvas.create_animated_gif')
    @mock.patch('photoeditor.pixelate_board.messagebox.showerror')
    def test_run_animated_gif(self, mock_msgbox, mock_create_animated_gif, mock_after):
        """Check that run of a animated gif fails
           when Run GIF button is clicked because img_path is None.
        """
        mock_create_animated_gif.return_value = self.test_img
        with mock.patch.object(self.editor.right_canvas, 'img_path', self.test_path):
            self.editor.right_canvas.run_animated_gif()
        mock_create_animated_gif.assert_called_once()
        mock_after.assert_called_once()
        mock_msgbox.assert_not_called()


if __name__ == '__main__':
    main()
