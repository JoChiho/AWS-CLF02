# -*- coding: utf-8 -*-
"""CLF-C02 模拟考试模式（65 题 / 90 分钟 / 严格无解析）"""

import time
from typing import List, Dict, Any

import customtkinter as ctk
from tkinter import messagebox


from data.mock_exam import (
    MOCK_EXAM_DURATION_SEC,
    MOCK_EXAM_PASS_PERCENT,
    MOCK_EXAM_QUESTION_COUNT,
    score_mock_exam,
    select_mock_exam_questions,
)
from data.progress import record_session, update_question_stat
from gui.constants import DOMAIN_DISPLAY_NAMES, MOCK_EXAM_DURATION_MIN
from gui.wrapped_label import (
    apply_wraplength,
    measure_option_wraplength,
    measure_question_wraplength,
)


class MockExamMixin:
    """模拟考试流程（与练习模式独立，交卷后统一出解析）"""

    def _show_mock_exam_intro(self):
        """模拟考试规则说明与确认"""
        win = ctk.CTkToplevel(self)
        win.title("模拟考试说明")
        win.geometry("560x420")
        win.grab_set()
        win.transient(self)

        ctk.CTkLabel(
            win,
            text="CLF-C02 模拟考试",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(pady=(18, 8))

        rules = (
            f"• 题量：{MOCK_EXAM_QUESTION_COUNT} 题（按官方四大领域权重随机抽题）\n"
            f"• 时限：{MOCK_EXAM_DURATION_MIN} 分钟倒计时，到时自动交卷\n"
            f"• 严格模式：答题期间不显示解析与正误\n"
            f"• 及格线：{MOCK_EXAM_PASS_PERCENT:.0f}%（{int(MOCK_EXAM_QUESTION_COUNT * MOCK_EXAM_PASS_PERCENT / 100)} 题以上）\n"
            "• 交卷后：统一查看得分、领域分项与错题解析\n"
            "• 进度将写入历史记录（mode = mock_exam）"
        )
        ctk.CTkLabel(
            win,
            text=rules,
            font=ctk.CTkFont(size=14),
            justify="left",
        ).pack(padx=28, pady=12, anchor="w")

        btn_row = ctk.CTkFrame(win, fg_color="transparent")
        btn_row.pack(pady=20)

        def on_start():
            win.destroy()
            self._start_mock_exam()

        ctk.CTkButton(
            btn_row,
            text="开始模拟考试",
            width=160,
            height=40,
            fg_color="#e67e22",
            hover_color="#f39c12",
            command=on_start,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_row,
            text="取消",
            width=100,
            height=40,
            command=win.destroy,
        ).pack(side="left", padx=10)

    def _start_mock_exam(self):
        """启动一场新的模拟考试"""
        questions = select_mock_exam_questions(bank_id=self.current_bank_id)
        if len(questions) < MOCK_EXAM_QUESTION_COUNT:
            messagebox.showerror(
                "无法开始",
                f"题库不足以组成 {MOCK_EXAM_QUESTION_COUNT} 题模拟考试（当前仅 {len(questions)} 题）。",
            )
            return

        if getattr(self, "menu_frame", None) and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()

        self._mock_exam_active = True
        self.questions = questions
        self.total = len(questions)
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self._option_text_labels = []
        self.is_multi = False
        self.multi_submit_btn = None
        self.current_mode = "mock_exam"
        self.quiz_start_time = time.time()
        self._question_shuffles.clear()
        self._mock_timer_remaining = MOCK_EXAM_DURATION_SEC
        self._mock_timer_job = None
        self._mock_submitted = False

        self.title("AWS CLF-C02 认证考试刷题系统 - 模拟考试")
        self._build_mock_exam_ui()
        self._load_mock_question(0)
        self._mock_start_timer()

        self.bind("<Configure>", self._mock_on_window_resize)
        self.after(80, self._mock_update_wraplength)
        self.after(220, self._mock_update_wraplength)

    def _mock_start_timer(self):
        self._mock_tick_timer()

    def _mock_cancel_timer(self):
        if self._mock_timer_job is not None:
            try:
                self.after_cancel(self._mock_timer_job)
            except Exception:
                pass
            self._mock_timer_job = None

    def _mock_tick_timer(self):
        if not getattr(self, "_mock_exam_active", False) or self._mock_submitted:
            return

        if self._mock_timer_remaining <= 0:
            self._mock_submit_exam(auto=True)
            return

        mins, secs = divmod(self._mock_timer_remaining, 60)
        color = "#e74c3c" if self._mock_timer_remaining <= 300 else "#f39c12"
        if hasattr(self, "_mock_timer_label") and self._mock_timer_label.winfo_exists():
            self._mock_timer_label.configure(
                text=f"⏱ 剩余 {mins:02d}:{secs:02d}",
                text_color=color if self._mock_timer_remaining <= 600 else "#2ecc71",
            )

        self._mock_timer_remaining -= 1
        self._mock_timer_job = self.after(1000, self._mock_tick_timer)

    def _build_mock_exam_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        top_frame = ctk.CTkFrame(self, height=55, corner_radius=0)
        top_frame.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            top_frame,
            text="模拟考试（严格模式 · 无解析）",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#e67e22",
        ).pack(side="left", padx=15, pady=8)

        self._mock_timer_label = ctk.CTkLabel(
            top_frame,
            text="⏱ 剩余 90:00",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2ecc71",
        )
        self._mock_timer_label.pack(side="right", padx=12)

        self.progress_label = ctk.CTkLabel(top_frame, text="", font=ctk.CTkFont(size=14))
        self.progress_label.pack(side="right", padx=8)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        main_frame.bind("<Configure>", lambda e: self._mock_update_wraplength())

        self.info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=8, pady=(8, 4))
        self.info_frame.bind("<Configure>", lambda e: self._mock_update_wraplength())

        self.domain_label = ctk.CTkLabel(
            self.info_frame, text="", font=ctk.CTkFont(size=12), text_color="#888888"
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
        self.question_label.pack(fill="x", anchor="w", pady=(6, 6))

        self._mock_hint_label = ctk.CTkLabel(
            self.info_frame,
            text="提示：答题期间不显示解析。多选题勾选后切换题号会自动保存作答。",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
        )
        self._mock_hint_label.pack(fill="x", anchor="w", pady=(0, 6))

        self.options_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        self.options_frame.pack(fill="both", expand=True, padx=8, pady=6)
        self.options_frame.bind("<Configure>", lambda e: self._mock_update_wraplength())

        nav_frame = ctk.CTkFrame(self, height=58, corner_radius=0)
        nav_frame.grid(row=2, column=0, sticky="ew")
        nav_frame.grid_columnconfigure(0, weight=0)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=0)
        nav_frame.grid_columnconfigure(3, weight=0)

        self.top_frame = top_frame
        self.main_frame = main_frame
        self.nav_frame = nav_frame

        self.prev_btn = ctk.CTkButton(
            nav_frame, text="← 上一题", width=105, height=34, command=self._mock_go_previous
        )
        self.prev_btn.grid(row=0, column=0, padx=(12, 6), pady=8, sticky="w")

        self.question_counter = ctk.CTkLabel(nav_frame, text="", font=ctk.CTkFont(size=14))
        self.question_counter.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        self.next_btn = ctk.CTkButton(
            nav_frame, text="下一题 →", width=105, height=34, command=self._mock_go_next
        )
        self.next_btn.grid(row=0, column=2, padx=(6, 6), pady=8, sticky="e")

        self.finish_btn = ctk.CTkButton(
            nav_frame,
            text="交卷",
            width=95,
            height=34,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=lambda: self._mock_submit_exam(auto=False),
        )
        self.finish_btn.grid(row=0, column=3, padx=(6, 12), pady=8, sticky="e")

    def _mock_get_shuffle_info(self, quiz_idx: int, q: Dict[str, Any]) -> Dict[str, Any]:
        if quiz_idx in self._question_shuffles:
            return self._question_shuffles[quiz_idx]
        info = self._get_bank().shuffle_question_options(q)
        self._question_shuffles[quiz_idx] = info
        return info

    def _mock_capture_current_answer(self):
        """将当前题目的选择写入 user_answers（原始字母）"""
        if self.current_index < 0 or self.current_index >= self.total:
            return

        shuffle_info = self._question_shuffles.get(self.current_index, {})
        display_to_original = shuffle_info.get("display_to_original", {})

        if self.is_multi:
            selected_display = []
            for i, widget in enumerate(self.option_widgets):
                if isinstance(widget, ctk.CTkCheckBox) and widget.get():
                    selected_display.append(chr(ord("A") + i))
            if selected_display:
                original = sorted(display_to_original.get(d, d) for d in selected_display)
                self.user_answers[self.current_index] = original
            elif self.current_index in self.user_answers:
                del self.user_answers[self.current_index]
        else:
            if hasattr(self, "radio_var"):
                selected_display = self.radio_var.get()
                if selected_display:
                    original = display_to_original.get(selected_display, selected_display)
                    self.user_answers[self.current_index] = [original]
                elif self.current_index in self.user_answers:
                    del self.user_answers[self.current_index]

    def _load_mock_question(self, index: int):
        if index < 0 or index >= self.total:
            return

        self._mock_capture_current_answer()

        self.current_index = index
        q = self.questions[index]

        self.progress_label.configure(text=f"{index + 1} / {self.total}")
        self.question_counter.configure(text=f"第 {index + 1} 题 / 共 {self.total} 题")

        is_multi = len(q["correct_answers"]) > 1
        type_hint = "（多选题）" if is_multi else "（单选题）"
        domain_cn = DOMAIN_DISPLAY_NAMES.get(q.get("domain", ""), q.get("domain", "未分类"))
        self.domain_label.configure(text=f"领域：{domain_cn} {type_hint}")
        # 模拟考试保持纯英文题干，不附加中文服务名标注（贴近真实考试）
        self.question_label.configure(text=q["question"])

        self.update_idletasks()
        self._mock_update_wraplength()
        self.after(10, self._mock_update_wraplength)
        self.after(60, self._mock_update_wraplength)

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_widgets.clear()
        self._option_text_labels.clear()
        self.multi_submit_btn = None

        self.is_multi = is_multi
        shuffle_info = self._mock_get_shuffle_info(index, q)
        display_options = shuffle_info["shuffled_options"]
        original_to_display = shuffle_info["original_to_display"]

        stored_original = self.user_answers.get(index, [])
        current_display = [original_to_display.get(c, c) for c in stored_original]

        scale = max(0.7, min(1.1, self.winfo_width() / 1000.0))
        opt_font_size = int(13 * scale)
        init_wrap = measure_option_wraplength(self)

        if self.is_multi:
            for letter in ["A", "B", "C", "D", "E"][: len(display_options)]:
                var = ctk.BooleanVar(value=letter in current_display)
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

                def _toggle(event, var=var, ind=indicator):
                    ind.toggle()

                text_label.bind("<Button-1>", _toggle)
                self.option_widgets.append(indicator)
                self._option_text_labels.append(text_label)
        else:
            self.radio_var = ctk.StringVar(value=current_display[0] if current_display else "")

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

                def _select(event, ltr=letter):
                    self.radio_var.set(ltr)

                text_label.bind("<Button-1>", _select)
                self.option_widgets.append(indicator)
                self._option_text_labels.append(text_label)

        answered = index in self.user_answers
        status = "已作答" if answered else "未作答"
        self._mock_hint_label.configure(
            text=f"本题状态：{status} | 答题期间不显示解析。切换题号会自动保存当前选择。"
        )

        self.prev_btn.configure(state="normal" if index > 0 else "disabled")
        self.next_btn.configure(state="normal" if index < self.total - 1 else "disabled")

    def _mock_go_previous(self):
        if self.current_index > 0:
            self._load_mock_question(self.current_index - 1)

    def _mock_go_next(self):
        if self.current_index < self.total - 1:
            self._load_mock_question(self.current_index + 1)

    def _mock_submit_exam(self, auto: bool = False):
        if self._mock_submitted:
            return

        if not auto:
            self._mock_capture_current_answer()
            answered_count = sum(1 for i in range(self.total) if self.user_answers.get(i))
            unanswered = self.total - answered_count
            msg = f"确定要交卷吗？\n\n已作答：{self.total - unanswered} / {self.total}"
            if unanswered > 0:
                msg += f"\n仍有 {unanswered} 题未作答（将计为错误）。"
            if not messagebox.askyesno("确认交卷", msg):
                return

        self._mock_submitted = True
        self._mock_cancel_timer()
        self._mock_capture_current_answer()

        duration = int(time.time() - self.quiz_start_time) if self.quiz_start_time else 0
        result = score_mock_exam(self.questions, self.user_answers)

        try:
            record_session(
                "mock_exam",
                result["total"],
                result["correct_count"],
                duration,
                answered=result["answered_count"],
                bank_id=self.current_bank_id,
            )
            for i, q in enumerate(self.questions):
                user_ans = self.user_answers.get(i, [])
                if not user_ans:
                    continue
                qid = q.get("id")
                if not qid:
                    continue
                is_correct = set(user_ans) == set(q.get("correct_answers", []))
                update_question_stat(
                    qid, is_correct, user_ans, bank_id=self.current_bank_id
                )
            saved = True
        except Exception as e:
            print(f"[进度保存警告] {e}")
            saved = False

        self._mock_show_results(result, duration, saved, auto=auto)

    def _mock_show_results(
        self,
        result: Dict[str, Any],
        duration: int,
        saved: bool,
        auto: bool = False,
    ):
        win = ctk.CTkToplevel(self)
        win.title("模拟考试成绩")
        win.geometry("720x640")
        win.grab_set()

        title = "考试时间到，已自动交卷" if auto else "模拟考试结束"
        ctk.CTkLabel(win, text=title, font=ctk.CTkFont(size=20, weight="bold")).pack(
            pady=(14, 6)
        )

        pass_text = "✅ 及格" if result["passed"] else "❌ 未及格"
        pass_color = "#2ecc71" if result["passed"] else "#e74c3c"
        ctk.CTkLabel(
            win,
            text=f"{pass_text}（及格线 {MOCK_EXAM_PASS_PERCENT:.0f}%）",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=pass_color,
        ).pack(pady=4)

        ctk.CTkLabel(
            win,
            text=(
                f"得分：{result['correct_count']} / {result['total']}  "
                f"正确率：{result['percentage']:.1f}%\n"
                f"已作答：{result['answered_count']} 题  "
                f"用时：{duration // 60}分{duration % 60}秒"
            ),
            font=ctk.CTkFont(size=15),
        ).pack(pady=6)

        if saved:
            ctk.CTkLabel(
                win,
                text="✓ 进度已自动保存",
                font=ctk.CTkFont(size=13),
                text_color="#2ecc71",
            ).pack(pady=(0, 8))

        ctk.CTkLabel(
            win,
            text="领域分项正确率",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=20, pady=(8, 4))

        domain_box = ctk.CTkTextbox(win, height=110, font=ctk.CTkFont(size=13))
        domain_box.pack(fill="x", padx=20, pady=(0, 8))
        for domain, st in result["domain_stats"].items():
            if st["total"] == 0:
                continue
            name = DOMAIN_DISPLAY_NAMES.get(domain, domain)
            acc = st["correct"] / st["total"] * 100
            domain_box.insert(
                "end",
                f"  {name:<12}  {st['correct']}/{st['total']}  ({acc:.0f}%)\n",
            )
        domain_box.configure(state="disabled")

        ctk.CTkLabel(
            win,
            text=f"错题与未作答（共 {len(result['wrong_items'])} 题）",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=20, pady=(4, 4))

        detail = ctk.CTkTextbox(win, font=ctk.CTkFont(size=12), wrap="word")
        detail.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        from gui.explanation_formatter import format_answer_labels_with_text

        for item in result["wrong_items"]:
            qid = item.get("id") or "?"
            opts = item.get("options") or []
            if item.get("unanswered"):
                ua = "未作答"
            else:
                ua = format_answer_labels_with_text(
                    item.get("user_answer") or [],
                    options=opts,
                )
            ca = format_answer_labels_with_text(
                item.get("correct_answers") or [],
                options=opts,
            )
            detail.insert("end", f"【第{item['index']}题 · {qid}】\n")
            detail.insert("end", f"{item['question'][:120]}...\n" if len(item["question"]) > 120 else f"{item['question']}\n")
            detail.insert("end", f"你的答案：{ua}\n")
            detail.insert("end", f"正确答案：{ca}\n")
            exp = item.get("explanation", "")
            if exp:
                detail.insert("end", f"解析：{exp[:300]}{'...' if len(exp) > 300 else ''}\n")
            detail.insert("end", "\n")
        detail.configure(state="disabled")

        btn_row = ctk.CTkFrame(win, fg_color="transparent")
        btn_row.pack(pady=10)

        ctk.CTkButton(
            btn_row,
            text="关闭",
            width=100,
            command=win.destroy,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row,
            text="返回主菜单",
            width=130,
            fg_color="#2980b9",
            hover_color="#3498db",
            command=lambda: (win.destroy(), self._mock_return_to_menu()),
        ).pack(side="left", padx=8)

    def _mock_return_to_menu(self):
        """清理模拟考试界面并返回主菜单"""
        self._mock_cancel_timer()
        self._mock_exam_active = False
        self._mock_submitted = False

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
        self._question_shuffles.clear()
        self.top_frame = None
        self.main_frame = None
        self.nav_frame = None

        self.title("AWS CLF-C02 认证考试刷题系统 - 练习模式")
        if self._is_cloudcertprep():
            self._build_cloudcertprep_menu_ui()
        elif self._is_keyword_drill():
            self._build_keyword_drill_menu_ui()
        else:
            self._build_menu_ui()

    def _mock_on_window_resize(self, event):
        if event.widget != self or not getattr(self, "_mock_exam_active", False):
            return

        scale = max(0.65, min(1.15, self.winfo_width() / 1000.0))
        try:
            question_size = int(15 * scale)
            option_size = int(13 * scale)
            button_font_size = int(13 * scale)
            btn_height = int(34 * scale)
            nav_btn_width = int(105 * scale)

            self.question_label.configure(font=ctk.CTkFont(size=question_size, weight="bold"))
            self.after(5, self._mock_update_wraplength)
            self.after(40, self._mock_update_wraplength)

            self.prev_btn.configure(
                width=max(80, nav_btn_width),
                height=btn_height,
                font=ctk.CTkFont(size=button_font_size),
            )
            self.next_btn.configure(
                width=max(80, nav_btn_width),
                height=btn_height,
                font=ctk.CTkFont(size=button_font_size),
            )
            self.finish_btn.configure(
                width=max(75, int(95 * scale)),
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
        except Exception:
            pass

    def _mock_update_wraplength(self):
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