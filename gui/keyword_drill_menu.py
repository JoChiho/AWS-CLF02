# -*- coding: utf-8 -*-
"""服务定义辨识（关键词闪卡）独立子菜单。"""

import customtkinter as ctk

from data.banks import BANK_KEYWORD_DRILL, BANK_NATIVE
from gui.constants import DOMAIN_DISPLAY_NAMES


class KeywordDrillMenuMixin:
    """看定义选服务名：考前热身，进度独立存储。"""

    def _open_keyword_drill_menu(self) -> None:
        self.current_bank_id = BANK_KEYWORD_DRILL
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_keyword_drill_menu_ui()

    def _return_to_native_menu_from_drill(self) -> None:
        self.current_bank_id = BANK_NATIVE
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_menu_ui()

    def _build_keyword_drill_menu_ui(self) -> None:
        bank = self._get_bank()
        total_count = len(bank.ALL_QUESTIONS)

        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill="both", expand=True, padx=40, pady=30)

        scrollable = ctk.CTkScrollableFrame(self.menu_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True)

        ctk.CTkButton(
            scrollable,
            text="← 返回主菜单",
            height=36,
            font=ctk.CTkFont(size=14),
            fg_color="#34495e",
            hover_color="#4a6278",
            command=self._return_to_native_menu_from_drill,
        ).pack(anchor="w", padx=60, pady=(0, 12))

        ctk.CTkLabel(
            scrollable,
            text="服务定义辨识",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#e67e22",
        ).pack(pady=(4, 4))

        ctk.CTkLabel(
            scrollable,
            text=f"看定义 → 从 4 个易混名称里选服务 · 共 {total_count} 题 · 进度独立",
            font=ctk.CTkFont(size=15),
            text_color="#95a5a6",
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            scrollable,
            text="适合做真题前先把 S3 / EBS / EFS、GuardDuty / Inspector / Macie 等对上号。",
            font=ctk.CTkFont(size=13),
            text_color="#7f8c8d",
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            scrollable,
            text="开始练习",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e67e22",
        ).pack(anchor="w", padx=60, pady=(0, 6))

        ctk.CTkButton(
            scrollable,
            text=f"全部定义题（{total_count} 题）",
            height=52,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#d35400",
            hover_color="#e67e22",
            command=lambda: self._start_quiz(bank.ALL_QUESTIONS, "keyword_drill:all"),
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkButton(
            scrollable,
            text="自定义练习（抽 10/20/30/50 题）",
            height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#8e44ad",
            hover_color="#9b59b6",
            command=self._show_custom_practice_dialog,
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkLabel(
            scrollable,
            text="按考试领域",
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
            text="我的学习（本模式独立进度）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f39c12",
        ).pack(anchor="w", padx=60, pady=(18, 6))

        ctk.CTkButton(
            scrollable,
            text="打开错题本",
            height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self._show_wrong_book,
        ).pack(pady=6, fill="x", padx=60)

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
            text="我的统计与趋势",
            height=42,
            font=ctk.CTkFont(size=15),
            fg_color="#8e44ad",
            hover_color="#9b59b6",
            command=self._show_my_stats,
        ).pack(pady=4, fill="x", padx=60)
