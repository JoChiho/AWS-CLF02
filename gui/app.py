# -*- coding: utf-8 -*-
"""
AWS CLF-C02 图形界面刷题系统（练习模式）

特点：
- 鼠标点击选择答案
- 自由翻阅上一题 / 下一题
- 每选择/修改答案后立即显示详细解析
"""

import customtkinter as ctk
from typing import List, Dict

from data import ALL_QUESTIONS, SINGLE_CHOICE_QUESTIONS, MULTI_CHOICE_QUESTIONS


class CLFQuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 窗口设置 - 支持响应式
        self.title("AWS CLF-C02 认证考试刷题系统 - 练习模式")
        self.geometry("1000x720")
        self.minsize(820, 620)
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 当前使用的题库
        self.questions = []
        self.total = 0

        # 用户答案存储
        self.user_answers: Dict[int, List[str]] = {}
        self.current_index = 0

        self.option_widgets: List[ctk.CTkRadioButton | ctk.CTkCheckBox] = []
        self.is_multi = False
        self.multi_submit_btn: ctk.CTkButton | None = None

        # 先显示选择题库的菜单界面
        self._build_menu_ui()

    # ==================== 菜单界面 ====================
    def _build_menu_ui(self):
        """题库选择主菜单"""
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill="both", expand=True, padx=40, pady=40)

        title = ctk.CTkLabel(
            self.menu_frame,
            text="AWS CLF-C02 刷题系统",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(20, 10))

        subtitle = ctk.CTkLabel(
            self.menu_frame,
            text="请选择你要练习的题库",
            font=ctk.CTkFont(size=16)
        )
        subtitle.pack(pady=(0, 30))

        # 单选题按钮
        btn1 = ctk.CTkButton(
            self.menu_frame,
            text="单选题题库（46题）",
            height=55,
            font=ctk.CTkFont(size=18),
            command=lambda: self._start_quiz(SINGLE_CHOICE_QUESTIONS)
        )
        btn1.pack(pady=12, fill="x", padx=60)

        # 多选题按钮（用户重点想测试）
        btn2 = ctk.CTkButton(
            self.menu_frame,
            text="多选题题库（49题）",
            height=55,
            font=ctk.CTkFont(size=18),
            fg_color="#2980b9",
            hover_color="#3498db",
            command=lambda: self._start_quiz(MULTI_CHOICE_QUESTIONS)
        )
        btn2.pack(pady=12, fill="x", padx=60)

        # 全部题目
        btn3 = ctk.CTkButton(
            self.menu_frame,
            text="全部题目（95题）",
            height=55,
            font=ctk.CTkFont(size=18),
            command=lambda: self._start_quiz(ALL_QUESTIONS)
        )
        btn3.pack(pady=12, fill="x", padx=60)

        note = ctk.CTkLabel(
            self.menu_frame,
            text="提示：多选题需要点击「提交答案」按钮后才会显示解析",
            font=ctk.CTkFont(size=13),
            text_color="#888888"
        )
        note.pack(pady=30)

    def _start_quiz(self, question_list):
        """从菜单切换到正式答题界面"""
        self.menu_frame.destroy()

        self.questions = question_list
        self.total = len(self.questions)
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self.is_multi = False
        self.multi_submit_btn = None

        # 构建真正的答题界面
        self._build_quiz_ui()
        self._load_question(0)

        # 绑定窗口大小变化
        self.bind("<Configure>", self._on_window_resize)
        self.after(150, self._update_wraplength)

    # ==================== 答题界面（原 _build_ui 内容） ====================
    def _build_quiz_ui(self):
        # 使用 grid 布局让整个界面真正响应式（推荐做法）
        self.grid_rowconfigure(0, weight=0)   # 顶部标题
        self.grid_rowconfigure(1, weight=1)   # 主内容区
        self.grid_rowconfigure(2, weight=0)   # 底部导航

        self.grid_columnconfigure(0, weight=1)

        # ========== 顶部标题栏 ==========
        top_frame = ctk.CTkFrame(self, height=55, corner_radius=0)
        top_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        title_label = ctk.CTkLabel(
            top_frame,
            text="AWS CLF-C02 练习模式",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=8)

        self.progress_label = ctk.CTkLabel(
            top_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.progress_label.pack(side="right", padx=15)

        # ========== 主内容区 ==========
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)

        # 题目信息区
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=8, pady=(8, 4))

        self.domain_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.domain_label.pack(anchor="w")

        self.question_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=900,          # 初始值，会在 resize 时动态更新
            justify="left"
        )
        self.question_label.pack(anchor="w", pady=(6, 10))

        # 选项容器（普通 Frame，配合 resize 动态调整）
        self.options_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        self.options_frame.pack(fill="both", expand=True, padx=8, pady=6)

        # ========== 解析面板（更灵活的响应式设计） ==========
        explain_frame = ctk.CTkFrame(main_frame, fg_color="#1f1f1f")
        explain_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        explain_title = ctk.CTkLabel(
            explain_frame,
            text="解析",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00bfff"
        )
        explain_title.pack(anchor="w", padx=12, pady=(8, 4))

        self.explain_text = ctk.CTkTextbox(
            explain_frame,
            font=ctk.CTkFont(size=13),
            wrap="word",
            state="disabled"
        )
        self.explain_text.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        # ========== 底部导航栏 ==========
        nav_frame = ctk.CTkFrame(self, height=58, corner_radius=0)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)

        nav_frame.grid_columnconfigure(0, weight=0)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=0)
        nav_frame.grid_columnconfigure(3, weight=0)

        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="← 上一题",
            width=105,
            height=34,
            command=self.go_previous
        )
        self.prev_btn.grid(row=0, column=0, padx=(12, 6), pady=8, sticky="w")

        self.question_counter = ctk.CTkLabel(
            nav_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.question_counter.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="下一题 →",
            width=105,
            height=34,
            command=self.go_next
        )
        self.next_btn.grid(row=0, column=2, padx=(6, 6), pady=8, sticky="e")

        self.finish_btn = ctk.CTkButton(
            nav_frame,
            text="完成测试",
            width=95,
            height=34,
            fg_color="#d35400",
            hover_color="#e67e22",
            command=self.finish_quiz
        )
        self.finish_btn.grid(row=0, column=3, padx=(6, 12), pady=8, sticky="e")

    def _load_question(self, index: int):
        """加载指定索引的题目"""
        if index < 0 or index >= self.total:
            return

        self.current_index = index
        q = self.questions[index]

        # 更新顶部进度
        self.progress_label.configure(text=f"{index + 1} / {self.total}")
        self.question_counter.configure(text=f"第 {index + 1} 题 / 共 {self.total} 题")

        # 题目信息
        self.domain_label.configure(text=f"领域：{q.get('domain', '未分类')}")
        self.question_label.configure(text=q["question"])

        # 动态更新 wraplength（响应式关键）
        self._update_wraplength()

        # 清空旧选项 + 清理多选提交按钮
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_widgets.clear()

        if self.multi_submit_btn:
            self.multi_submit_btn.destroy()
            self.multi_submit_btn = None

        # 判断是单选还是多选
        self.is_multi = len(q["correct_answers"]) > 1

        # 动态创建选项控件（带缩放支持）
        current_answer = self.user_answers.get(index, [])
        scale = max(0.7, min(1.1, self.winfo_width() / 1000.0))
        opt_font_size = int(13 * scale)

        if self.is_multi:
            # ==================== 多选题 ====================
            for letter in ["A", "B", "C", "D", "E"][:len(q["options"])]:
                var = ctk.BooleanVar(value=letter in current_answer)
                cb = ctk.CTkCheckBox(
                    self.options_frame,
                    text=q["options"][ord(letter) - ord("A")],
                    variable=var,
                    font=ctk.CTkFont(size=opt_font_size)
                )
                cb.pack(anchor="w", padx=15, pady=4)
                self.option_widgets.append(cb)

            # 多选题专用提交按钮
            btn_text = "更新答案" if index in self.user_answers else "提交答案"
            self.multi_submit_btn = ctk.CTkButton(
                self.options_frame,
                text=btn_text,
                height=int(34 * scale),
                fg_color="#2980b9",
                hover_color="#3498db",
                font=ctk.CTkFont(size=opt_font_size),
                command=self._submit_multi_answer
            )
            self.multi_submit_btn.pack(fill="x", padx=20, pady=(10, 4))

        else:
            # ==================== 单选题 ====================
            self.radio_var = ctk.StringVar(value=current_answer[0] if current_answer else "")

            for i, opt in enumerate(q["options"]):
                letter = chr(ord("A") + i)
                rb = ctk.CTkRadioButton(
                    self.options_frame,
                    text=opt,
                    variable=self.radio_var,
                    value=letter,
                    font=ctk.CTkFont(size=opt_font_size),
                    command=self._on_single_change
                )
                rb.pack(anchor="w", padx=15, pady=4)
                self.option_widgets.append(rb)

        # 加载题目后更新解析面板（多选题会根据是否有提交记录决定显示强度）
        self._update_explanation_panel()

        # 更新按钮状态
        self.prev_btn.configure(state="normal" if index > 0 else "disabled")
        self.next_btn.configure(state="normal" if index < self.total - 1 else "disabled")

    def _on_single_change(self):
        """单选题选择变化"""
        selected = self.radio_var.get()
        if selected:
            self.user_answers[self.current_index] = [selected]
            self._update_explanation_panel()

    def _submit_multi_answer(self):
        """
        多选题专用提交逻辑：
        用户必须点击此按钮后，才会正式记录答案并显示解析。
        """
        if not self.is_multi or not self.option_widgets:
            return

        selected = []
        for i, widget in enumerate(self.option_widgets):
            if isinstance(widget, ctk.CTkCheckBox):
                letter = chr(ord("A") + i)
                if widget.get():          # 获取当前勾选状态
                    selected.append(letter)

        selected.sort()
        self.user_answers[self.current_index] = selected
        self._update_explanation_panel(force_full_explanation=True)

    def _update_explanation_panel(self, force_full_explanation=False):
        """
        更新解析面板。
        对于多选题：
        - 如果还没提交过答案 → 提示“请点击提交答案”
        - 如果已经提交过 → 默认显示“上次提交的答案”，除非 force_full_explanation=True 才显示完整正误+解析
        """
        q = self.questions[self.current_index]
        user_ans = self.user_answers.get(self.current_index, [])

        self.explain_text.configure(state="normal")
        self.explain_text.delete("1.0", "end")

        if not user_ans:
            self.explain_text.insert("end", "请先选择答案，然后点击下方的「提交答案」按钮查看解析。")
            self.explain_text.configure(state="disabled")
            return

        correct = q.get("correct_answers", [])

        # 多选题的特殊处理：除非刚提交，否则只显示“上次选择”，不直接暴露正误
        if self.is_multi and not force_full_explanation:
            self.explain_text.insert("end", f"你上次提交的答案：{', '.join(user_ans)}\n\n")
            self.explain_text.insert("end", "点击「更新答案」按钮可重新提交并查看本次选择的正误与详细解析。")
            self.explain_text.configure(state="disabled")
            return

        # 显示用户答案 + 正确答案 + 题库自带的详细解析
        is_correct = (set(user_ans) == set(correct))

        status = "✅ 回答正确" if is_correct else "❌ 回答错误"
        self.explain_text.insert("end", f"{status}\n\n")

        self.explain_text.insert("end", f"你的答案：{', '.join(user_ans)}\n")
        self.explain_text.insert("end", f"正确答案：{', '.join(correct)}\n\n")

        self.explain_text.insert("end", f"📝 解析：\n{q.get('explanation', '暂无解析')}")

        self.explain_text.configure(state="disabled")

    # ==================== 响应式相关方法 ====================

    def _on_window_resize(self, event):
        """窗口大小变化时动态调整字体、间距和按钮大小"""
        if event.widget != self:
            return

        width = self.winfo_width()
        height = self.winfo_height()

        # 根据窗口宽度计算缩放比例（基准宽度 1000）
        scale = max(0.65, min(1.15, width / 1000.0))

        try:
            # 动态字体大小
            title_size = int(18 * scale)
            question_size = int(15 * scale)
            option_size = int(13 * scale)
            button_font_size = int(13 * scale)
            small_size = int(12 * scale)

            # 动态按钮高度
            btn_height = int(34 * scale)
            nav_btn_width = int(105 * scale)

            # 更新题目文字
            self.question_label.configure(
                font=ctk.CTkFont(size=question_size, weight="bold"),
                wraplength=max(350, width - 70)
            )

            # 更新导航按钮
            self.prev_btn.configure(
                width=max(80, nav_btn_width),
                height=btn_height,
                font=ctk.CTkFont(size=button_font_size)
            )
            self.next_btn.configure(
                width=max(80, nav_btn_width),
                height=btn_height,
                font=ctk.CTkFont(size=button_font_size)
            )
            self.finish_btn.configure(
                width=max(75, int(95 * scale)),
                height=btn_height,
                font=ctk.CTkFont(size=button_font_size)
            )

            # 更新计数器文字
            self.question_counter.configure(font=ctk.CTkFont(size=small_size))
            self.progress_label.configure(font=ctk.CTkFont(size=small_size))

            # 如果是多选题，同步调整提交按钮
            if self.multi_submit_btn and self.multi_submit_btn.winfo_exists():
                self.multi_submit_btn.configure(
                    height=btn_height,
                    font=ctk.CTkFont(size=button_font_size)
                )

        except Exception:
            pass

    def _update_wraplength(self):
        """手动更新 wraplength（在加载题目时调用）"""
        current_width = self.winfo_width()
        if current_width < 200:
            current_width = 950
        new_wraplength = max(320, current_width - 70)
        self.question_label.configure(wraplength=new_wraplength)

    # ==================== 原有方法 ====================

    def go_previous(self):
        if self.current_index > 0:
            self._load_question(self.current_index - 1)

    def go_next(self):
        if self.current_index < self.total - 1:
            self._load_question(self.current_index + 1)

    def finish_quiz(self):
        """完成测试，显示总结"""
        correct_count = 0
        for i, q in enumerate(self.questions):
            user = self.user_answers.get(i, [])
            if set(user) == set(q["correct_answers"]):
                correct_count += 1

        percentage = (correct_count / self.total) * 100 if self.total > 0 else 0

        # 弹出总结窗口
        summary = ctk.CTkToplevel(self)
        summary.title("测试完成")
        summary.geometry("500x300")
        summary.grab_set()

        ctk.CTkLabel(
            summary,
            text="本次练习完成！",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            summary,
            text=f"得分：{correct_count} / {self.total}",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            summary,
            text=f"正确率：{percentage:.1f}%",
            font=ctk.CTkFont(size=18)
        ).pack(pady=10)

        ctk.CTkButton(
            summary,
            text="关闭",
            command=summary.destroy
        ).pack(pady=30)


def launch_gui():
    """启动图形界面"""
    app = CLFQuizApp()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()