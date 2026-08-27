# -*- coding: utf-8 -*-
"""策略与准则辨识独立子菜单。"""

import customtkinter as ctk

from data.banks import BANK_CONCEPT_DRILL, BANK_NATIVE
from gui.constants import DOMAIN_DISPLAY_NAMES


class ConceptDrillMenuMixin:
    """迁移策略、CAF/WAF 准则、落地场景术语：进度独立。"""

    def _open_concept_drill_menu(self) -> None:
        self.current_bank_id = BANK_CONCEPT_DRILL
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_concept_drill_menu_ui()

    def _return_to_native_menu_from_concept_drill(self) -> None:
        self.current_bank_id = BANK_NATIVE
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
        self._build_menu_ui()

    def _build_concept_drill_menu_ui(self) -> None:
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
            command=self._return_to_native_menu_from_concept_drill,
        ).pack(anchor="w", padx=60, pady=(0, 12))

        ctk.CTkLabel(
            scrollable,
            text="策略与准则辨识",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#5dade2",
        ).pack(pady=(4, 4))

        ctk.CTkLabel(
            scrollable,
            text=f"看场景 → 选 7 R / CAF / Well-Architected / DR 等术语 · 共 {total_count} 题 · 进度独立",
            font=ctk.CTkFont(size=15),
            text_color="#95a5a6",
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            scrollable,
            text="适合补 Rehost/Replatform、六大视角、RTO/RPO、责任共担落地这类真题用语。",
            font=ctk.CTkFont(size=13),
            text_color="#7f8c8d",
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            scrollable,
            text="开始练习",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#5dade2",
        ).pack(anchor="w", padx=60, pady=(0, 6))

        ctk.CTkButton(
            scrollable,
            text=f"全部策略题（{total_count} 题）",
            height=52,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1a5276",
            hover_color="#2874a6",
            command=lambda: self._start_quiz(bank.ALL_QUESTIONS, "concept_drill:all"),
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
