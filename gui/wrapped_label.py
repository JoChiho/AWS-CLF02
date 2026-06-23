# -*- coding: utf-8 -*-
"""CTkLabel 换行辅助：按容器宽度计算 wraplength，避免文字被裁切。"""

from __future__ import annotations

from typing import Any


def widget_scaling(widget: Any) -> float:
    try:
        return float(widget._get_widget_scaling())
    except Exception:
        return 1.0


def frame_wraplength(
    frame_width: int,
    scale: float = 1.0,
    *,
    margin: float = 56,
    minimum: int = 160,
) -> int:
    """
    根据容器物理像素宽度，计算 CTkLabel 的 wraplength（逻辑单位）。

    CTkLabel 会把 wraplength 再乘以 widget scaling 传给 tk.Label，
    因此这里要除以 scale，避免高 DPI 下换行宽度过大、文字横向溢出。
    """
    if frame_width <= 80:
        return minimum
    available = frame_width - margin * scale
    return max(minimum, int(available / max(scale, 0.75)))


def apply_wraplength(label: Any, wraplength: int) -> None:
    """设置换行宽度，并允许标签随内容增高。"""
    label.configure(wraplength=wraplength, height=0)
    label.update_idletasks()


def measure_container_wraplength(
    reference: Any,
    container: Any | None,
    *,
    margin: float = 56,
    minimum: int = 160,
    fallback: Any | None = None,
    fallback_margin: float = 72,
) -> int:
    """优先按容器实际宽度计算 wraplength，否则回退到窗口宽度。"""
    scale = widget_scaling(reference)
    try:
        if container is not None and container.winfo_exists():
            width = container.winfo_width()
            if width > 80:
                return frame_wraplength(width, scale, margin=margin, minimum=minimum)
    except Exception:
        pass
    try:
        root = fallback if fallback is not None else reference
        width = root.winfo_width()
        if width > 80:
            return frame_wraplength(
                width, scale, margin=fallback_margin, minimum=minimum,
            )
    except Exception:
        pass
    return minimum


def wrap_reference_widget(host: Any) -> Any:
    """从答题界面取用于 DPI 缩放的参考控件。"""
    labels = getattr(host, "_option_text_labels", [])
    if labels:
        return labels[0]
    if hasattr(host, "question_label"):
        return host.question_label
    return host


def measure_question_wraplength(host: Any) -> int:
    host.update_idletasks()
    ref = wrap_reference_widget(host)
    return measure_container_wraplength(
        ref,
        getattr(host, "info_frame", None),
        margin=24,
        minimum=200,
        fallback=host,
        fallback_margin=48,
    )


def measure_option_wraplength(host: Any) -> int:
    host.update_idletasks()
    ref = wrap_reference_widget(host)
    return measure_container_wraplength(
        ref,
        getattr(host, "options_frame", None),
        margin=56,
        minimum=160,
        fallback=host,
        fallback_margin=72,
    )