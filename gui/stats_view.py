# -*- coding: utf-8 -*-
"""历史记录、错题本、统计趋势弹窗"""

import customtkinter as ctk

from data.progress import (
    get_recent_sessions,
    get_accuracy_trend,
)
from gui.constants import ACCURACY_TREND_TEXT


class StatsMixin:
    """持久化数据可视化弹窗"""

    def _show_history(self):
        """显示最近 10 次练习历史"""
        bank_label = self._bank_label()
        sessions = get_recent_sessions(10, bank_id=self.current_bank_id)

        win = ctk.CTkToplevel(self)
        win.title(f"历史作答记录（最近10次）· {bank_label}")
        win.geometry("820x520")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="最近 10 次练习记录（最新在前）",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(15, 10))

        if not sessions:
            ctk.CTkLabel(
                win,
                text="还没有任何练习记录。\n完成一次测试后记录会自动保存。",
                font=ctk.CTkFont(size=15),
            ).pack(pady=40)
            ctk.CTkButton(win, text="关闭", command=win.destroy).pack(pady=20)
            return

        textbox = ctk.CTkTextbox(win, font=ctk.CTkFont(size=13), wrap="none")
        textbox.pack(fill="both", expand=True, padx=20, pady=10)

        header = f"{'时间':<20} {'模式':<28} {'已答/总':>9} {'正确':>5} {'成绩':>10} {'用时':>8}\n"
        header += "-" * 102 + "\n"
        textbox.insert("end", header)

        for s in sessions:
            ts = s.get("timestamp", "")[:19].replace("T", " ")
            mode = s.get("mode", "unknown")
            total = s.get("total", 0)
            answered = s.get("answered", total)
            correct = s.get("correct", 0)
            acc = s.get("accuracy", 0.0)
            dur = s.get("duration_sec", 0)
            dur_str = f"{dur//60}m{dur%60:02d}s" if dur else "-"
            quiz_str = f"{answered}/{total}" if total else str(answered)
            if s.get("scaled_score") is not None:
                result_str = f"{int(s['scaled_score']):>4}分"
            else:
                result_str = f"{acc:>6.1f}%"
            line = (
                f"{ts:<20} {mode:<28} {quiz_str:>9} {correct:>5} "
                f"{result_str:>10} {dur_str:>8}\n"
            )
            textbox.insert("end", line)

        textbox.configure(state="disabled")
        ctk.CTkButton(win, text="关闭", width=100, command=win.destroy).pack(pady=12)

    def _show_my_stats(self):
        """显示个人正确率趋势与总体统计"""
        bank_label = self._bank_label()
        trend = get_accuracy_trend(bank_id=self.current_bank_id)

        win = ctk.CTkToplevel(self)
        win.title(f"我的统计与趋势 · {bank_label}")
        win.geometry("620x480")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="学习数据统计",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(15, 12))

        if trend["count"] == 0:
            ctk.CTkLabel(
                win,
                text="还没有足够的数据。\n完成几次练习后，这里会显示你的正确率趋势。",
                font=ctk.CTkFont(size=15),
            ).pack(pady=50)
            ctk.CTkButton(win, text="关闭", command=win.destroy).pack(pady=20)
            return

        card = ctk.CTkFrame(win)
        card.pack(padx=30, pady=8, fill="x")

        ctk.CTkLabel(
            card, text=f"最近练习次数：{trend['count']}", font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=(10, 4))
        ctk.CTkLabel(
            card, text=f"最近一次正确率：{trend['latest']:.1f}%", font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=2)
        ctk.CTkLabel(
            card,
            text=f"近10次平均正确率：{trend['avg']:.1f}%",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=15, pady=2)
        ctk.CTkLabel(
            card,
            text=f"最高 / 最低：{trend['max']:.1f}%  /  {trend['min']:.1f}%",
            font=ctk.CTkFont(size=14),
        ).pack(anchor="w", padx=15, pady=(2, 10))

        trend_text = ACCURACY_TREND_TEXT.get(trend.get("trend", "stable"), "")
        ctk.CTkLabel(
            win,
            text=trend_text,
            font=ctk.CTkFont(size=15),
            text_color="#3498db",
        ).pack(pady=12)

        ctk.CTkLabel(
            win,
            text="提示：历史记录与错题本会永久保存（直到手动删除 user_data.json）。",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
        ).pack(pady=(10, 20))

        ctk.CTkButton(win, text="关闭", width=120, height=36, command=win.destroy).pack(pady=10)