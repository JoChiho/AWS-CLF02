# -*- coding: utf-8 -*-
"""GUI 模块导入与结构回归测试"""

import importlib.util
import unittest

HAS_CTK = importlib.util.find_spec("customtkinter") is not None


@unittest.skipUnless(HAS_CTK, "customtkinter not installed")
class TestGuiImports(unittest.TestCase):
    def test_launch_gui_exported(self):
        from gui import launch_gui, CLFQuizApp
        self.assertTrue(callable(launch_gui))
        self.assertTrue(issubclass(CLFQuizApp, object))

    def test_submodules_importable(self):
        from gui.menu import MenuMixin
        from gui.quiz_view import QuizMixin
        from gui.stats_view import StatsMixin
        from gui.mock_exam import MockExamMixin
        from gui.wrong_book_view import WrongBookMixin
        from gui.constants import DOMAIN_DISPLAY_NAMES

        self.assertTrue(hasattr(MenuMixin, "_build_menu_ui"))
        self.assertTrue(hasattr(QuizMixin, "_begin_quiz_session"))
        self.assertTrue(hasattr(StatsMixin, "_show_history"))
        self.assertTrue(hasattr(MockExamMixin, "_start_mock_exam"))
        self.assertTrue(hasattr(WrongBookMixin, "_show_wrong_book"))
        self.assertIn("Cloud Concepts", DOMAIN_DISPLAY_NAMES)

    def test_app_composes_mixins(self):
        from gui.app import CLFQuizApp
        from gui.menu import MenuMixin
        from gui.quiz_view import QuizMixin
        from gui.stats_view import StatsMixin
        from gui.mock_exam import MockExamMixin
        from gui.wrong_book_view import WrongBookMixin

        self.assertTrue(issubclass(CLFQuizApp, MenuMixin))
        self.assertTrue(issubclass(CLFQuizApp, QuizMixin))
        self.assertTrue(issubclass(CLFQuizApp, StatsMixin))
        self.assertTrue(issubclass(CLFQuizApp, MockExamMixin))
        self.assertTrue(issubclass(CLFQuizApp, WrongBookMixin))


if __name__ == "__main__":
    unittest.main()