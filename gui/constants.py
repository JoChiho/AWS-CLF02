# -*- coding: utf-8 -*-
"""GUI 层共享常量"""

from data.mock_exam import (
    MOCK_EXAM_DURATION_SEC,
    MOCK_EXAM_PASS_PERCENT,
    MOCK_EXAM_QUESTION_COUNT,
)

DOMAIN_DISPLAY_NAMES = {
    "Cloud Concepts": "云概念",
    "Security and Compliance": "安全与合规",
    "Technology and Services": "技术与服务",
    "Billing, Pricing, and Support": "账单、定价与支持",
}

MOCK_EXAM_DURATION_MIN = MOCK_EXAM_DURATION_SEC // 60

# 连续答对 N 次后自动标为「已掌握」，默认不再出现在错题本主列表
MASTER_STREAK_REQUIRED = 2
WRONG_BOOK_TOP_N_DEFAULT = 10

ACCURACY_TREND_TEXT = {
    "improving": "📈 最近表现有明显进步！继续保持",
    "declining": "📉 最近正确率有所下降，建议多看错题解析",
    "stable": "➡️ 发挥稳定",
    "no_data": "",
}