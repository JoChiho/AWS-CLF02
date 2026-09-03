# -*- coding: utf-8 -*-
"""薄弱点突击独立子菜单。"""

import customtkinter as ctk

from data.banks import BANK_NATIVE, BANK_WEAK_POINT_DRILL
from gui.constants import DOMAIN_DISPLAY_NAMES


class WeakPointMenuMixin:
    """针对反复错题考点的突击练习，进度独立存储。"""

    def _open_weak_point_menu(self) -> None:
        self.current_bank_id = BANK_WEAK_POINT_DRILL
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_weak_point_menu_ui()

    def _return_to_native_menu_from_weak_point(self) -> None:
        self.current_bank_id = BANK_NATIVE
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_menu_ui()

    def _build_weak_point_menu_ui(self) -> None:
        bank = self._get_bank()
        total_count = len(bank.ALL_QUESTIONS)
        single_count = len(bank.SINGLE_CHOICE_QUESTIONS)
        multi_count = len(bank.MULTI_CHOICE_QUESTIONS)

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
            command=self._return_to_native_menu_from_weak_point,
        ).pack(anchor="w", padx=60, pady=(0, 12))

        ctk.CTkLabel(
            scrollable,
            text="薄弱点突击",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#c0392b",
        ).pack(pady=(4, 4))

        ctk.CTkLabel(
            scrollable,
            text=f"针对反复错题的考点重出新题 · 共 {total_count} 题（单选 {single_count} / 多选 {multi_count}）· 进度独立",
            font=ctk.CTkFont(size=15),
            text_color="#95a5a6",
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            scrollable,
            text="覆盖 Direct Connect、Service Catalog、Audit Manager、Inspector/Config、迁云评估、Compute Optimizer、性能效率。",
            font=ctk.CTkFont(size=13),
            text_color="#7f8c8d",
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            scrollable,
            text="开始突击",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#c0392b",
        ).pack(anchor="w", padx=60, pady=(0, 6))

        ctk.CTkButton(
            scrollable,
            text=f"全部突击题（{total_count} 题）",
            height=52,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#922b21",
            hover_color="#c0392b",
            command=lambda: self._start_quiz(bank.ALL_QUESTIONS, "weak_point_drill:all"),
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
