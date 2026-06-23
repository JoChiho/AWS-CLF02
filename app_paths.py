# -*- coding: utf-8 -*-
"""应用路径工具：开发模式与 PyInstaller 冻结模式统一解析。"""
from __future__ import annotations

import sys
from pathlib import Path


def get_app_root() -> Path:
    """
    返回用户数据应存放的应用根目录。

    - 开发模式：项目根目录（main.py 所在目录）
    - PyInstaller 冻结模式：可执行文件所在目录
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def get_bundle_root() -> Path:
    """返回只读资源包根目录（冻结模式下为 _MEIPASS）。"""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return get_app_root()