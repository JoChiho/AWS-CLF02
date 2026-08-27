# -*- coding: utf-8 -*-
"""
AWS CLF-C02 图形界面刷题系统（练习模式）

模块结构：
    app.py        - 应用入口与共享状态初始化
    menu.py       - 主菜单
    quiz_view.py  - 答题界面
    stats_view.py - 历史 / 错题本 / 统计
    mock_exam.py     - 模拟考试（65 题 / 90 分钟）
    wrong_book_view.py - 增强错题本
    custom_practice_view.py - 自定义练习
    keyword_drill_menu.py - 服务定义辨识子菜单
    concept_drill_menu.py - 策略与准则辨识子菜单
"""

from typing import Dict, List, Any

import customtkinter as ctk

from gui.bank_context import BankContextMixin
from gui.menu import MenuMixin
from gui.cloudcertprep_menu import CloudCertPrepMenuMixin
from gui.keyword_drill_menu import KeywordDrillMenuMixin
from gui.concept_drill_menu import ConceptDrillMenuMixin
from gui.quiz_view import QuizMixin
from gui.stats_view import StatsMixin
from gui.mock_exam import MockExamMixin
from gui.wrong_book_view import WrongBookMixin
from gui.custom_practice_view import CustomPracticeMixin


class CLFQuizApp(
    BankContextMixin,
    MenuMixin,
    CloudCertPrepMenuMixin,
    KeywordDrillMenuMixin,
    ConceptDrillMenuMixin,
    QuizMixin,
    StatsMixin,
    MockExamMixin,
    WrongBookMixin,
    CustomPracticeMixin,
    ctk.CTk,
):
    """AWS CLF-C02 刷题主窗口（组合各功能 Mixin）"""

    def __init__(self):
        super().__init__()

        self.title("AWS CLF-C02 认证考试刷题系统 - 练习模式")
        self.geometry("1000x720")
        self.minsize(820, 620)
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 题库与会话状态
        self.questions: List[Dict[str, Any]] = []
        self.total = 0
        self.user_answers: Dict[int, List[str]] = {}
        self.current_index = 0

        # 答题界面控件引用
        self.option_widgets: List[ctk.CTkRadioButton | ctk.CTkCheckBox] = []
        self._option_text_labels: List[ctk.CTkLabel] = []
        self.is_multi = False
        self.multi_submit_btn: ctk.CTkButton | None = None

        # 持久化追踪
        self.current_mode: str = "all"
        self.quiz_start_time: float = 0.0
        self._question_shuffles: Dict[int, Dict[str, Any]] = {}
        self._user_font_scale: float = 1.0
        self._explanation_full_visible: bool = False

        # 布局 frame 引用（返回主菜单时清理）
        self.menu_frame = None
        self.top_frame = None
        self.main_frame = None
        self.nav_frame = None

        # 模拟考试状态
        self._mock_exam_active = False
        self._mock_submitted = False
        self._mock_timer_remaining = 0
        self._mock_timer_job = None

        self._init_bank_context()
        self._build_menu_ui()


def launch_gui():
    """启动图形界面"""
    app = CLFQuizApp()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()