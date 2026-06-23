# -*- coding: utf-8 -*-
"""答题界面、选项交互、完成测试与返回主菜单"""

import time
from typing import List, Dict, Any

import customtkinter as ctk

from data import (
    get_questions_by_domain,
    get_wrong_book_questions,
    shuffle_question_options,
    get_shuffled_questions,
)
from data.progress import (
    get_practice_font_scale,
    record_session,
    set_practice_font_scale,
    update_question_stat,
)
from gui.constants import (
    PRACTICE_FONT_SCALE_MAX,
    PRACTICE_FONT_SCALE_MIN,
    PRACTICE_FONT_SCALE_STEP,
)
from gui.explanation_formatter import render_explanation_body
from gui.term_glossary import annotate_text
from gui.wrapped_label import (
    apply_wraplength,
    measure_option_wraplength,
    measure_question_wraplength,
)


class QuizMixin:
    """练习模式答题流程"""

    def _annotated_explanation(self, text: str) -> str:
        """解析区：英文术语附中文标注，题干与选项保持纯英文。"""
        return annotate_text(text or "")

    def _get_shuffle_info(self, quiz_idx: int, q: Dict[str, Any]) -> Dict[str, Any]:
        """获取（或生成）当前题目的打乱信息，缓存以保证同一会话内稳定"""
        if quiz_idx in self._question_shuffles:
            return self._question_shuffles[quiz_idx]
        info = shuffle_question_options(q)
        self._question_shuffles[quiz_idx] = info
        return info

    def _begin_quiz_session(self, question_list, mode: str):
        """统一入口：销毁菜单、初始化会话、构建答题界面"""
        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()

        self.questions = get_shuffled_questions(question_list)
        self.total = len(self.questions)
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self._option_text_labels = []
        self.is_multi = False
        self.multi_submit_btn = None
        self.current_mode = mode
        self.quiz_start_time = time.time()
        self._question_shuffles.clear()
        self._explain_expanded = False
        self._explanation_full_visible = False
        self._user_font_scale = self._clamp_user_font_scale(get_practice_font_scale())

        self._build_quiz_ui()
        self._load_question(0)
        self._refresh_quiz_typography()

        self.bind("<Configure>", self._on_window_resize)
        self.after(80, self._update_wraplength)
        self.after(220, self._update_wraplength)

    def _start_quiz(self, question_list, mode: str = "all"):
        """从菜单切换到正式答题界面"""
        self._begin_quiz_session(question_list, mode)

    def _start_domain_quiz(self, domain: str):
        """按考试领域启动分类练习"""
        questions = get_questions_by_domain(domain)
        if not questions:
            print(f"警告：领域 '{domain}' 没有题目")
            return
        self._begin_quiz_session(questions, f"domain:{domain}")

    def _start_wrong_book_quiz(self, wrong_ids: List[str], mode: str = "wrong_book"):
        """从错题本启动针对性练习"""
        questions = get_wrong_book_questions(wrong_ids)
        if not questions:
            print("错题本为空，无法开始练习")
            return
        self._begin_quiz_session(questions, mode)

    def _start_custom_quiz(self, question_list: List[Dict[str, Any]], mode: str):
        """自定义练习入口"""
        if not question_list:
            return
        self._begin_quiz_session(question_list, mode)

    def _build_quiz_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        top_frame = ctk.CTkFrame(self, height=55, corner_radius=0)
        top_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        ctk.CTkLabel(
            top_frame,
            text="AWS CLF-C02 练习模式",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(side="left", padx=15, pady=8)

        self.progress_label = ctk.CTkLabel(top_frame, text="", font=ctk.CTkFont(size=14))
        self.progress_label.pack(side="right", padx=15)

        font_ctrl = ctk.CTkFrame(top_frame, fg_color="transparent")
        font_ctrl.pack(side="right", padx=(0, 4))

        self.font_decrease_btn = ctk.CTkButton(
            font_ctrl,
            text="A−",
            width=38,
            height=28,
            fg_color="#2d3a52",
            hover_color="#3d4f6f",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._decrease_quiz_font,
        )
        self.font_decrease_btn.pack(side="left", padx=(0, 4))

        self.font_scale_label = ctk.CTkLabel(
            font_ctrl,
            text="100%",
            width=52,
            font=ctk.CTkFont(size=13),
            text_color="#b8c0d0",
        )
        self.font_scale_label.pack(side="left", padx=2)

        self.font_increase_btn = ctk.CTkButton(
            font_ctrl,
            text="A+",
            width=38,
            height=28,
            fg_color="#2d3a52",
            hover_color="#3d4f6f",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._increase_quiz_font,
        )
        self.font_increase_btn.pack(side="left", padx=(4, 0))
        self._update_font_scale_label()

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        main_frame.bind("<Configure>", lambda e: self._update_wraplength())

        self.info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=8, pady=(8, 4))
        self.info_frame.bind("<Configure>", lambda e: self._update_wraplength())

        self.domain_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
        )
        self.domain_label.pack(fill="x", anchor="w")

        self.question_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=620,
            justify="left",
            anchor="w",
            height=0,
        )
        self.question_label.pack(fill="x", anchor="w", pady=(6, 10))

        self.options_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        self.options_frame.pack(fill="both", expand=True, padx=8, pady=6)
        self.options_frame.bind("<Configure>", lambda e: self._update_wraplength())

        self.explain_frame = ctk.CTkFrame(
            main_frame, fg_color="#1a2030", corner_radius=10, border_width=1, border_color="#2d3a52"
        )
        self.explain_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        explain_header = ctk.CTkFrame(self.explain_frame, fg_color="transparent")
        explain_header.pack(fill="x", padx=12, pady=(10, 6))

        ctk.CTkLabel(
            explain_header,
            text="答案解析",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#7ec8ff",
        ).pack(side="left")

        explain_header_right = ctk.CTkFrame(explain_header, fg_color="transparent")
        explain_header_right.pack(side="right")

        self.explain_toggle_btn = ctk.CTkButton(
            explain_header_right,
            text="收起 ▲",
            width=76,
            height=28,
            fg_color="#2d3a52",
            hover_color="#3d4f6f",
            font=ctk.CTkFont(size=12),
            command=self._toggle_explanation_layout,
        )

        self.explain_status_badge = ctk.CTkLabel(
            explain_header_right,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=6,
            fg_color="#2a3142",
            text_color="#9aa3b5",
            padx=10,
            pady=4,
        )
        self.explain_status_badge.pack(side="right")

        self.explain_meta_frame = ctk.CTkFrame(
            self.explain_frame, fg_color="#232b3d", corner_radius=8
        )
        self.explain_meta_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.explain_your_answer = ctk.CTkLabel(
            self.explain_meta_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#d5dbe8",
            anchor="w",
            justify="left",
            wraplength=400,
        )
        self.explain_your_answer.pack(fill="x", padx=12, pady=(8, 2))

        self.explain_correct_answer = ctk.CTkLabel(
            self.explain_meta_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#6ee7a0",
            anchor="w",
            justify="left",
            wraplength=400,
        )
        self.explain_correct_answer.pack(fill="x", padx=12, pady=(2, 8))

        self.explain_text = ctk.CTkTextbox(
            self.explain_frame,
            font=ctk.CTkFont(size=14),
            wrap="word",
            fg_color="#141a26",
            text_color="#e2e6ef",
            border_width=0,
            activate_scrollbars=True,
        )
        self.explain_text.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        nav_frame = ctk.CTkFrame(self, height=58, corner_radius=0)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        nav_frame.grid_columnconfigure(0, weight=0)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=0)
        nav_frame.grid_columnconfigure(3, weight=0)

        self.top_frame = top_frame
        self.main_frame = main_frame
        self.nav_frame = nav_frame

        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="← 上一题",
            width=105,
            height=34,
            command=self.go_previous,
        )
        self.prev_btn.grid(row=0, column=0, padx=(12, 6), pady=8, sticky="w")

        self.question_counter = ctk.CTkLabel(nav_frame, text="", font=ctk.CTkFont(size=14))
        self.question_counter.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="下一题 →",
            width=105,
            height=34,
            command=self.go_next,
        )
        self.next_btn.grid(row=0, column=2, padx=(6, 6), pady=8, sticky="e")

        self.finish_btn = ctk.CTkButton(
            nav_frame,
            text="完成测试",
            width=95,
            height=34,
            fg_color="#d35400",
            hover_color="#e67e22",
            command=self.finish_quiz,
        )
        self.finish_btn.grid(row=0, column=3, padx=(6, 12), pady=8, sticky="e")

    def _load_question(self, index: int):
        """加载指定索引的题目"""
        if index < 0 or index >= self.total:
            return

        self.current_index = index
        q = self.questions[index]
        self._explanation_full_visible = False

        self.progress_label.configure(text=f"{index + 1} / {self.total}")
        self.question_counter.configure(text=f"第 {index + 1} 题 / 共 {self.total} 题")
        self.domain_label.configure(text=f"领域：{q.get('domain', '未分类')}")
        self.question_label.configure(text=q["question"])

        self.update_idletasks()
        self._update_wraplength()
        self.after(10, self._update_wraplength)
        self.after(60, self._update_wraplength)
        self.after(180, self._update_wraplength)
        self.after(350, self._update_wraplength)

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_widgets.clear()
        self._option_text_labels.clear()

        if self.multi_submit_btn:
            self.multi_submit_btn.destroy()
            self.multi_submit_btn = None

        self.is_multi = len(q["correct_answers"]) > 1
        shuffle_info = self._get_shuffle_info(index, q)
        display_options = shuffle_info["shuffled_options"]
        original_to_display = shuffle_info["original_to_display"]

        stored_original = self.user_answers.get(index, [])
        current_display_answer = [original_to_display.get(c, c) for c in stored_original]

        scale = self._combined_font_scale()
        opt_font_size = max(12, int(13 * scale))
        init_wrap = measure_option_wraplength(self)

        if self.is_multi:
            for letter in ["A", "B", "C", "D", "E"][: len(display_options)]:
                var = ctk.BooleanVar(value=letter in current_display_answer)
                row = ctk.CTkFrame(self.options_frame, fg_color="transparent")
                row.pack(fill="x", padx=6, pady=2)

                indicator = ctk.CTkCheckBox(
                    row,
                    text="",
                    variable=var,
                    width=22,
                    height=22,
                    checkbox_width=16,
                    checkbox_height=16,
                    font=ctk.CTkFont(size=opt_font_size),
                )
                indicator.grid(row=0, column=0, padx=(4, 8), pady=3, sticky="n")

                text_label = ctk.CTkLabel(
                    row,
                    text=display_options[ord(letter) - ord("A")],
                    font=ctk.CTkFont(size=opt_font_size),
                    wraplength=init_wrap,
                    justify="left",
                    anchor="w",
                    height=0,
                )
                text_label.grid(row=0, column=1, sticky="ew", pady=3)
                row.grid_columnconfigure(1, weight=1)

                def _toggle_this(event, var=var, ind=indicator):
                    ind.toggle()

                text_label.bind("<Button-1>", _toggle_this)
                self.option_widgets.append(indicator)
                self._option_text_labels.append(text_label)

            btn_text = "更新答案" if index in self.user_answers else "提交答案"
            self.multi_submit_btn = ctk.CTkButton(
                self.options_frame,
                text=btn_text,
                height=int(34 * scale),
                fg_color="#2980b9",
                hover_color="#3498db",
                font=ctk.CTkFont(size=opt_font_size),
                command=self._submit_multi_answer,
            )
            self.multi_submit_btn.pack(fill="x", padx=20, pady=(10, 4))
        else:
            self.radio_var = ctk.StringVar(
                value=current_display_answer[0] if current_display_answer else ""
            )

            for i, opt_text in enumerate(display_options):
                letter = chr(ord("A") + i)
                row = ctk.CTkFrame(self.options_frame, fg_color="transparent")
                row.pack(fill="x", padx=6, pady=2)

                indicator = ctk.CTkRadioButton(
                    row,
                    text="",
                    variable=self.radio_var,
                    value=letter,
                    width=22,
                    height=22,
                    radiobutton_width=16,
                    radiobutton_height=16,
                    font=ctk.CTkFont(size=opt_font_size),
                    command=self._on_single_change,
                )
                indicator.grid(row=0, column=0, padx=(4, 8), pady=3, sticky="n")

                text_label = ctk.CTkLabel(
                    row,
                    text=opt_text,
                    font=ctk.CTkFont(size=opt_font_size),
                    wraplength=init_wrap,
                    justify="left",
                    anchor="w",
                    height=0,
                )
                text_label.grid(row=0, column=1, sticky="ew", pady=3)
                row.grid_columnconfigure(1, weight=1)

                def _select_this(event, ltr=letter):
                    self.radio_var.set(ltr)
                    self._on_single_change()

                text_label.bind("<Button-1>", _select_this)
                self.option_widgets.append(indicator)
                self._option_text_labels.append(text_label)

        self._update_explanation_panel()
        self.prev_btn.configure(state="normal" if index > 0 else "disabled")
        self.next_btn.configure(state="normal" if index < self.total - 1 else "disabled")

    def _on_single_change(self):
        """单选题选择变化（将显示字母转回原始字母后存储）"""
        selected_display = self.radio_var.get()
        if selected_display:
            shuffle_info = self._question_shuffles.get(self.current_index, {})
            display_to_original = shuffle_info.get("display_to_original", {})
            original_letter = display_to_original.get(selected_display, selected_display)
            self.user_answers[self.current_index] = [original_letter]
            self._update_explanation_panel()

    def _submit_multi_answer(self):
        """多选题提交：记录答案并显示完整解析"""
        if not self.is_multi or not self.option_widgets:
            return

        shuffle_info = self._question_shuffles.get(self.current_index, {})
        display_to_original = shuffle_info.get("display_to_original", {})

        selected_display = []
        for i, widget in enumerate(self.option_widgets):
            if isinstance(widget, ctk.CTkCheckBox):
                letter = chr(ord("A") + i)
                if widget.get():
                    selected_display.append(letter)

        selected_original = sorted(display_to_original.get(d, d) for d in selected_display)
        self.user_answers[self.current_index] = selected_original
        self._update_explanation_panel(force_full_explanation=True)

    def _clamp_user_font_scale(self, scale: float) -> float:
        return max(
            PRACTICE_FONT_SCALE_MIN,
            min(PRACTICE_FONT_SCALE_MAX, round(scale, 2)),
        )

    def _window_font_scale(self) -> float:
        try:
            return max(0.65, min(1.15, self.winfo_width() / 1000.0))
        except Exception:
            return 1.0

    def _combined_font_scale(self) -> float:
        return self._window_font_scale() * getattr(self, "_user_font_scale", 1.0)

    def _update_font_scale_label(self) -> None:
        if not hasattr(self, "font_scale_label"):
            return
        pct = int(round(getattr(self, "_user_font_scale", 1.0) * 100))
        self.font_scale_label.configure(text=f"{pct}%")
        at_min = self._user_font_scale <= PRACTICE_FONT_SCALE_MIN
        at_max = self._user_font_scale >= PRACTICE_FONT_SCALE_MAX
        self.font_decrease_btn.configure(state="disabled" if at_min else "normal")
        self.font_increase_btn.configure(state="disabled" if at_max else "normal")

    def _change_quiz_font(self, delta: float) -> None:
        new_scale = self._clamp_user_font_scale(self._user_font_scale + delta)
        if new_scale == self._user_font_scale:
            return
        self._user_font_scale = new_scale
        set_practice_font_scale(new_scale)
        self._refresh_quiz_typography()

    def _decrease_quiz_font(self) -> None:
        self._change_quiz_font(-PRACTICE_FONT_SCALE_STEP)

    def _increase_quiz_font(self) -> None:
        self._change_quiz_font(PRACTICE_FONT_SCALE_STEP)

    def _refresh_quiz_typography(self, *, refresh_explanation: bool = True) -> None:
        """根据窗口与用户字体偏好，刷新题目/选项/解析字号。"""
        scale = self._combined_font_scale()
        self._update_font_scale_label()

        try:
            domain_size = max(11, int(12 * scale))
            question_size = max(13, int(15 * scale))
            option_size = max(12, int(13 * scale))
            button_font_size = max(12, int(13 * scale))
            small_size = max(11, int(12 * scale))
            explain_body_size = max(13, int(14 * scale))
            badge_size = max(12, int(13 * scale))
            meta_size = max(12, int(13 * scale))
            btn_height = max(30, int(34 * scale))
            nav_btn_width = max(80, int(105 * scale))

            if hasattr(self, "domain_label") and self.domain_label.winfo_exists():
                self.domain_label.configure(font=ctk.CTkFont(size=domain_size))
            if hasattr(self, "question_label") and self.question_label.winfo_exists():
                self.question_label.configure(
                    font=ctk.CTkFont(size=question_size, weight="bold"),
                )
            if hasattr(self, "explain_status_badge") and self.explain_status_badge.winfo_exists():
                self.explain_status_badge.configure(font=ctk.CTkFont(size=badge_size, weight="bold"))
            if hasattr(self, "explain_your_answer") and self.explain_your_answer.winfo_exists():
                self.explain_your_answer.configure(font=ctk.CTkFont(size=meta_size))
            if hasattr(self, "explain_correct_answer") and self.explain_correct_answer.winfo_exists():
                self.explain_correct_answer.configure(font=ctk.CTkFont(size=meta_size))

            if hasattr(self, "prev_btn") and self.prev_btn.winfo_exists():
                self.prev_btn.configure(
                    width=nav_btn_width,
                    height=btn_height,
                    font=ctk.CTkFont(size=button_font_size),
                )
            if hasattr(self, "next_btn") and self.next_btn.winfo_exists():
                self.next_btn.configure(
                    width=nav_btn_width,
                    height=btn_height,
                    font=ctk.CTkFont(size=button_font_size),
                )
            if hasattr(self, "finish_btn") and self.finish_btn.winfo_exists():
                self.finish_btn.configure(
                    width=max(75, int(95 * scale)),
                    height=btn_height,
                    font=ctk.CTkFont(size=button_font_size),
                )
            if hasattr(self, "question_counter") and self.question_counter.winfo_exists():
                self.question_counter.configure(font=ctk.CTkFont(size=small_size))
            if hasattr(self, "progress_label") and self.progress_label.winfo_exists():
                self.progress_label.configure(font=ctk.CTkFont(size=small_size))

            if self.multi_submit_btn and self.multi_submit_btn.winfo_exists():
                self.multi_submit_btn.configure(
                    height=btn_height,
                    font=ctk.CTkFont(size=button_font_size),
                )

            opt_font = ctk.CTkFont(size=option_size)
            for lbl in getattr(self, "_option_text_labels", []):
                try:
                    if lbl and lbl.winfo_exists():
                        lbl.configure(font=opt_font)
                except Exception:
                    pass
            for w in getattr(self, "option_widgets", []):
                try:
                    if w and w.winfo_exists():
                        w.configure(font=opt_font)
                except Exception:
                    pass

            self._update_wraplength()

            if refresh_explanation and self._explanation_full_visible:
                self._update_explanation_panel(
                    force_full_explanation=True,
                    preserve_layout=True,
                )
            elif hasattr(self, "explain_text") and self.explain_text.winfo_exists():
                self.explain_text.configure(font=ctk.CTkFont(size=explain_body_size))
        except Exception:
            pass

    def _set_explanation_toggle_visible(self, visible: bool) -> None:
        if visible:
            self.explain_toggle_btn.pack(side="right", padx=(0, 8))
        else:
            self.explain_toggle_btn.pack_forget()

    def _apply_explanation_layout(self, expanded: bool) -> None:
        """展开：解析占满主区域；收起：题目+选项在上、解析在下。"""
        self._explain_expanded = expanded
        self.explain_toggle_btn.configure(
            text="收起 ▲" if expanded else "展开 ▼",
        )

        self.explain_frame.pack_forget()
        if expanded:
            self.info_frame.pack_forget()
            self.options_frame.pack_forget()
            self.explain_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))
        else:
            self.info_frame.pack(fill="x", padx=8, pady=(8, 4))
            self.options_frame.pack(fill="both", expand=True, padx=8, pady=6)
            self.explain_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))

    def _toggle_explanation_layout(self) -> None:
        self._apply_explanation_layout(not self._explain_expanded)

    def _set_explanation_placeholder(
        self, badge_text: str, badge_fg: str, badge_text_color: str, hint: str,
        *, preserve_layout: bool = False,
    ) -> None:
        """未作答 / 待提交时的解析区占位状态。"""
        self.explain_status_badge.configure(
            text=badge_text, fg_color=badge_fg, text_color=badge_text_color,
        )
        self.explain_your_answer.configure(text="")
        self.explain_correct_answer.configure(text="")
        self.explain_meta_frame.pack_forget()
        self._set_explanation_toggle_visible(False)
        self._explanation_full_visible = False
        if not preserve_layout:
            self._apply_explanation_layout(expanded=False)

        scale = self._combined_font_scale()
        inner = self.explain_text._textbox
        inner.configure(state="normal")
        inner.delete("1.0", "end")
        inner.tag_configure(
            "muted",
            foreground="#9aa3b5",
            font=("Microsoft YaHei UI", max(12, int(13 * scale))),
            spacing1=4,
            spacing3=6,
        )
        inner.insert("end", hint, "muted")
        inner.configure(state="disabled")

    def _update_explanation_panel(
        self, force_full_explanation=False, preserve_layout: bool = False,
    ):
        """更新解析面板（原始字母映射回显示字母）"""
        q = self.questions[self.current_index]
        user_ans_original = self.user_answers.get(self.current_index, [])

        if not user_ans_original:
            hint = (
                "请先选择答案。"
                if not self.is_multi
                else "请先勾选选项，然后点击「提交答案」查看解析。"
            )
            self._set_explanation_placeholder(
                "待作答", "#2a3142", "#9aa3b5", hint,
                preserve_layout=preserve_layout,
            )
            return

        shuffle_info = self._question_shuffles.get(self.current_index, {})
        original_to_display = shuffle_info.get("original_to_display", {})

        user_ans_display = [original_to_display.get(c, c) for c in user_ans_original]
        correct_original = q.get("correct_answers", [])
        correct_display = [original_to_display.get(c, c) for c in correct_original]

        show_full = force_full_explanation or self._explanation_full_visible
        if self.is_multi and not show_full:
            self._set_explanation_placeholder(
                "待提交",
                "#3d3420",
                "#ffd966",
                f"已选：{', '.join(user_ans_display)}\n\n"
                "点击「提交答案」或「更新答案」后，将显示正误与详细解析。",
                preserve_layout=preserve_layout,
            )
            return

        is_correct = set(user_ans_original) == set(correct_original)
        if is_correct:
            badge_text, badge_fg, badge_color = "回答正确", "#1a3d2e", "#6ee7a0"
        else:
            badge_text, badge_fg, badge_color = "回答错误", "#3d2228", "#f5a8a8"

        self.explain_status_badge.configure(
            text=badge_text, fg_color=badge_fg, text_color=badge_color,
        )
        self.explain_meta_frame.pack(fill="x", padx=12, pady=(0, 8), before=self.explain_text)
        self.explain_your_answer.configure(
            text=f"你的答案：{', '.join(user_ans_display)}",
        )
        self.explain_correct_answer.configure(
            text=f"正确答案：{', '.join(correct_display)}",
        )

        explanation = self._annotated_explanation(q.get("explanation", "暂无解析"))
        render_explanation_body(
            self.explain_text, explanation, scale=self._combined_font_scale(),
        )

        self._explanation_full_visible = True
        self._set_explanation_toggle_visible(True)
        if not preserve_layout:
            self._apply_explanation_layout(expanded=True)

    def _on_window_resize(self, event):
        """窗口大小变化时动态调整字体、间距和按钮大小"""
        if event.widget != self:
            return

        try:
            if hasattr(self, "question_label") and self.question_label.winfo_exists():
                self.question_label.configure(justify="left", anchor="w")
                self.question_label.update_idletasks()

            self._refresh_quiz_typography()

            width = self.winfo_width()
            meta_wrap = max(260, int(width - 180))
            if hasattr(self, "explain_your_answer") and self.explain_your_answer.winfo_exists():
                self.explain_your_answer.configure(wraplength=meta_wrap)
            if hasattr(self, "explain_correct_answer") and self.explain_correct_answer.winfo_exists():
                self.explain_correct_answer.configure(wraplength=meta_wrap)

            self.after(5, self._update_wraplength)
            self.after(40, self._update_wraplength)
            self.after(160, self._update_wraplength)
        except Exception:
            pass

    def _update_wraplength(self):
        """按选项区域实际宽度更新换行，避免文字横向溢出或被裁切。"""
        q_wrap = measure_question_wraplength(self)
        opt_wrap = measure_option_wraplength(self)

        try:
            if hasattr(self, "question_label") and self.question_label.winfo_exists():
                apply_wraplength(self.question_label, q_wrap)
        except Exception:
            pass

        for lbl in getattr(self, "_option_text_labels", []):
            if lbl is None:
                continue
            try:
                if lbl.winfo_exists():
                    apply_wraplength(lbl, opt_wrap)
            except Exception:
                pass

        try:
            self.update_idletasks()
        except Exception:
            pass

    def go_previous(self):
        if self.current_index > 0:
            self._load_question(self.current_index - 1)

    def go_next(self):
        if self.current_index < self.total - 1:
            self._load_question(self.current_index + 1)

    def finish_quiz(self):
        """完成测试，显示总结 + 持久化进度"""
        correct_count = 0
        answered_count = 0

        for i, q in enumerate(self.questions):
            user = self.user_answers.get(i, [])
            if user:
                answered_count += 1
                if set(user) == set(q["correct_answers"]):
                    correct_count += 1

        answered_for_rate = answered_count if answered_count > 0 else 1
        percentage = (correct_count / answered_for_rate) * 100 if answered_count > 0 else 0.0
        duration = int(time.time() - self.quiz_start_time) if self.quiz_start_time else 0

        try:
            record_session(
                self.current_mode, self.total, correct_count, duration, answered=answered_count
            )
            for i, q in enumerate(self.questions):
                user_ans = self.user_answers.get(i, [])
                if not user_ans:
                    continue
                qid = q.get("id")
                if not qid:
                    continue
                is_correct = set(user_ans) == set(q.get("correct_answers", []))
                update_question_stat(qid, is_correct, user_ans)
        except Exception as e:
            print(f"[进度保存警告] {e}")

        summary = ctk.CTkToplevel(self)
        summary.title("测试完成")
        summary.geometry("520x360")
        summary.grab_set()

        ctk.CTkLabel(
            summary,
            text="本次练习完成！",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(18, 6))

        progress_text = f"作答进度：{answered_count} / {self.total} 题"
        if answered_count == self.total:
            progress_text = f"已完成全部 {self.total} 题"
        ctk.CTkLabel(
            summary,
            text=progress_text,
            font=ctk.CTkFont(size=14),
            text_color="#888888",
        ).pack(pady=(0, 4))

        score_denominator = answered_count if answered_count > 0 else self.total
        ctk.CTkLabel(
            summary,
            text=f"得分：{correct_count} / {score_denominator}",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(pady=6)

        rate_note = "（基于已回答题目）" if answered_count > 0 else "（未作答任何题目）"
        ctk.CTkLabel(
            summary,
            text=f"正确率：{percentage:.1f}% {rate_note}",
            font=ctk.CTkFont(size=16),
        ).pack(pady=2)

        ctk.CTkLabel(
            summary,
            text=f"用时：{duration // 60}分{duration % 60}秒",
            font=ctk.CTkFont(size=14),
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            summary,
            text="✓ 进度已自动保存（历史记录 + 错题统计）",
            font=ctk.CTkFont(size=13),
            text_color="#2ecc71",
        ).pack(pady=(6, 12))

        ctk.CTkButton(
            summary, text="关闭", width=110, height=36, command=summary.destroy
        ).pack(side="left", padx=8, pady=10)

        ctk.CTkButton(
            summary,
            text="返回主菜单",
            width=130,
            height=36,
            fg_color="#2980b9",
            hover_color="#3498db",
            command=lambda: (summary.destroy(), self._return_to_menu()),
        ).pack(side="left", padx=8, pady=10)

    def _return_to_menu(self):
        """从答题界面安全返回主菜单"""
        for frame_attr in ("top_frame", "main_frame", "nav_frame"):
            frame = getattr(self, frame_attr, None)
            if frame and frame.winfo_exists():
                frame.destroy()

        try:
            self.unbind("<Configure>")
        except Exception:
            pass

        self.questions = []
        self.total = 0
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self._option_text_labels = []
        self.is_multi = False
        self.multi_submit_btn = None
        self.current_mode = "all"
        self.quiz_start_time = 0.0
        self._explain_expanded = False
        self._explanation_full_visible = False
        self.top_frame = None
        self.main_frame = None
        self.nav_frame = None

        self._build_menu_ui()