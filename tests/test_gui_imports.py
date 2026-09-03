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
        from gui.custom_practice_view import CustomPracticeMixin
        from gui.cloudcertprep_menu import CloudCertPrepMenuMixin
        from gui.keyword_drill_menu import KeywordDrillMenuMixin
        from gui.concept_drill_menu import ConceptDrillMenuMixin
        from gui.weak_point_menu import WeakPointMenuMixin
        from gui.bank_context import BankContextMixin
        from gui.constants import DOMAIN_DISPLAY_NAMES

        self.assertTrue(hasattr(MenuMixin, "_build_menu_ui"))
        self.assertTrue(hasattr(QuizMixin, "_begin_quiz_session"))
        self.assertTrue(hasattr(QuizMixin, "_toggle_explanation_layout"))
        self.assertTrue(hasattr(QuizMixin, "_apply_explanation_layout"))
        self.assertTrue(hasattr(QuizMixin, "_increase_quiz_font"))
        self.assertTrue(hasattr(QuizMixin, "_decrease_quiz_font"))
        self.assertTrue(hasattr(StatsMixin, "_show_history"))
        self.assertTrue(hasattr(MockExamMixin, "_start_mock_exam"))
        self.assertTrue(hasattr(WrongBookMixin, "_show_wrong_book"))
        self.assertTrue(hasattr(CustomPracticeMixin, "_show_custom_practice_dialog"))
        self.assertTrue(hasattr(CloudCertPrepMenuMixin, "_open_cloudcertprep_menu"))
        self.assertTrue(hasattr(KeywordDrillMenuMixin, "_open_keyword_drill_menu"))
        self.assertTrue(hasattr(ConceptDrillMenuMixin, "_open_concept_drill_menu"))
        self.assertTrue(hasattr(WeakPointMenuMixin, "_open_weak_point_menu"))
        self.assertTrue(hasattr(BankContextMixin, "_get_bank"))
        self.assertTrue(hasattr(BankContextMixin, "_is_keyword_drill"))
        self.assertTrue(hasattr(BankContextMixin, "_is_concept_drill"))
        self.assertTrue(hasattr(BankContextMixin, "_is_weak_point_drill"))
        self.assertIn("Cloud Concepts", DOMAIN_DISPLAY_NAMES)

    def test_app_composes_mixins(self):
        from gui.app import CLFQuizApp
        from gui.menu import MenuMixin
        from gui.quiz_view import QuizMixin
        from gui.stats_view import StatsMixin
        from gui.mock_exam import MockExamMixin
        from gui.wrong_book_view import WrongBookMixin
        from gui.custom_practice_view import CustomPracticeMixin
        from gui.cloudcertprep_menu import CloudCertPrepMenuMixin
        from gui.keyword_drill_menu import KeywordDrillMenuMixin
        from gui.concept_drill_menu import ConceptDrillMenuMixin
        from gui.weak_point_menu import WeakPointMenuMixin
        from gui.bank_context import BankContextMixin

        self.assertTrue(issubclass(CLFQuizApp, BankContextMixin))
        self.assertTrue(issubclass(CLFQuizApp, CloudCertPrepMenuMixin))
        self.assertTrue(issubclass(CLFQuizApp, KeywordDrillMenuMixin))
        self.assertTrue(issubclass(CLFQuizApp, ConceptDrillMenuMixin))
        self.assertTrue(issubclass(CLFQuizApp, WeakPointMenuMixin))
        self.assertTrue(issubclass(CLFQuizApp, MenuMixin))
        self.assertTrue(issubclass(CLFQuizApp, QuizMixin))
        self.assertTrue(issubclass(CLFQuizApp, StatsMixin))
        self.assertTrue(issubclass(CLFQuizApp, MockExamMixin))
        self.assertTrue(issubclass(CLFQuizApp, WrongBookMixin))
        self.assertTrue(issubclass(CLFQuizApp, CustomPracticeMixin))


if __name__ == "__main__":
    unittest.main()