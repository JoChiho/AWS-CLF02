# -*- coding: utf-8 -*-
"""换行宽度计算测试"""

import unittest

from gui.wrapped_label import frame_wraplength


class TestWrappedLabel(unittest.TestCase):
    def test_frame_wraplength_accounts_for_scaling(self):
        physical = 400
        scale = 1.5
        wrap = frame_wraplength(physical, scale, margin=56, minimum=160)
        effective = wrap * scale
        self.assertLessEqual(effective, physical - 56 * scale + 1)

    def test_frame_wraplength_minimum(self):
        self.assertEqual(frame_wraplength(40, 1.0), 160)

    def test_frame_wraplength_grows_with_container(self):
        small = frame_wraplength(320, 1.0, margin=56)
        large = frame_wraplength(640, 1.0, margin=56)
        self.assertLess(small, large)


if __name__ == "__main__":
    unittest.main()