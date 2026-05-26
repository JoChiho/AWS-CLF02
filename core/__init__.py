# -*- coding: utf-8 -*-
"""
Core 引擎层（Core Layer）

包含：
- parser.py   : 输入格式解析
- engine.py   : 测验运行 + 评分系统
"""

from .parser import parse_user_answers, is_quit_command
from .engine import run_single_round, review_wrong_questions, get_performance_message

__all__ = [
    "parse_user_answers",
    "is_quit_command",
    "run_single_round",
    "review_wrong_questions",
    "get_performance_message",
]