# -*- coding: utf-8 -*-
"""CloudCertPrep CLF-C02 领域映射与模拟考试权重。"""

# domainN.json → 官方 CLF-C02 领域名
DOMAIN_FILE_MAP = {
    1: "Cloud Concepts",
    2: "Security and Compliance",
    3: "Technology and Services",
    4: "Billing, Pricing, and Support",
}

DOMAIN_DISPLAY_NAMES = {
    "Cloud Concepts": "云概念",
    "Security and Compliance": "安全与合规",
    "Technology and Services": "技术与服务",
    "Billing, Pricing, and Support": "账单定价与支持",
}

DOMAINS = [
    "Cloud Concepts",
    "Security and Compliance",
    "Technology and Services",
    "Billing, Pricing, and Support",
]

# CLF-C02 官方考试领域权重（%）
MOCK_EXAM_DOMAIN_WEIGHTS = {
    "Cloud Concepts": 24,
    "Security and Compliance": 30,
    "Technology and Services": 34,
    "Billing, Pricing, and Support": 12,
}

SOURCE_REPO = "https://github.com/nastaso/cloudcertprep"
SOURCE_LICENSE = "MIT"
SOURCE_RAW_BASE = (
    "https://raw.githubusercontent.com/nastaso/cloudcertprep/main/src/data/clf-c02"
)