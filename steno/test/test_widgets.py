# -*- coding: utf-8 -*-
"""
.. module:: test_widgets
   :platform: Unix, Windows
   :synopsis: Custom widgets testing

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import unittest

from widgets import VideoWidget


class VideoWidgetTestCase(unittest.TestCase):

    def test_size_calculation(self):
        data = (
            (4, 3, 500, 300, 400, 300),
            (4, 3, 200, 300, 200, 150),
            (3, 2, 400, 200, 300, 200),
            (3, 2, 150, 200, 150, 100),
            (5, 3, 600, 300, 500, 300),
            (5, 3, 250, 300, 250, 150),
            (16, 9, 170, 90, 160, 90),
            (16, 9, 80, 90, 80, 45),
            (14, 9, 150, 90, 140, 90),
            (14, 9, 70, 90, 70, 45),
            (16, 10, 200, 100, 160, 100),
            (16, 10, 80, 100, 80, 50),
            (21, 9, 250, 90, 210, 90),
            (21, 9, 70, 500, 70, 30),
        )
        for aspect_w, aspect_h, slot_w, slot_h, result_w, result_h in data:
            size = VideoWidget._calculate_size((slot_w, slot_h),
                                               (aspect_w, aspect_h))
            msg = (u'On verifying of {0}x{1}.\nSlot: {2}x{3}.\n'
                   'Expected: {4}x{5}.\nReceived: {6}x{7}.'
                   .format(aspect_w, aspect_h, slot_w, slot_h, result_w,
                           result_h, size.GetWidth(), size.GetHeight()))
            self.assertEqual(size.GetWidth(), result_w, msg=msg)
            self.assertEqual(size.GetHeight(), result_h, msg=msg)
