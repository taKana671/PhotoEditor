import tkinter as tk
from unittest import TestCase

import cv2
from TkinterDnD2 import *

from photoeditor.convert_board import EditorBoard


class CommonSetUp(TestCase):

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
