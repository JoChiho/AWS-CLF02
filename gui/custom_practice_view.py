# -*- coding: utf-8 -*-
"""自定义练习配置界面"""

from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox


from data.custom_practice import (
    FILTER_ALL,
    FILTER_LOW_ACCURACY,
    FILTER_NEVER,
    SCOPE_ALL,
    SCOPE_MULTI,
    SCOPE_SINGLE,
    get_practice_pool,
    select_custom_practice_questions,
)
from gui.constants import (
    CUSTOM_PRACTICE_COUNTS,
    CUSTOM_PRACTICE_DEFAULT_ACCURACY_THRESHOLD,
    DOMAIN_DISPLAY_NAMES,
)


class CustomPracticeMixin:
    """自定义练习：题量 + 范围 + 筛选"""

    def _show_custom_practice_dialog(self) -> None:
        bank = self._get_bank()
        bank_label = self._bank_label()
        win = ctk.CTkToplevel(self)
        win.title(f"自定义练习 · {bank_label}")
        win.geometry("520x560")
        win.minsize(480, 520)
        win.grab_set()
        win.transient(self)

        ctk.CTkLabel(
            win,
            text="自定义练习",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(pady=(16, 4))

        ctk.CTkLabel(
            win,
            text="按题量、范围与掌握情况随机抽题，适合碎片化复习",
            font=ctk.CTkFont(size=13),
            text_color="#9aa3b5",
        ).pack(pady=(0, 12))

        body = ctk.CTkScrollableFrame(win, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=4)

        count_var = ctk.StringVar(value=str(CUSTOM_PRACTICE_COUNTS[1]))
        scope_options = [
            ("全部题库", SCOPE_ALL),
            ("仅单选题", SCOPE_SINGLE),
            ("仅多选题", SCOPE_MULTI),
        ]
        for domain in bank.DOMAINS:
            label = DOMAIN_DISPLAY_NAMES.get(domain, domain)
            scope_options.append((label, f"domain:{domain}"))
        scope_labels = [label for label, _ in scope_options]
        scope_values = [value for _, value in scope_options]
        scope_var = ctk.StringVar(value=scope_labels[0])
        filter_var = ctk.StringVar(value=FILTER_ALL)
        threshold_var = ctk.StringVar(
            value=str(int(CUSTOM_PRACTICE_DEFAULT_ACCURACY_THRESHOLD))
        )

        preview_label = ctk.CTkLabel(
            body,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#7ec8ff",
            justify="left",
            anchor="w",
            wraplength=440,
        )

        def _scope_value() -> str:
            label = scope_var.get()
            if label in scope_labels:
                return scope_values[scope_labels.index(label)]
            return SCOPE_ALL

        def _refresh_preview() -> None:
            pool = get_practice_pool(
                scope=_scope_value(),
                filter_mode=filter_var.get(),
                accuracy_threshold=float(threshold_var.get()),
                bank_id=self.current_bank_id,
            )
            req = int(count_var.get())
            avail = len(pool)
            if avail == 0:
                preview_label.configure(
                    text="当前条件下没有可用题目，请放宽筛选或换范围。",
                    text_color="#f5a8a8",
                )
            elif avail < req:
                preview_label.configure(
                    text=f"符合条件的题目共 {avail} 道，将抽取全部 {avail} 道。",
                    text_color="#ffd966",
                )
            else:
                preview_label.configure(
                    text=f"符合条件的题目共 {avail} 道，将随机抽取 {req} 道。",
                    text_color="#7ec8ff",
                )

        # --- 题量 ---
        ctk.CTkLabel(
            body,
            text="抽题数量",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(4, 6))

        count_row = ctk.CTkFrame(body, fg_color="transparent")
        count_row.pack(fill="x", pady=(0, 12))

        for i, n in enumerate(CUSTOM_PRACTICE_COUNTS):
            ctk.CTkRadioButton(
                count_row,
                text=f"{n} 题",
                variable=count_var,
                value=str(n),
                font=ctk.CTkFont(size=13),
                command=_refresh_preview,
            ).grid(row=0, column=i, padx=(0, 12), sticky="w")

        # --- 题目范围 ---
        ctk.CTkLabel(
            body,
            text="题目范围",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(4, 6))

        ctk.CTkOptionMenu(
            body,
            values=scope_labels,
            variable=scope_var,
            width=360,
            font=ctk.CTkFont(size=13),
            command=lambda _v: _refresh_preview(),
        ).pack(anchor="w", pady=(0, 12))

        # --- 筛选条件 ---
        ctk.CTkLabel(
            body,
            text="筛选条件",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(4, 6))

        filter_frame = ctk.CTkFrame(body, fg_color="#232b3d", corner_radius=8)
        filter_frame.pack(fill="x", pady=(0, 8))

        for text, value in [
            ("不限（从范围内随机）", FILTER_ALL),
            ("从未做过", FILTER_NEVER),
            ("正确率低于阈值（做过且未达标）", FILTER_LOW_ACCURACY),
        ]:
            ctk.CTkRadioButton(
                filter_frame,
                text=text,
                variable=filter_var,
                value=value,
                font=ctk.CTkFont(size=13),
                command=_refresh_preview,
            ).pack(anchor="w", padx=14, pady=6)

        threshold_row = ctk.CTkFrame(body, fg_color="transparent")
        threshold_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            threshold_row,
            text="正确率阈值：",
            font=ctk.CTkFont(size=13),
        ).pack(side="left")

        ctk.CTkOptionMenu(
            threshold_row,
            values=["50", "60", "70", "80"],
            variable=threshold_var,
            width=80,
            font=ctk.CTkFont(size=13),
            command=lambda _v: _refresh_preview(),
        ).pack(side="left", padx=(4, 4))

        ctk.CTkLabel(
            threshold_row,
            text="% 以下",
            font=ctk.CTkFont(size=13),
            text_color="#9aa3b5",
        ).pack(side="left")

        preview_label.pack(fill="x", pady=(8, 4))
        _refresh_preview()

        btn_row = ctk.CTkFrame(win, fg_color="transparent")
        btn_row.pack(pady=16)

        def _on_start() -> None:
            count = int(count_var.get())
            scope = _scope_value()
            filter_mode = filter_var.get()
            threshold = float(threshold_var.get())

            pool = get_practice_pool(
                scope=scope,
                filter_mode=filter_mode,
                accuracy_threshold=threshold,
                bank_id=self.current_bank_id,
            )
            if not pool:
                messagebox.showwarning(
                    "无法开始",
                    "当前条件下没有可用题目。\n请调整题目范围或筛选条件。",
                    parent=win,
                )
                return

            result = select_custom_practice_questions(
                count=count,
                scope=scope,
                filter_mode=filter_mode,
                accuracy_threshold=threshold,
                bank_id=self.current_bank_id,
            )
            win.destroy()

            if result.actual_count < result.requested_count:
                messagebox.showinfo(
                    "抽题提示",
                    f"符合条件的题目仅 {result.pool_size} 道，\n"
                    f"本次将练习全部 {result.actual_count} 道。",
                    parent=self,
                )

            self._start_custom_quiz(result.questions, result.mode)

        ctk.CTkButton(
            btn_row,
            text="开始练习",
            width=140,
            height=40,
            fg_color="#8e44ad",
            hover_color="#9b59b6",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=_on_start,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_row,
            text="取消",
            width=100,
            height=40,
            command=win.destroy,
        ).pack(side="left", padx=10)