# -*- coding: utf-8 -*-
"""
AWS CLF-C02 图形界面刷题系统（练习模式）

特点：
- 鼠标点击选择答案
- 自由翻阅上一题 / 下一题
- 每选择/修改答案后立即显示详细解析
"""

import customtkinter as ctk
from typing import List, Dict, Any
import time

from data import (
    ALL_QUESTIONS,
    SINGLE_CHOICE_QUESTIONS,
    MULTI_CHOICE_QUESTIONS,
    DOMAINS,
    get_domain_question_count,
    get_question_by_id,
    get_wrong_book_questions,
    shuffle_question_options,
    get_shuffled_questions,
)
from data.progress import (
    record_session,
    update_question_stat,
    get_recent_sessions,
    get_wrong_question_ids,
    get_accuracy_trend,
    get_question_stats,
)


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

        # 进度追踪相关
        self.current_mode: str = "all"          # all / single / multi / domain:xxx / wrong_book
        self.quiz_start_time: float = 0.0       # 用于计算本次练习时长

        # 选项打乱缓存（当前会话内每道题只打乱一次，翻页稳定）
        self._question_shuffles: Dict[int, Dict[str, Any]] = {}

        # 先显示选择题库的菜单界面
        self._build_menu_ui()

    def _get_shuffle_info(self, quiz_idx: int, q: Dict[str, Any]) -> Dict[str, Any]:
        """获取（或生成）当前题目的打乱信息，缓存以保证同一会话内稳定"""
        if quiz_idx in self._question_shuffles:
            return self._question_shuffles[quiz_idx]
        info = shuffle_question_options(q)
        self._question_shuffles[quiz_idx] = info
        return info

    # ==================== 菜单界面 ====================
    def _build_menu_ui(self):
        """题库选择主菜单（支持传统模式 + 考试领域分类练习）"""
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # 使用可滚动容器，保证所有按钮（包括下面的错题本/我的学习）都能被看到
        scrollable = ctk.CTkScrollableFrame(self.menu_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            scrollable,
            text="AWS CLF-C02 刷题系统",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(10, 5))

        subtitle = ctk.CTkLabel(
            scrollable,
            text="请选择你要练习的题库",
            font=ctk.CTkFont(size=16)
        )
        subtitle.pack(pady=(0, 20))

        # ========== 传统模式 ==========
        traditional_label = ctk.CTkLabel(
            scrollable,
            text="传统模式",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888"
        )
        traditional_label.pack(anchor="w", padx=60, pady=(0, 6))

        single_count = len(SINGLE_CHOICE_QUESTIONS)
        multi_count = len(MULTI_CHOICE_QUESTIONS)
        total_count = len(ALL_QUESTIONS)

        btn1 = ctk.CTkButton(
            scrollable,
            text=f"单选题题库（{single_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            command=lambda: self._start_quiz(SINGLE_CHOICE_QUESTIONS, "single")
        )
        btn1.pack(pady=6, fill="x", padx=60)

        btn2 = ctk.CTkButton(
            scrollable,
            text=f"多选题题库（{multi_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            fg_color="#2980b9",
            hover_color="#3498db",
            command=lambda: self._start_quiz(MULTI_CHOICE_QUESTIONS, "multi")
        )
        btn2.pack(pady=6, fill="x", padx=60)

        btn3 = ctk.CTkButton(
            scrollable,
            text=f"全部题目（{total_count}题）",
            height=48,
            font=ctk.CTkFont(size=16),
            command=lambda: self._start_quiz(ALL_QUESTIONS, "all")
        )
        btn3.pack(pady=6, fill="x", padx=60)

        # ========== 直接入口：错题本（最醒目，放在传统模式之后） ==========
        btn_wrong_direct = ctk.CTkButton(
            scrollable,
            text="打开错题本（累计 C/W 统计 + 一键练习）",
            height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self._show_wrong_book
        )
        btn_wrong_direct.pack(pady=(12, 6), fill="x", padx=60)

        # ========== 按考试领域分类练习（新增） ==========
        domain_label = ctk.CTkLabel(
            scrollable,
            text="按考试领域分类练习（CLF-C02 官方四大领域）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00b894"
        )
        domain_label.pack(anchor="w", padx=60, pady=(18, 6))

        for domain in DOMAINS:
            count = get_domain_question_count(domain)
            display_name = {
                "Cloud Concepts": "云概念",
                "Security and Compliance": "安全与合规",
                "Technology and Services": "技术与服务",
                "Billing, Pricing, and Support": "账单、定价与支持"
            }.get(domain, domain)

            btn = ctk.CTkButton(
                scrollable,
                text=f"{display_name}（{count}题）",
                height=48,
                font=ctk.CTkFont(size=16),
                fg_color="#00b894",
                hover_color="#00d9a3",
                command=lambda d=domain: self._start_domain_quiz(d)
            )
            btn.pack(pady=6, fill="x", padx=60)

        note = ctk.CTkLabel(
            scrollable,
            text="提示：多选题需要点击「提交答案」按钮后才会显示解析 | 领域练习会混合单选与多选题",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        note.pack(pady=(20, 10))

        # ========== 我的学习（历史 + 统计） ==========
        progress_label = ctk.CTkLabel(
            scrollable,
            text="我的学习",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f39c12"
        )
        progress_label.pack(anchor="w", padx=60, pady=(10, 6))

        btn_hist = ctk.CTkButton(
            scrollable,
            text="历史记录（近10次）",
            height=42,
            font=ctk.CTkFont(size=15),
            fg_color="#7f8c8d",
            hover_color="#95a5a6",
            command=self._show_history
        )
        btn_hist.pack(pady=4, fill="x", padx=60)

        btn_wrong = ctk.CTkButton(
            scrollable,
            text="错题本（累计统计）",
            height=42,
            font=ctk.CTkFont(size=15),
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self._show_wrong_book
        )
        btn_wrong.pack(pady=4, fill="x", padx=60)

        btn_stats = ctk.CTkButton(
            scrollable,
            text="我的统计与趋势",
            height=42,
            font=ctk.CTkFont(size=15),
            fg_color="#8e44ad",
            hover_color="#9b59b6",
            command=self._show_my_stats
        )
        btn_stats.pack(pady=4, fill="x", padx=60)

    def _start_quiz(self, question_list, mode: str = "all"):
        """从菜单切换到正式答题界面"""
        self.menu_frame.destroy()

        # 每次进入题库时打乱题目出题顺序（不修改原始列表）
        self.questions = get_shuffled_questions(question_list)
        self.total = len(self.questions)
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self.is_multi = False
        self.multi_submit_btn = None

        # 记录本次练习模式 + 开始时间（用于持久化）
        self.current_mode = mode
        self.quiz_start_time = time.time()

        # 清空上一轮的选项打乱缓存（新会话重新打乱）
        self._question_shuffles.clear()

        # 构建真正的答题界面
        self._build_quiz_ui()
        self._load_question(0)

        # 绑定窗口大小变化
        self.bind("<Configure>", self._on_window_resize)
        self.after(150, self._update_wraplength)

    def _start_domain_quiz(self, domain: str):
        """按考试领域启动分类练习"""
        from data import get_questions_by_domain

        questions = get_questions_by_domain(domain)
        if not questions:
            print(f"警告：领域 '{domain}' 没有题目")
            return

        self.menu_frame.destroy()

        # 每次进入题库时打乱题目出题顺序
        self.questions = get_shuffled_questions(questions)
        self.total = len(self.questions)
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self.is_multi = False
        self.multi_submit_btn = None

        # 记录领域模式 + 开始时间
        self.current_mode = f"domain:{domain}"
        self.quiz_start_time = time.time()

        # 清空上一轮的选项打乱缓存
        self._question_shuffles.clear()

        self._build_quiz_ui()
        self._load_question(0)

        self.bind("<Configure>", self._on_window_resize)
        self.after(150, self._update_wraplength)

    def _start_wrong_book_quiz(self, wrong_ids: List[str]):
        """从错题本启动针对性练习"""
        from data import get_wrong_book_questions

        questions = get_wrong_book_questions(wrong_ids)
        if not questions:
            print("错题本为空，无法开始练习")
            return

        self.menu_frame.destroy()

        # 每次进入题库时打乱题目出题顺序（即使是从错题本进入也打乱）
        self.questions = get_shuffled_questions(questions)
        self.total = len(self.questions)
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self.is_multi = False
        self.multi_submit_btn = None

        self.current_mode = "wrong_book"
        self.quiz_start_time = time.time()

        # 清空上一轮的选项打乱缓存
        self._question_shuffles.clear()

        self._build_quiz_ui()
        self._load_question(0)

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
        self.info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=8, pady=(8, 4))

        # 额外绑定 info_frame 的尺寸变化，更及时地更新题目换行
        self.info_frame.bind("<Configure>", lambda e: self._update_wraplength())

        self.domain_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.domain_label.pack(fill="x", anchor="w")

        self.question_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=700,          # 初始值，会在 resize 时动态更新
            justify="left",
            anchor="w"               # 确保文字内容靠左对齐（而非默认居中）
        )
        self.question_label.pack(fill="x", anchor="w", pady=(6, 10))

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

        # 保存引用以便后续返回主菜单时清理
        self.top_frame = top_frame
        self.main_frame = main_frame
        self.nav_frame = nav_frame

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
        self.update_idletasks()
        self._update_wraplength()

        # 多次保障更新，确保换行生效
        self.after(50, self._update_wraplength)
        self.after(150, self._update_wraplength)

        # 清空旧选项 + 清理多选提交按钮
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_widgets.clear()

        if self.multi_submit_btn:
            self.multi_submit_btn.destroy()
            self.multi_submit_btn = None

        # 判断是单选还是多选
        self.is_multi = len(q["correct_answers"]) > 1

        # 获取本题的选项打乱信息（同一会话内稳定）
        shuffle_info = self._get_shuffle_info(index, q)
        display_options = shuffle_info["shuffled_options"]
        display_to_original = shuffle_info["display_to_original"]
        original_to_display = shuffle_info["original_to_display"]

        # 动态创建选项控件（带缩放支持）
        # 注意：self.user_answers 始终存储「原始字母」，需要映射到当前显示字母才能正确回显
        stored_original = self.user_answers.get(index, [])
        current_display_answer = [original_to_display.get(c, c) for c in stored_original]

        scale = max(0.7, min(1.1, self.winfo_width() / 1000.0))
        opt_font_size = int(13 * scale)

        if self.is_multi:
            # ==================== 多选题（使用打乱后的选项） ====================
            for letter in ["A", "B", "C", "D", "E"][:len(display_options)]:
                var = ctk.BooleanVar(value=letter in current_display_answer)
                cb = ctk.CTkCheckBox(
                    self.options_frame,
                    text=display_options[ord(letter) - ord("A")],
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
            # ==================== 单选题（使用打乱后的选项） ====================
            self.radio_var = ctk.StringVar(value=current_display_answer[0] if current_display_answer else "")

            for i, opt_text in enumerate(display_options):
                letter = chr(ord("A") + i)
                rb = ctk.CTkRadioButton(
                    self.options_frame,
                    text=opt_text,
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
        """单选题选择变化（将显示字母转回原始字母后存储）"""
        selected_display = self.radio_var.get()
        if selected_display:
            shuffle_info = self._question_shuffles.get(self.current_index, {})
            display_to_original = shuffle_info.get("display_to_original", {})
            original_letter = display_to_original.get(selected_display, selected_display)
            self.user_answers[self.current_index] = [original_letter]
            self._update_explanation_panel()

    def _submit_multi_answer(self):
        """
        多选题专用提交逻辑：
        用户必须点击此按钮后，才会正式记录答案并显示解析。
        存储时将显示字母全部转回原始字母。
        """
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

        # 转回原始字母并排序（保持与题库一致的存储格式）
        selected_original = sorted(display_to_original.get(d, d) for d in selected_display)
        self.user_answers[self.current_index] = selected_original
        self._update_explanation_panel(force_full_explanation=True)

    def _update_explanation_panel(self, force_full_explanation=False):
        """
        更新解析面板（会将内部存储的原始字母映射回用户看到的显示字母）。
        """
        q = self.questions[self.current_index]
        user_ans_original = self.user_answers.get(self.current_index, [])

        self.explain_text.configure(state="normal")
        self.explain_text.delete("1.0", "end")

        if not user_ans_original:
            self.explain_text.insert("end", "请先选择答案，然后点击下方的「提交答案」按钮查看解析。")
            self.explain_text.configure(state="disabled")
            return

        # 取出本题打乱映射，把原始字母转成用户实际看到的显示字母
        shuffle_info = self._question_shuffles.get(self.current_index, {})
        original_to_display = shuffle_info.get("original_to_display", {})

        user_ans_display = [original_to_display.get(c, c) for c in user_ans_original]
        correct_original = q.get("correct_answers", [])
        correct_display = [original_to_display.get(c, c) for c in correct_original]

        # 多选题的特殊处理：除非刚提交，否则只显示“上次选择”，不直接暴露正误
        if self.is_multi and not force_full_explanation:
            self.explain_text.insert("end", f"你上次提交的答案：{', '.join(user_ans_display)}\n\n")
            self.explain_text.insert("end", "点击「更新答案」按钮可重新提交并查看本次选择的正误与详细解析。")
            self.explain_text.configure(state="disabled")
            return

        # 显示用户答案 + 正确答案 + 题库自带的详细解析（全部使用显示字母）
        is_correct = (set(user_ans_original) == set(correct_original))

        status = "✅ 回答正确" if is_correct else "❌ 回答错误"
        self.explain_text.insert("end", f"{status}\n\n")

        self.explain_text.insert("end", f"你的答案：{', '.join(user_ans_display)}\n")
        self.explain_text.insert("end", f"正确答案：{', '.join(correct_display)}\n\n")

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

            # 更新题目文字：动态字体 + 靠左对齐 + 初始 wraplength（后续由 _update_wraplength 用容器实际宽度精调）
            try:
                if width > 200:
                    new_wrap = max(260, width - 130)
                else:
                    new_wrap = 700
            except Exception:
                new_wrap = 700

            self.question_label.configure(
                font=ctk.CTkFont(size=question_size, weight="bold"),
                wraplength=new_wrap,
                justify="left",
                anchor="w"
            )
            self.question_label.update_idletasks()

            # 使用容器真实宽度再次精调 wraplength（确保窄窗口下题目自动换行且完整显示）
            self.after(10, self._update_wraplength)

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
        """手动更新 wraplength（在加载题目时调用）。优先使用 info_frame 实际宽度，保证窄窗口时正确换行并靠左显示完整题目。"""
        self.update_idletasks()

        try:
            # 优先使用题目信息容器的实际宽度（比窗口宽度更精确，自动考虑所有 padding）
            container_width = self.info_frame.winfo_width()
            if container_width > 60:
                # info_frame 有 padx=8（左右16），外层 main_frame 有 padx=8，预留安全边距后计算
                new_wraplength = max(260, container_width - 36)
            else:
                # 回退到窗口宽度
                win_width = self.winfo_width()
                if win_width > 200:
                    new_wraplength = max(260, win_width - 130)
                else:
                    new_wraplength = 700
        except Exception:
            new_wraplength = 700

        self.question_label.configure(wraplength=new_wraplength)
        self.question_label.update_idletasks()

    # ==================== 原有方法 ====================

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
            if user:   # 用户真正作答过
                answered_count += 1
                if set(user) == set(q["correct_answers"]):
                    correct_count += 1

        # 正确率按「已回答的题目」计算（支持中途点击「完成测试」查看当前正确率）
        answered_for_rate = answered_count if answered_count > 0 else 1
        percentage = (correct_count / answered_for_rate) * 100 if answered_count > 0 else 0.0

        # 计算本次练习时长
        duration = int(time.time() - self.quiz_start_time) if self.quiz_start_time else 0

        # ==================== 持久化：记录会话 + 更新每题统计 ====================
        try:
            # 1. 记录本次会话（最近 10 次）。传入 answered 使历史记录和趋势统计使用正确率 = correct / answered
            record_session(self.current_mode, self.total, correct_count, duration, answered=answered_count)

            # 2. 更新每道已作答题目的累计正确/错误次数（永久）
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

        # ==================== 弹出总结窗口 ====================
        summary = ctk.CTkToplevel(self)
        summary.title("测试完成")
        summary.geometry("520x360")
        summary.grab_set()

        ctk.CTkLabel(
            summary,
            text="本次练习完成！",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(18, 6))

        # 作答进度（区分题库规模和实际作答数）
        progress_text = f"作答进度：{answered_count} / {self.total} 题"
        if answered_count == self.total:
            progress_text = f"已完成全部 {self.total} 题"
        ctk.CTkLabel(
            summary,
            text=progress_text,
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        ).pack(pady=(0, 4))

        # 得分使用「答对 / 已答」
        score_denominator = answered_count if answered_count > 0 else self.total
        ctk.CTkLabel(
            summary,
            text=f"得分：{correct_count} / {score_denominator}",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=6)

        # 正确率明确说明基于已回答题目
        rate_note = "（基于已回答题目）" if answered_count > 0 else "（未作答任何题目）"
        ctk.CTkLabel(
            summary,
            text=f"正确率：{percentage:.1f}% {rate_note}",
            font=ctk.CTkFont(size=16)
        ).pack(pady=2)

        ctk.CTkLabel(
            summary,
            text=f"用时：{duration // 60}分{duration % 60}秒",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            summary,
            text="✓ 进度已自动保存（历史记录 + 错题统计）",
            font=ctk.CTkFont(size=13),
            text_color="#2ecc71"
        ).pack(pady=(6, 12))

        ctk.CTkButton(
            summary,
            text="关闭",
            width=110,
            height=36,
            command=summary.destroy
        ).pack(side="left", padx=8, pady=10)

        ctk.CTkButton(
            summary,
            text="返回主菜单",
            width=130,
            height=36,
            fg_color="#2980b9",
            hover_color="#3498db",
            command=lambda: (summary.destroy(), self._return_to_menu())
        ).pack(side="left", padx=8, pady=10)

    # ==================== 新增：三个持久化功能视图 ====================

    def _show_history(self):
        """显示最近 10 次练习历史"""
        sessions = get_recent_sessions(10)

        win = ctk.CTkToplevel(self)
        win.title("历史作答记录（最近10次）")
        win.geometry("820x520")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="最近 10 次练习记录（最新在前）",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))

        if not sessions:
            ctk.CTkLabel(
                win,
                text="还没有任何练习记录。\n完成一次测试后记录会自动保存。",
                font=ctk.CTkFont(size=15)
            ).pack(pady=40)
            ctk.CTkButton(win, text="关闭", command=win.destroy).pack(pady=20)
            return

        # 使用 Textbox 展示表格
        textbox = ctk.CTkTextbox(win, font=ctk.CTkFont(size=13), wrap="none")
        textbox.pack(fill="both", expand=True, padx=20, pady=10)

        # 表头支持新字段：answered（实际作答数）。旧记录无 answered 时回退到 total
        header = f"{'时间':<20} {'模式':<28} {'已答/总':>9} {'正确':>5} {'正确率':>8} {'用时':>8}\n"
        header += "-" * 98 + "\n"
        textbox.insert("end", header)

        for s in sessions:
            ts = s.get("timestamp", "")[:19].replace("T", " ")
            mode = s.get("mode", "unknown")
            total = s.get("total", 0)
            answered = s.get("answered", total)  # 兼容旧会话记录
            correct = s.get("correct", 0)
            acc = s.get("accuracy", 0.0)
            dur = s.get("duration_sec", 0)
            dur_str = f"{dur//60}m{dur%60:02d}s" if dur else "-"

            quiz_str = f"{answered}/{total}" if total else str(answered)
            line = f"{ts:<20} {mode:<28} {quiz_str:>9} {correct:>5} {acc:>7.1f}% {dur_str:>8}\n"
            textbox.insert("end", line)

        textbox.configure(state="disabled")

        ctk.CTkButton(win, text="关闭", width=100, command=win.destroy).pack(pady=12)

    def _show_wrong_book(self):
        """显示错题本 + 支持一键练习"""
        wrong_ids = get_wrong_question_ids(sort_by="error_rate")

        win = ctk.CTkToplevel(self)
        win.title("错题本（累计统计）")
        win.geometry("860x580")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="错题本（按错误率排序）",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(12, 6))

        if not wrong_ids:
            ctk.CTkLabel(
                win,
                text="太棒了！目前没有任何错题记录。\n继续练习，系统会自动统计你做错的题目。",
                font=ctk.CTkFont(size=15)
            ).pack(pady=40)
            ctk.CTkButton(win, text="关闭", command=win.destroy).pack(pady=20)
            return

        # 统计信息
        total_wrong = len(wrong_ids)
        info = ctk.CTkLabel(
            win,
            text=f"共 {total_wrong} 道题目曾经答错过（错误率从高到低排序）",
            font=ctk.CTkFont(size=13)
        )
        info.pack(pady=(0, 8))

        textbox = ctk.CTkTextbox(win, font=ctk.CTkFont(size=12), wrap="word")
        textbox.pack(fill="both", expand=True, padx=15, pady=6)

        header = f"{'ID':<6} {'C/W':<8} {'错误率':<8}  题目摘要\n"
        header += "-" * 100 + "\n"
        textbox.insert("end", header)

        for qid in wrong_ids[:30]:   # 最多显示前 30 道，避免界面太长
            stat = get_question_stats(qid) or {}
            c = stat.get("correct_count", 0)
            w = stat.get("wrong_count", 0)
            rate = (w / (c + w) * 100.0) if (c + w) > 0 else 0.0

            q = get_question_by_id(qid)
            qtext = (q["question"][:55] + "...") if q and len(q["question"]) > 58 else (q["question"] if q else "(题目不存在)")

            line = f"{qid:<6} {c}/{w:<6} {rate:>6.1f}%  {qtext}\n"
            textbox.insert("end", line)

        if len(wrong_ids) > 30:
            textbox.insert("end", f"\n... 还有 {len(wrong_ids) - 30} 道错题未显示 ...\n")

        textbox.configure(state="disabled")

        # 底部按钮
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=12)

        def start_practice():
            win.destroy()
            self._start_wrong_book_quiz(wrong_ids)

        ctk.CTkButton(
            btn_frame,
            text=f"练习全部 {len(wrong_ids)} 道错题",
            width=200,
            height=38,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=start_practice
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="关闭",
            width=100,
            height=38,
            command=win.destroy
        ).pack(side="left", padx=10)

    def _show_my_stats(self):
        """显示个人正确率趋势与总体统计"""
        trend = get_accuracy_trend()

        win = ctk.CTkToplevel(self)
        win.title("我的统计与趋势")
        win.geometry("620x480")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="学习数据统计",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 12))

        if trend["count"] == 0:
            ctk.CTkLabel(
                win,
                text="还没有足够的数据。\n完成几次练习后，这里会显示你的正确率趋势。",
                font=ctk.CTkFont(size=15)
            ).pack(pady=50)
            ctk.CTkButton(win, text="关闭", command=win.destroy).pack(pady=20)
            return

        # 核心指标卡片
        card = ctk.CTkFrame(win)
        card.pack(padx=30, pady=8, fill="x")

        ctk.CTkLabel(card, text=f"最近练习次数：{trend['count']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=(10, 4))
        ctk.CTkLabel(card, text=f"最近一次正确率：{trend['latest']:.1f}%", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=2)
        ctk.CTkLabel(card, text=f"近10次平均正确率：{trend['avg']:.1f}%", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=2)
        ctk.CTkLabel(card, text=f"最高 / 最低：{trend['max']:.1f}%  /  {trend['min']:.1f}%", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15, pady=(2, 10))

        # 趋势文字描述
        trend_text = {
            "improving": "📈 最近表现有明显进步！继续保持",
            "declining": "📉 最近正确率有所下降，建议多看错题解析",
            "stable": "➡️ 发挥稳定",
            "no_data": ""
        }.get(trend.get("trend", "stable"), "")

        ctk.CTkLabel(
            win,
            text=trend_text,
            font=ctk.CTkFont(size=15),
            text_color="#3498db"
        ).pack(pady=12)

        ctk.CTkLabel(
            win,
            text="提示：历史记录与错题本会永久保存（直到手动删除 user_data.json）。",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        ).pack(pady=(10, 20))

        ctk.CTkButton(win, text="关闭", width=120, height=36, command=win.destroy).pack(pady=10)

    def _return_to_menu(self):
        """从答题界面安全返回主菜单（清理 quiz 布局 + 重建初始菜单）"""
        # 清理三个主布局 frame
        for frame_attr in ("top_frame", "main_frame", "nav_frame"):
            frame = getattr(self, frame_attr, None)
            if frame and frame.winfo_exists():
                frame.destroy()

        # 清理 resize 绑定（避免残留回调）
        try:
            self.unbind("<Configure>")
        except Exception:
            pass

        # 重置所有状态
        self.questions = []
        self.total = 0
        self.user_answers = {}
        self.current_index = 0
        self.option_widgets = []
        self.is_multi = False
        self.multi_submit_btn = None
        self.current_mode = "all"
        self.quiz_start_time = 0.0
        self.top_frame = None
        self.main_frame = None
        self.nav_frame = None

        # 重新构建主菜单
        self._build_menu_ui()


def launch_gui():
    """启动图形界面"""
    app = CLFQuizApp()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()