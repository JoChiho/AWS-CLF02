# -*- coding: utf-8 -*-
"""CloudCertPrep 题库独立子菜单。"""

import customtkinter as ctk

from data.banks import BANK_CLOUDCERTPREP, BANK_NATIVE
from gui.constants import DOMAIN_DISPLAY_NAMES, MOCK_EXAM_DURATION_MIN, MOCK_EXAM_QUESTION_COUNT


class CloudCertPrepMenuMixin:
    """CloudCertPrep 板块入口与子菜单（进度与自建题库完全隔离）。"""

    def _open_cloudcertprep_menu(self) -> None:
        self.current_bank_id = BANK_CLOUDCERTPREP
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_cloudcertprep_menu_ui()

    def _return_to_native_menu(self) -> None:
        self.current_bank_id = BANK_NATIVE
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_menu_ui()

    def _build_cloudcertprep_menu_ui(self) -> None:
        bank = self._get_bank()
        single_count = len(bank.SINGLE_CHOICE_QUESTIONS)
        multi_count = len(bank.MULTI_CHOICE_QUESTIONS)
        total_count = len(bank.ALL_QUESTIONS)

        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill="both", expand=True, padx=40, pady=30)

        scrollable = ctk.CTkScrollableFrame(self.menu_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True)

        ctk.CTkButton(
            scrollable,
            text="← 返回自建题库（320 题）",
            height=36,
            font=ctk.CTkFont(size=14),
            fg_color="#34495e",
            hover_color="#4a6278",
            command=self._return_to_native_menu,
        ).pack(anchor="w", padx=60, pady=(0, 12))

        ctk.CTkLabel(
            scrollable,
            text="CloudCertPrep 题库",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1abc9c",
        ).pack(pady=(4, 4))

        ctk.CTkLabel(
            scrollable,
            text=f"MIT 开源题库 · 已中文化 · 共 {total_count} 题（进度独立存储）",
            font=ctk.CTkFont(size=15),
            text_color="#95a5a6",
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            scrollable,
            text="模拟考试（贴近真实 CLF-C02）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e67e22",
        ).pack(anchor="w", padx=60, pady=(0, 6))

        ctk.CTkButton(
            scrollable,
            text=f"开始模拟考试（{MOCK_EXAM_QUESTION_COUNT}题 · {MOCK_EXAM_DURATION_MIN}分钟 · 无解析）",
            height=52,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#e67e22",
            hover_color="#f39c12",
            command=self._show_mock_exam_intro,
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkLabel(
            scrollable,
            text="练习模式",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888",
        ).pack(anchor="w", padx=60, pady=(12, 6))

        ctk.CTkButton(
            scrollable,
            text=f"单选题题库（{single_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            command=lambda: self._start_quiz(bank.SINGLE_CHOICE_QUESTIONS, "single"),
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkButton(
            scrollable,
            text=f"多选题题库（{multi_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            fg_color="#2980b9",
            hover_color="#3498db",
            command=lambda: self._start_quiz(bank.MULTI_CHOICE_QUESTIONS, "multi"),
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkButton(
            scrollable,
            text=f"全部题目（{total_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            command=lambda: self._start_quiz(bank.ALL_QUESTIONS, "all"),
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkLabel(
            scrollable,
            text="自定义练习",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#9b59b6",
        ).pack(anchor="w", padx=60, pady=(12, 6))

        ctk.CTkButton(
            scrollable,
            text="自定义练习（抽 10/20/30/50 题 · 筛选未做/低正确率）",
            height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#8e44ad",
            hover_color="#9b59b6",
            command=self._show_custom_practice_dialog,
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkLabel(
            scrollable,
            text="按考试领域分类练习",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00b894",
        ).pack(anchor="w", padx=60, pady=(18, 6))

        for domain in bank.DOMAINS:
            count = bank.get_domain_question_count(domain)
            display_name = DOMAIN_DISPLAY_NAMES.get(domain, domain)
            ctk.CTkButton(
                scrollable,
                text=f"{display_name}（{count}题）",
                height=48,
                font=ctk.CTkFont(size=16),
                fg_color="#00b894",
                hover_color="#00d9a3",
                command=lambda d=domain: self._start_domain_quiz(d),
            ).pack(pady=6, fill="x", padx=60)

        ctk.CTkLabel(
            scrollable,
            text="我的学习（CloudCertPrep 独立进度）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f39c12",
        ).pack(anchor="w", padx=60, pady=(18, 6))

        ctk.CTkButton(
            scrollable,
            text="历史记录（近10次）",
            height=42,
            font=ctk.CTkFont(size=15),
            fg_color="#7f8c8d",
            hover_color="#95a5a6",
            command=self._show_history,
        ).pack(pady=4, fill="x", padx=60)

        ctk.CTkButton(
            scrollable,
            text="错题本（增强）",
            height=42,
            font=ctk.CTkFont(size=15),
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self._show_wrong_book,
        ).pack(pady=4, fill="x", padx=60)

        ctk.CTkButton(
            scrollable,
            text="我的统计与趋势",
            height=42,
            font=ctk.CTkFont(size=15),
            fg_color="#8e44ad",
            hover_color="#9b59b6",
            command=self._show_my_stats,
        ).pack(pady=4, fill="x", padx=60)

        ctk.CTkLabel(
            scrollable,
            text="提示：题干与选项为中文（AWS 术语保留英文）；解析区可追加术语中文标注",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
        ).pack(pady=(20, 10))