# -*- coding: utf-8 -*-
"""增强版错题本：全量滚动、领域筛选、单题练习、Top N、已掌握标记"""

import customtkinter as ctk

from data import DOMAINS, get_wrong_book_questions
from data.progress import (
    get_wrong_book_entries,
    set_question_mastered,
    count_mastered_wrong_questions,
)
from gui.constants import (
    DOMAIN_DISPLAY_NAMES,
    MASTER_STREAK_REQUIRED,
    WRONG_BOOK_TOP_N_DEFAULT,
)


class WrongBookMixin:
    """错题本增强界面"""

    def _show_wrong_book(self):
        """打开增强版错题本"""
        win = ctk.CTkToplevel(self)
        win.title("错题本")
        win.geometry("920x640")
        win.minsize(780, 520)
        win.grab_set()

        state = {
            "sort_by": "error_rate",
            "domain": None,
            "include_mastered": False,
        }

        ctk.CTkLabel(
            win,
            text="错题本",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(12, 4))

        ctk.CTkLabel(
            win,
            text=f"连续答对 {MASTER_STREAK_REQUIRED} 次将自动标为「已掌握」并从主列表隐藏",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
        ).pack(pady=(0, 8))

        toolbar = ctk.CTkFrame(win, fg_color="transparent")
        toolbar.pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkLabel(toolbar, text="领域：", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=(0, 4)
        )
        domain_options = ["全部"] + [
            DOMAIN_DISPLAY_NAMES.get(d, d) for d in DOMAINS
        ]
        domain_var = ctk.StringVar(value="全部")
        domain_menu = ctk.CTkOptionMenu(
            toolbar,
            values=domain_options,
            variable=domain_var,
            width=140,
        )
        domain_menu.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(toolbar, text="排序：", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=(0, 4)
        )
        sort_labels = {
            "error_rate": "错误率",
            "wrong_count": "错误次数",
            "last_wrong": "最近作答",
        }
        sort_var = ctk.StringVar(value=sort_labels["error_rate"])
        sort_menu = ctk.CTkOptionMenu(
            toolbar,
            values=list(sort_labels.values()),
            variable=sort_var,
            width=110,
        )
        sort_menu.pack(side="left", padx=(0, 12))

        include_mastered_var = ctk.BooleanVar(value=False)

        def on_include_mastered():
            state["include_mastered"] = include_mastered_var.get()
            refresh_list()

        ctk.CTkCheckBox(
            toolbar,
            text="显示已掌握",
            variable=include_mastered_var,
            command=on_include_mastered,
            font=ctk.CTkFont(size=13),
        ).pack(side="left", padx=4)

        summary_label = ctk.CTkLabel(
            win, text="", font=ctk.CTkFont(size=13), anchor="w"
        )
        summary_label.pack(fill="x", padx=18, pady=(0, 6))

        list_scroll = ctk.CTkScrollableFrame(win, fg_color="#1a1a1a")
        list_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        empty_label = ctk.CTkLabel(
            list_scroll,
            text="",
            font=ctk.CTkFont(size=15),
            justify="center",
        )

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=10)

        current_ids: list[str] = []

        def _domain_from_label(label: str):
            if label == "全部":
                return None
            for d, name in DOMAIN_DISPLAY_NAMES.items():
                if name == label:
                    return d
            return None

        def _sort_from_label(label: str) -> str:
            for key, val in sort_labels.items():
                if val == label:
                    return key
            return "error_rate"

        def refresh_list():
            for child in list_scroll.winfo_children():
                child.destroy()

            state["domain"] = _domain_from_label(domain_var.get())
            state["sort_by"] = _sort_from_label(sort_var.get())

            entries = get_wrong_book_entries(
                sort_by=state["sort_by"],
                domain=state["domain"],
                include_mastered=state["include_mastered"],
            )
            current_ids.clear()
            current_ids.extend(e["id"] for e in entries)

            mastered_n = count_mastered_wrong_questions()
            domain_note = (
                f" · 领域：{domain_var.get()}"
                if state["domain"]
                else ""
            )
            summary_label.configure(
                text=(
                    f"当前显示 {len(entries)} 题{domain_note}"
                    f"  |  已掌握（隐藏中）：{mastered_n} 题"
                )
            )

            if not entries:
                empty_label = ctk.CTkLabel(
                    list_scroll,
                    text=(
                        "当前筛选条件下没有错题。\n"
                        "若刚标为「已掌握」，可勾选「显示已掌握」查看。"
                    ),
                    font=ctk.CTkFont(size=14),
                    justify="center",
                )
                empty_label.pack(pady=40)
                return

            header = ctk.CTkFrame(list_scroll, fg_color="transparent")
            header.pack(fill="x", pady=(4, 6))
            for text, width in [
                ("ID", 52),
                ("C/W", 56),
                ("错误率", 58),
                ("领域", 88),
                ("题目摘要", 340),
                ("操作", 120),
            ]:
                ctk.CTkLabel(
                    header,
                    text=text,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=width,
                    anchor="w",
                ).pack(side="left", padx=2)

            for entry in entries:
                self._wrong_book_add_row(
                    list_scroll,
                    win,
                    entry,
                    refresh_list,
                )

        def start_practice(ids: list[str], mode_suffix: str):
            if not ids:
                return
            win.destroy()
            questions = get_wrong_book_questions(ids)
            if not questions:
                return
            self._start_wrong_book_quiz(ids, mode=f"wrong_book:{mode_suffix}")

        def on_domain_change(choice):
            refresh_list()

        def on_sort_change(choice):
            refresh_list()

        domain_menu.configure(command=on_domain_change)
        sort_menu.configure(command=on_sort_change)

        top_n = WRONG_BOOK_TOP_N_DEFAULT
        ctk.CTkButton(
            btn_frame,
            text=f"练 Top {top_n}",
            width=110,
            height=36,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=lambda: start_practice(
                current_ids[:top_n], f"top{top_n}"
            ),
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame,
            text="练当前筛选",
            width=120,
            height=36,
            fg_color="#d35400",
            hover_color="#e67e22",
            command=lambda: start_practice(current_ids, "filtered"),
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame,
            text="练全部显示",
            width=120,
            height=36,
            fg_color="#8e44ad",
            hover_color="#9b59b6",
            command=lambda: start_practice(current_ids, "all_visible"),
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame,
            text="关闭",
            width=90,
            height=36,
            command=win.destroy,
        ).pack(side="left", padx=6)

        refresh_list()

    def _wrong_book_add_row(
        self,
        parent,
        win,
        entry: dict,
        refresh_callback,
    ):
        """错题本中单行：摘要 + 练这题 + 掌握标记"""
        row = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=6)
        row.pack(fill="x", pady=3, padx=2)

        qid = entry["id"]
        mastered = entry.get("mastered", False)
        domain_cn = DOMAIN_DISPLAY_NAMES.get(entry.get("domain", ""), entry.get("domain", ""))

        id_btn = ctk.CTkButton(
            row,
            text=qid,
            width=48,
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#34495e",
            hover_color="#4a6278",
            command=lambda: self._wrong_book_practice_one(win, qid),
        )
        id_btn.pack(side="left", padx=(8, 4), pady=8)

        ctk.CTkLabel(
            row,
            text=f"{entry['correct_count']}/{entry['wrong_count']}",
            width=52,
            anchor="w",
            font=ctk.CTkFont(size=12),
        ).pack(side="left", padx=2)

        ctk.CTkLabel(
            row,
            text=f"{entry['error_rate']:.0f}%",
            width=54,
            anchor="w",
            font=ctk.CTkFont(size=12),
        ).pack(side="left", padx=2)

        ctk.CTkLabel(
            row,
            text=domain_cn[:6],
            width=80,
            anchor="w",
            font=ctk.CTkFont(size=11),
            text_color="#aaaaaa",
        ).pack(side="left", padx=2)

        preview = entry.get("question_preview", "")
        ctk.CTkLabel(
            row,
            text=preview,
            width=340,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=12),
            wraplength=330,
        ).pack(side="left", padx=4, pady=6)

        action_frame = ctk.CTkFrame(row, fg_color="transparent")
        action_frame.pack(side="left", padx=4, pady=6)

        ctk.CTkButton(
            action_frame,
            text="练这题",
            width=56,
            height=26,
            font=ctk.CTkFont(size=11),
            command=lambda: self._wrong_book_practice_one(win, qid),
        ).pack(side="left", padx=2)

        master_text = "取消掌握" if mastered else "标掌握"
        master_color = "#7f8c8d" if mastered else "#27ae60"

        def toggle_master():
            set_question_mastered(qid, mastered=not mastered)
            refresh_callback()

        ctk.CTkButton(
            action_frame,
            text=master_text,
            width=64,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color=master_color,
            hover_color="#95a5a6",
            command=toggle_master,
        ).pack(side="left", padx=2)

        if mastered:
            ctk.CTkLabel(
                row,
                text="✓",
                font=ctk.CTkFont(size=14),
                text_color="#2ecc71",
            ).pack(side="right", padx=8)

    def _wrong_book_practice_one(self, win, qid: str):
        """从错题本直接练习单道题"""
        win.destroy()
        self._start_wrong_book_quiz([qid], mode=f"wrong_book:single:{qid}")