# -*- coding: utf-8 -*-
"""主菜单界面"""

import customtkinter as ctk

from data import (
    ALL_QUESTIONS,
    SINGLE_CHOICE_QUESTIONS,
    MULTI_CHOICE_QUESTIONS,
    DOMAINS,
    get_domain_question_count,
)
from gui.constants import DOMAIN_DISPLAY_NAMES, MOCK_EXAM_QUESTION_COUNT, MOCK_EXAM_DURATION_MIN


class MenuMixin:
    """主菜单构建与题库入口"""

    def _build_menu_ui(self):
        """题库选择主菜单（支持传统模式 + 考试领域分类练习）"""
        from data.banks import BANK_NATIVE

        self.current_bank_id = BANK_NATIVE
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill="both", expand=True, padx=40, pady=30)

        scrollable = ctk.CTkScrollableFrame(self.menu_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True)

        ctk.CTkLabel(
            scrollable,
            text="AWS CLF-C02 刷题系统",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            scrollable,
            text="请选择练习模式或模拟考试",
            font=ctk.CTkFont(size=16),
        ).pack(pady=(0, 12))

        # ========== CloudCertPrep 独立板块 ==========
        try:
            from data.cloudcertprep import ALL_QUESTIONS as CCP_ALL
            ccp_count = len(CCP_ALL)
        except Exception:
            ccp_count = 0

        ctk.CTkButton(
            scrollable,
            text=f"CloudCertPrep 题库（{ccp_count or '1050+'} 题 · MIT 开源）",
            height=56,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color="#16a085",
            hover_color="#1abc9c",
            command=self._open_cloudcertprep_menu,
        ).pack(pady=(0, 8), fill="x", padx=60)

        try:
            from data.keyword_drill import ALL_QUESTIONS as KD_ALL
            kd_count = len(KD_ALL)
        except Exception:
            kd_count = 0

        ctk.CTkButton(
            scrollable,
            text=f"服务定义辨识（{kd_count} 题 · 看定义选服务名）",
            height=56,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color="#d35400",
            hover_color="#e67e22",
            command=self._open_keyword_drill_menu,
        ).pack(pady=(0, 8), fill="x", padx=60)

        try:
            from data.concept_drill import ALL_QUESTIONS as CD_ALL
            cd_count = len(CD_ALL)
        except Exception:
            cd_count = 0

        ctk.CTkButton(
            scrollable,
            text=f"策略与准则辨识（{cd_count} 题 · 迁移/CAF/场景术语）",
            height=56,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color="#1a5276",
            hover_color="#2874a6",
            command=self._open_concept_drill_menu,
        ).pack(pady=(0, 16), fill="x", padx=60)

        ctk.CTkLabel(
            scrollable,
            text="自建精选题库（320 题）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3498db",
        ).pack(anchor="w", padx=60, pady=(0, 6))

        # ========== 模拟考试（推荐备考） ==========
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

        # ========== 传统模式 ==========
        ctk.CTkLabel(
            scrollable,
            text="传统模式",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888",
        ).pack(anchor="w", padx=60, pady=(0, 6))

        single_count = len(SINGLE_CHOICE_QUESTIONS)
        multi_count = len(MULTI_CHOICE_QUESTIONS)
        total_count = len(ALL_QUESTIONS)

        ctk.CTkButton(
            scrollable,
            text=f"单选题题库（{single_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            command=lambda: self._start_quiz(SINGLE_CHOICE_QUESTIONS, "single"),
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkButton(
            scrollable,
            text=f"多选题题库（{multi_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            fg_color="#2980b9",
            hover_color="#3498db",
            command=lambda: self._start_quiz(MULTI_CHOICE_QUESTIONS, "multi"),
        ).pack(pady=6, fill="x", padx=60)

        ctk.CTkButton(
            scrollable,
            text=f"全部题目（{total_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            command=lambda: self._start_quiz(ALL_QUESTIONS, "all"),
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

        ctk.CTkButton(
            scrollable,
            text="打开错题本（筛选 · Top10 · 单题练习 · 已掌握）",
            height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self._show_wrong_book,
        ).pack(pady=(12, 6), fill="x", padx=60)

        # ========== 按考试领域分类练习 ==========
        ctk.CTkLabel(
            scrollable,
            text="按考试领域分类练习（CLF-C02 官方四大领域）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00b894",
        ).pack(anchor="w", padx=60, pady=(18, 6))

        for domain in DOMAINS:
            count = get_domain_question_count(domain)
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
            text="提示：多选题需要点击「提交答案」按钮后才会显示解析 | 领域练习会混合单选与多选题",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
        ).pack(pady=(20, 10))

        # ========== 我的学习 ==========
        ctk.CTkLabel(
            scrollable,
            text="我的学习",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f39c12",
        ).pack(anchor="w", padx=60, pady=(10, 6))

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