# -*- coding: utf-8 -*-
"""
AWS CLF-C02 简体中文考试中「肯定会译成中文」的术语。

依据（2026 对照）：
- 官方考试指南简体中文版（领域 1–4、技术和概念）
- 官方「考试范围内的 AWS 服务」中文页
- AWS 官方中文词汇表 / 中文产品页

原则：
- Amazon S3、Amazon EC2、AWS Lambda、IAM 等服务品牌名保持英文
- 购买选项、全球基础设施、安全组件、账单支持类考点词用官方中文
"""
from __future__ import annotations

import re

# 长词优先。仅收录官方考试指南/范围内服务页已使用的中文译法。
_PHRASE_EN_TO_ZH: list[tuple[str, str]] = [
    ("Amazon WorkSpaces Secure Browser", "Amazon WorkSpaces 安全浏览器"),
    ("Amazon WorkSpaces 安全浏览器", "Amazon WorkSpaces 安全浏览器"),
    ("AWS Elastic Disaster Recovery", "AWS 弹性灾难恢复"),
    ("AWS Shared Responsibility Model", "AWS 责任共担模式"),
    ("Shared Responsibility Model", "责任共担模式"),
    ("AWS Management Console", "AWS 管理控制台"),
    ("AWS Pricing Calculator", "AWS 定价计算器"),
    ("AWS Support Center", "AWS 支持中心"),
    ("AWS Professional Services", "AWS 专业服务"),
    ("AWS Partner Network (APN)", "AWS 合作伙伴网络 (APN)"),
    ("AWS Partner Network", "AWS 合作伙伴网络"),
    ("AWS Cost and Usage Report", "AWS 成本和使用情况报告"),
    ("Cost and Usage Report", "AWS 成本和使用情况报告"),
    ("AWS Cost Allocation Tags", "AWS 成本分配标签"),
    ("cost allocation tags", "成本分配标签"),
    ("Network Access Control Lists (NACLs)", "网络 ACL（NACL）"),
    ("Network Access Control Lists", "网络 ACL"),
    ("AWS Network Access Control Lists", "网络 ACL"),
    ("AWS Security Groups", "安全组"),
    ("Multi-Factor Authentication (MFA)", "多重身份验证 (MFA)"),
    ("Multi-factor authentication (MFA)", "多重身份验证 (MFA)"),
    ("Multi-Factor Authentication", "多重身份验证"),
    ("Multi-factor authentication", "多重身份验证"),
    ("Principle of Least Privilege", "最低权限原则"),
    ("principle of least privilege", "最低权限原则"),
    ("Serverless interactive query service", "无服务器交互式查询服务"),
    ("Infrastructure as Code (IaC)", "基础设施即代码 (IaC)"),
    ("Infrastructure as Code", "基础设施即代码 (IaC)"),
    ("Elastic Load Balancing", "弹性负载均衡"),
    ("Elastic Load Balancer", "弹性负载均衡器"),
    ("Application Load Balancer", "应用程序负载均衡器"),
    ("Network Load Balancer", "网络负载均衡器"),
    ("Gateway Load Balancer", "网关负载均衡器"),
    ("Virtual Private Gateway", "虚拟私有网关"),
    ("Internet Gateway", "互联网网关"),
    ("NAT Gateway", "NAT 网关"),
    ("EC2 On-Demand Instances", "EC2 按需型实例"),
    ("EC2 Reserved Instances", "EC2 预留实例"),
    ("EC2 Spot Instances", "EC2 竞价型实例"),
    ("EC2 Dedicated Instances", "EC2 专用实例"),
    ("EC2 Dedicated Hosts", "EC2 专属主机"),
    ("On-Demand Instances", "按需型实例"),
    ("On-Demand Instance", "按需型实例"),
    ("Reserved Instances", "预留实例"),
    ("Reserved Instance", "预留实例"),
    ("Spot Instances", "竞价型实例"),
    ("Spot Instance", "竞价型实例"),
    ("AWS Savings Plans", "AWS 节省计划"),
    ("Savings Plans", "AWS 节省计划"),
    ("Dedicated Hosts", "专属主机"),
    ("Dedicated Host", "专属主机"),
    ("Dedicated Instances", "专用实例"),
    ("Dedicated Instance", "专用实例"),
    ("Capacity Reservations", "容量预留"),
    ("Capacity Reservation", "容量预留"),
    ("Consolidated Billing", "整合账单"),
    ("Service Quotas", "服务配额"),
    ("Availability Zones", "可用区"),
    ("Availability Zone", "可用区"),
    ("Edge Locations", "边缘站点"),
    ("Edge Location", "边缘站点"),
    ("Security Groups", "安全组"),
    ("Security Group", "安全组"),
    ("Network ACLs", "网络 ACL"),
    ("Network ACL", "网络 ACL"),
    ("Instance Store", "实例存储"),
    ("Operational Excellence", "卓越运营"),
    ("Performance Efficiency", "性能效率"),
    ("Cost Optimization", "成本优化"),
    ("High Availability", "高可用性"),
    ("Fault Tolerance", "容错"),
    ("encryption in transit", "传输中加密"),
    ("encryption at rest", "静态加密"),
    ("compute optimized", "计算优化型"),
    ("storage optimized", "存储优化型"),
    ("Economies of Scale", "规模经济"),
    ("Global Reach", "全球覆盖范围"),
    ("Hybrid architecture", "混合架构"),
    ("Hybrid Architecture", "混合架构"),
    ("AWS Regions", "AWS 区域"),
    ("AWS Region", "AWS 区域"),
]

# 仅当整段选项（去掉 A. 前缀）等于该词时才替换，避免误伤短词
_WHOLE_OPTION_EN_TO_ZH: dict[str, str] = {
    "On-premises": "本地部署",
    "On-Premises": "本地部署",
    "On premises": "本地部署",
    "Hybrid": "混合",
    "Cloud": "云",
    "Serverless": "无服务器",
    "Auto Scaling": "弹性伸缩",
    "Load Balancer": "负载均衡器",
    "Reliability": "可靠性",
    "Agility": "敏捷性",
    "Elasticity": "弹性",
    "Sustainability": "可持续性",
    "Security": "安全性",
    "MFA": "多重身份验证 (MFA)",
    "Economies of scale": "规模经济",
    "Economies of Scale": "规模经济",
    "Global Reach": "全球覆盖范围",
    "High Availability": "高可用性",
}

# 中文同义写法统一为考试指南用词
_ZH_UNIFY: list[tuple[str, str]] = [
    ("AWS 责任共担模型", "AWS 责任共担模式"),
    ("责任共担模型", "责任共担模式"),
    ("按需实例", "按需型实例"),
    ("竞价实例", "竞价型实例"),
    ("现货实例", "竞价型实例"),
    ("专用主机", "专属主机"),
    ("合并计费", "整合账单"),
    ("多因素认证", "多重身份验证"),
    ("多因素身份验证", "多重身份验证"),
    ("混合 architecture", "混合架构"),
]

_EN_TOKEN_RE = [
    (re.compile(r"(?<!AWS )Auto Scaling"), "弹性伸缩"),
    (re.compile(r"\bServerless\b"), "无服务器"),
    (re.compile(r"\bOn-premises\b", re.IGNORECASE), "本地部署"),
    (re.compile(r"\bHybrid\b"), "混合"),
    (re.compile(r"「([A-E])\. Cloud」"), r"「\1. 云」"),
    (re.compile(r"和 Cloud(?=[\s，。、」]|$)"), "和云"),
]

# 这些英文原词已确认对应官方中文，导入时不要再强制保留英文选项
_OFFICIAL_ZH_ENGLISH_FORMS: frozenset[str] = frozenset(
    {en for en, _zh in _PHRASE_EN_TO_ZH}
    | set(_WHOLE_OPTION_EN_TO_ZH.keys())
    | {
        "Spot instances",
        "Reserved instances",
        "On-demand instances",
        "Availability zones",
        "Security groups",
        "Edge locations",
        "Dedicated hosts",
        "Instance store",
        "Consolidated billing",
        "Service quotas",
    }
)


def is_official_zh_exam_term(en: str) -> bool:
    """英文选项是否属于官方中文考试会翻译的考点词。"""
    text = (en or "").strip()
    if not text:
        return False
    if text in _OFFICIAL_ZH_ENGLISH_FORMS:
        return True
    if text in _WHOLE_OPTION_EN_TO_ZH:
        return True
    lowered = {t.lower() for t in _OFFICIAL_ZH_ENGLISH_FORMS}
    if text.lower() in lowered:
        return True
    for en_phrase, _zh in _PHRASE_EN_TO_ZH:
        if en_phrase.lower() == text.lower():
            return True
    return False


def _collapse_cjk_spaces(text: str) -> str:
    text = re.sub(r"  +", " ", text)
    text = re.sub(r"([\u4e00-\u9fff]) +([\u4e00-\u9fff])", r"\1\2", text)
    return text.strip() if text.strip() != text else text


def apply_official_zh_exam_terms(text: str, *, whole_option: bool = False) -> str:
    """把官方中文考试会翻译的英文考点词换成考试指南用词。"""
    if not text:
        return text
    original = text
    leading = re.match(r"^(\s*)", text)
    prefix = leading.group(1) if leading else ""

    body = text
    letter = ""
    if whole_option and ". " in text[:4]:
        letter, body = text.split(". ", 1)
        letter = f"{letter}. "

    stripped = body.strip()
    if stripped in _WHOLE_OPTION_EN_TO_ZH:
        mapped = _WHOLE_OPTION_EN_TO_ZH[stripped]
        return f"{prefix}{letter}{mapped}"
    for en, zh in _WHOLE_OPTION_EN_TO_ZH.items():
        if stripped.lower() == en.lower():
            return f"{prefix}{letter}{zh}"

    for en, zh in _PHRASE_EN_TO_ZH:
        if en in body:
            body = body.replace(en, zh)

    # 常见大小写变体
    lowered_pairs = [
        ("availability zones", "可用区"),
        ("availability zone", "可用区"),
        ("spot instances", "竞价型实例"),
        ("reserved instances", "预留实例"),
        ("on-demand instances", "按需型实例"),
        ("security groups", "安全组"),
        ("edge locations", "边缘站点"),
        ("dedicated hosts", "专属主机"),
        ("savings plans", "AWS 节省计划"),
        ("shared responsibility model", "责任共担模式"),
        ("elastic load balancing", "弹性负载均衡"),
        ("multi-factor authentication", "多重身份验证"),
        ("instance store", "实例存储"),
        ("service quotas", "服务配额"),
        ("consolidated billing", "整合账单"),
        ("aws management console", "AWS 管理控制台"),
        ("economies of scale", "规模经济"),
        ("global reach", "全球覆盖范围"),
        ("high availability", "高可用性"),
        ("fault tolerance", "容错"),
        ("operational excellence", "卓越运营"),
        ("performance efficiency", "性能效率"),
        ("cost optimization", "成本优化"),
        ("hybrid architecture", "混合架构"),
        ("fault tolerance", "容错"),
    ]
    for en, zh in lowered_pairs:
        body = re.sub(re.escape(en), zh, body, flags=re.IGNORECASE)

    for pat, zh in _EN_TOKEN_RE:
        body = pat.sub(zh, body)

    for old, new in _ZH_UNIFY:
        if old in body:
            body = body.replace(old, new)

    body = body.replace("AWSShared Responsibility Model", "AWS 责任共担模式")
    body = _collapse_cjk_spaces(body)
    result = f"{prefix}{letter}{body}"
    return result if result != original or whole_option else result


def apply_official_zh_to_question(question: dict) -> dict:
    """就地改写题干 / 选项 / 解析中的官方中文考试术语。"""
    if question.get("question"):
        question["question"] = apply_official_zh_exam_terms(question["question"])
    if question.get("options"):
        question["options"] = [
            apply_official_zh_exam_terms(o, whole_option=True)
            for o in question["options"]
        ]
    if question.get("explanation"):
        question["explanation"] = apply_official_zh_exam_terms(question["explanation"])
    return question
