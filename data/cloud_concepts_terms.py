# -*- coding: utf-8 -*-
"""
Cloud Concepts 领域术语统一。

对照 docs/AWS-CLF-C02_All_Knowledge_Points.md 与 AWS 官方英文考点，
统一选项中的英文关键词，以及题干/解析中的中文译法。
"""
from __future__ import annotations

import re

# AWS CAF 六大视角（考试英文原词）
CAF_PERSPECTIVES: tuple[str, ...] = (
    "Business",
    "People",
    "Governance",
    "Platform",
    "Security",
    "Operations",
)

# CAF 相关选项应保留英文的考点词
CAF_OPTION_FORCE_ENGLISH: frozenset[str] = frozenset(
    {
        *CAF_PERSPECTIVES,
        "Financial",
        "Infrastructure",
        "Agility",
        "Technology",
        "Process",
        "Organization",
        "Product",
        "Networking",
        "Database",
        "Compute",
        "Compliance",
        "Envision",
        "Align",
        "Launch",
        "Scale",
        "Rehost",
        "Replatform",
        "Refactor",
        "Repurchase",
        "Retire",
        "Retain",
        "Relocate",
        "Revalidate",
        "Redistribute",
        "Reconfigure",
    }
)

# 云概念核心词（知识点清单 1.2 / 1.4）
CLOUD_CONCEPT_FORCE_ENGLISH: frozenset[str] = frozenset(
    {
        "IaaS",
        "PaaS",
        "SaaS",
        "IaaS & SaaS",
        "Loose Coupling",
        "Loose coupling",
        "Tight coupling",
        "Tightly coupling",
        "Elastic coupling",
        "Microservices",
        "CapEx",
        "OpEx",
        "TCO",
    }
)

# 解析/题干内统一中文表述（长词优先）
_EXPLANATION_ZH_UNIFY: list[tuple[str, str]] = [
    ("AWS CAF 的人员观点", "AWS CAF 的人员视角"),
    ("从人的角度对劳动力准备情况的强调", "从人员视角对劳动力准备情况的强调"),
    ("从人的角度", "从人员视角"),
    ("人们视角", "人员视角"),
    ("人们观点", "人员视角"),
    ("人才视角", "人员视角"),
    ("商业视角", "业务视角"),
    ("商业角度", "业务视角"),
    ("业务角度", "业务视角"),
    ("安全视角", "Security 视角"),
    ("安全性的运营", "Security 运营"),
    ("六个角度：业务、人员、治理、平台、安全性和运营", "六个视角：业务、人员、治理、平台、安全和运营"),
    ("六个角度", "六个视角"),
    ("六个观点", "六个视角"),
    ("CAF 观点", "CAF 视角"),
    ("哪个 CAF 观点", "哪个 CAF 视角"),
    ("哪种观点", "哪种视角"),
    ("哪个观点", "哪个视角"),
    ("什么观点", "什么视角"),
    ("的观点？", "的视角？"),
    ("而人员则侧重于", "而人员视角侧重于"),
    ("人们则侧重于", "人员视角侧重于"),
    ("而不是作为其自己单独的财务角度存在", "而不是作为其自己单独的 Financial 视角存在"),
    ("人们」是错误的：人员", "People」是错误的：人员"),
    ("「A. 人们」", "「A. People」"),
    ("「B. 人们」", "「B. People」"),
    ("「C. 人们」", "「C. People」"),
    ("「D. 人们」", "「D. People」"),
    ("「E. 人们」", "「E. People」"),
    ("「A. 商业」", "「A. Business」"),
    ("「B. 商业」", "「B. Business」"),
    ("「C. 商业」", "「C. Business」"),
    ("「D. 商业」", "「D. Business」"),
    ("「E. 商业」", "「E. Business」"),
    ("「B. 金融的」", "「B. Financial」"),
    ("「D. 基础设施」", "「D. Infrastructure」"),
    ("「E. 敏捷」", "「E. Agility」"),
    ("松散耦合", "松耦合"),
    ("松散耦合的", "松耦合的"),
    ("高可用性", "高可用"),
    ("容错能力", "容错"),
]

# 选项若为 CAF 视角中文误译，映射到英文原词
_OPTION_ZH_TO_EN: dict[str, str] = {
    "人们": "People",
    "商业": "Business",
    "金融的": "Financial",
    "治理": "Governance",
    "平台": "Platform",
    "运营": "Operations",
}

_CAF_QUESTION_RE = re.compile(
    r"CAF|Cloud Adoption Framework|云采用框架|迁移策略|转型域|转换域|"
    r"业务能力|技术能力|七个迁移|7 R|7R",
    re.IGNORECASE,
)


def is_cloud_concepts_domain(domain: str) -> bool:
    return (domain or "").strip() == "Cloud Concepts"


def should_force_cloud_concepts_english(en: str) -> bool:
    """Cloud Concepts 选项正文是否应保留英文考点词。"""
    text = (en or "").strip()
    if not text:
        return False
    if text in CAF_OPTION_FORCE_ENGLISH:
        return True
    if text in CLOUD_CONCEPT_FORCE_ENGLISH:
        return True
    lower = text.lower()
    if lower in {t.lower() for t in CAF_OPTION_FORCE_ENGLISH}:
        return True
    if lower in {t.lower() for t in CLOUD_CONCEPT_FORCE_ENGLISH}:
        return True
    return False


def normalize_cloud_concepts_text(text: str, *, in_caf_context: bool = False) -> str:
    """统一 Cloud Concepts 题干/解析中的术语译法。"""
    if not text:
        return text
    caf = in_caf_context or bool(_CAF_QUESTION_RE.search(text))
    for old, new in _EXPLANATION_ZH_UNIFY:
        if old in text:
            text = text.replace(old, new)
    if caf:
        text = text.replace("人们", "人员")
        text = text.replace("商业", "业务")
    return text


def normalize_cloud_concepts_question(question: dict) -> dict:
    """就地统一 Cloud Concepts 题目的术语。"""
    if not is_cloud_concepts_domain(question.get("domain", "")):
        return question

    caf = _CAF_QUESTION_RE.search(
        (question.get("question") or "")
        + (question.get("explanation") or "")
        + " ".join(question.get("options") or [])
    )

    if question.get("question"):
        question["question"] = normalize_cloud_concepts_text(
            question["question"],
            in_caf_context=bool(caf),
        )
    if question.get("explanation"):
        question["explanation"] = normalize_cloud_concepts_text(
            question["explanation"],
            in_caf_context=bool(caf),
        )
    return question