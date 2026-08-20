# -*- coding: utf-8 -*-
"""
将 CloudCertPrep 翻译结果中的 AWS 服务名与考试关键词还原为英文。

仅替换服务名、产品名及考点关键词，保留选项/题干中的中文语意。
"""
from __future__ import annotations

import re
from typing import Iterable

from data.cloud_concepts_terms import (
    normalize_cloud_concepts_text,
    should_force_cloud_concepts_english,
)
from data.official_zh_exam_terms import (
    apply_official_zh_exam_terms,
    apply_official_zh_to_question,
    is_official_zh_exam_term,
)
from gui.term_glossary import _RAW_TERMS

# 机器翻译误译 / 音译（仅服务名与产品名）
_SERVICE_MISTRANSLATIONS: list[tuple[str, str]] = [
    ("Amazon简单存储服务（Amazon S3）", "Amazon S3"),
    ("Amazon简单存储服务", "Amazon S3"),
    ("Amazon简单队列服务（Amazon SQS）", "Amazon SQS"),
    ("Amazon简单队列服务", "Amazon SQS"),
    ("Amazon简单通知服务 (Amazon SNS)", "Amazon SNS"),
    ("Amazon简单通知服务（Amazon SNS）", "Amazon SNS"),
    ("Amazon简单通知服务", "Amazon SNS"),
    ("Amazon简单电子邮件服务 (Amazon SES)", "Amazon SES"),
    ("Amazon简单电子邮件服务", "Amazon SES"),
    ("Amazon弹性块存储（Amazon EBS）", "Amazon EBS"),
    ("Amazon弹性块存储 (Amazon EBS)", "Amazon EBS"),
    ("Amazon弹性块存储", "Amazon EBS"),
    ("Amazon弹性块商店", "Amazon EBS"),
    ("Amazon弹性计算云 (Amazon EC2)", "Amazon EC2"),
    ("Amazon弹性计算云（Amazon EC2）", "Amazon EC2"),
    ("Amazon弹性计算云", "Amazon EC2"),
    ("Amazon弹性文件系统 (Amazon EFS)", "Amazon EFS"),
    ("Amazon弹性文件系统（Amazon EFS）", "Amazon EFS"),
    ("Amazon弹性文件系统 (EFS)", "Amazon EFS"),
    ("Amazon弹性文件系统", "Amazon EFS"),
    ("Amazon弹性容器服务（Amazon ECS）", "Amazon ECS"),
    ("Amazon弹性容器服务 (Amazon ECS)", "Amazon ECS"),
    ("Amazon弹性容器服务", "Amazon ECS"),
    ("Amazon虚拟私有云 (Amazon VPC)", "Amazon VPC"),
    ("Amazon虚拟私有云（Amazon VPC）", "Amazon VPC"),
    ("Amazon虚拟私有云", "Amazon VPC"),
    ("Amazon理解", "Amazon Comprehend"),
    ("Amazon应用程序流 2.0", "Amazon AppStream 2.0"),
    ("Amazon应用程序流", "Amazon AppStream"),
    ("Amazon转录", "Amazon Transcribe"),
    ("Amazon莱克斯", "Amazon Lex"),
    ("Amazon重新识别", "Amazon Rekognition"),
    ("Amazon海王星", "Amazon Neptune"),
    ("Amazon波莉", "Amazon Polly"),
    ("Amazon精确定位", "Amazon Pinpoint"),
    ("Amazon云搜索", "Amazon CloudSearch"),
    ("Amazon事件桥", "Amazon EventBridge"),
    ("Amazon翻译", "Amazon Translate"),
    ("Amazon文本", "Amazon Textract"),
    ("Amazon肯德拉", "Amazon Kendra"),
    ("Amazon钟声", "Amazon Chime"),
    ("Amazon侦探", "Amazon Detective"),
    ("Amazon机器映像", "AMI"),
    ("Amazon实例商店", "Instance Store"),
    ("Amazon个性化", "Amazon Personalize"),
    ("Amazon副总裁", "Amazon WorkSpaces"),
    ("Amazon文档数据库", "Amazon DocumentDB"),
    ("Amazon预测", "Amazon Forecast"),
    ("Amazon开放搜索服务", "Amazon OpenSearch Service"),
    ("Amazon机器学习", "Amazon Machine Learning"),
    ("Amazon数据生命周期管理器", "Amazon Data Lifecycle Manager"),
    ("Amazon EC2 系统经理", "Amazon EC2 Systems Manager"),
    ("Amazon EC2 系统管理器", "AWS Systems Manager"),
    ("AWS 数据库迁移服务 (AWS DMS)", "AWS Database Migration Service (DMS)"),
    ("AWS 数据库迁移服务 (DMS)", "AWS Database Migration Service (DMS)"),
    ("AWS 数据库迁移服务", "AWS Database Migration Service"),
    ("AWS 身份和访问管理 (IAM)", "AWS Identity and Access Management (IAM)"),
    ("AWS 身份和访问管理", "AWS Identity and Access Management"),
    ("AWS 密钥管理服务 (AWS KMS)", "AWS Key Management Service (KMS)"),
    ("AWS 密钥管理服务", "AWS Key Management Service"),
    ("AWS 存储网关", "AWS Storage Gateway"),
    ("AWS 雪球", "AWS Snowball"),
    ("AWS 弹性豆茎", "AWS Elastic Beanstalk"),
    ("AWS 健康仪表板", "AWS Health Dashboard"),
    ("AWS 服务目录", "AWS Service Catalog"),
    ("AWS 批处理", "AWS Batch"),
    ("AWS 迁移中心", "AWS Migration Hub"),
    ("AWS 法门", "AWS Fargate"),
    ("AWS 代码提交", "AWS CodeCommit"),
    ("AWS 市场", "AWS Marketplace"),
    ("AWS 代码管道", "AWS CodePipeline"),
    ("AWS 自动扩展", "AWS Auto Scaling"),
    ("AWS 数据管道", "AWS Data Pipeline"),
    ("AWS 数据同步", "AWS DataSync"),
    ("AWS 雪地车", "AWS Snowmobile"),
    ("AWS 应用程序发现服务", "AWS Application Discovery Service"),
    ("AWS 前哨站", "AWS Outposts"),
    ("AWS 代码构建", "AWS CodeBuild"),
    ("AWS 步骤函数", "AWS Step Functions"),
    ("AWS 架构转换工具", "AWS Transform"),
    ("AWS 架构完善的工具", "AWS Well-Architected Tool"),
    ("AWS 传输系列", "AWS Snow Family"),
    ("AWS 资源组", "AWS Resource Groups"),
    ("AWS 应用程序同步", "AWS AppSync"),
    ("AWS 代码部署", "AWS CodeDeploy"),
    ("AWS 云采用框架", "AWS Cloud Adoption Framework"),
    ("AWS 客户端 VPN", "AWS Client VPN"),
    ("AWSLambda", "AWS Lambda"),
    ("CloudWatch器", "CloudWatch"),
    ("AWS Certificate Manager器", "AWS Certificate Manager"),
    ("Amazon CloudWatch器", "Amazon CloudWatch"),
    ("亚马逊简单存储服务", "Amazon S3"),
    ("杂交种", "Hybrid"),
]

# 仅保留「中文考试仍用英文」的考点词反向还原。
# 购买选项 / 可用区 / 安全组等已改为官方中文，见 official_zh_exam_terms。
_EXAM_KEYWORDS: list[tuple[str, str]] = [
    ("服务控制策略", "Service Control Policies"),
    ("放置群组", "Placement Groups"),
    ("归置组", "Placement Groups"),
]

# 真题选项中保留英文的部署模型 / 云服务模型 / 标准考点词
_FORCE_ENGLISH_OPTION_TERMS: set[str] = {
    "Mixed",
    "Cloud-native", "Partner network", "Hybrid architecture",
    "IaaS", "SaaS", "PaaS", "IaaS & SaaS",
    "Platform as a Service (PaaS)",
    "Infrastructure as a Service (IaaS)",
    "Software as a Service (SaaS)",
    "Networking as a Service (NaaS)",
    "Platform as a service",
    "Infrastructure as a service",
    "Platform as a Service",
    "Infrastructure as a Service",
    "Software as a Service",
    "Networking as a Service",
    "EC2 Instances", "EC2 instances",
}

_DEPLOYMENT_MODEL_RE = re.compile(
    r"^(On-premises|Hybrid|Cloud|Mixed)$",
    re.IGNORECASE,
)
_CLOUD_SERVICE_MODEL_RE = re.compile(
    r"^(Platform|Infrastructure|Software|Networking) as a [Ss]ervice"
    r"(?:\s*\([A-Za-z]+\))?$",
)
_IAAS_ACRONYM_RE = re.compile(r"^IaaS(?:\s*&\s*SaaS)?$|^SaaS$|^PaaS$", re.IGNORECASE)

_SERVICE_NAME_PREFIXES = ("Amazon ", "AWS ", "Elastic ", "Application ", "Network ")


def _is_service_glossary_entry(en: str) -> bool:
    if en.startswith(_SERVICE_NAME_PREFIXES):
        return True
    if en in {
        "Auto Scaling", "CloudFormation", "CloudFront", "CloudWatch", "CloudTrail",
        "CloudHSM", "GuardDuty", "Inspector", "Macie", "Cognito", "DynamoDB",
        "Redshift", "Lambda", "Artifact", "Organizations", "Fargate", "Beanstalk",
        "Kinesis", "ElastiCache", "Route 53", "Lightsail", "Neptune", "Athena",
        "EMR", "ECS", "EKS", "EFS", "EBS", "SQS", "SNS", "RDS", "VPC", "IAM",
        "KMS", "WAF", "Shield", "Config", "Glue", "Outposts", "Snowball",
        "DataSync", "AppSync", "Step Functions", "Secrets Manager", "Security Hub",
        "Trusted Advisor", "Cost Explorer", "Budgets", "Direct Connect",
        "Transit Gateway", "Global Accelerator", "Certificate Manager",
        "Systems Manager", "Database Migration Service", "Storage Gateway",
        "Service Catalog", "Control Tower", "Firewall Manager", "PrivateLink",
        "Load Balancer", "Internet Gateway", "NAT Gateway", "Availability Zones",
        "Availability Zone", "Edge Locations", "Local Zones", "Multi-AZ",
        "Multi-Region", "Cross-Region", "On-Demand Instances", "Spot Instances",
        "Reserved Instances", "Dedicated Hosts", "Security Groups", "Network ACL",
        "Elastic Load Balancing", "Application Load Balancer", "Network Load Balancer",
    }:
        return True
    return False


# 术语表中文为通用技术概念（非专指某一 AWS 服务），禁止反向替换成服务英文名
_GLOSSARY_ZH_GENERIC_EXCLUSIONS: frozenset[str] = frozenset({
    "NoSQL 数据库",
    "关系型数据库",
    "云原生数据库",
    "文档数据库",
    "图数据库",
    "时序数据库",
    "账本数据库",
    "数据仓库",
    "对象存储",
    "文件存储",
    "文件系统",
    "内容分发网络",
    "基础设施即代码",
    "内存缓存",
    "商业智能",
    "弹性文件系统",
    "数据库迁移服务",
    "数据库迁移",
})


def _build_glossary_service_reverse() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen_zh: set[str] = set()
    for en, zh in sorted(_RAW_TERMS, key=lambda p: len(p[1]), reverse=True):
        if not _is_service_glossary_entry(en):
            continue
        zh = zh.strip()
        if not zh or zh == en or zh in seen_zh:
            continue
        if zh in _GLOSSARY_ZH_GENERIC_EXCLUSIONS:
            continue
        if re.fullmatch(r"[A-Za-z0-9 ./&+-]+", zh):
            continue
        seen_zh.add(zh)
        pairs.append((zh, en))
    return pairs


_REPLACEMENTS: list[tuple[str, str]] = sorted(
    {zh: en for zh, en in _SERVICE_MISTRANSLATIONS + _EXAM_KEYWORDS}.items(),
    key=lambda item: len(item[0]),
    reverse=True,
)

_POST_FIXES: list[tuple[str, str]] = [
    ("serverless interactive query service", "Serverless interactive query service"),
]

# 解析中修正与选项不一致或易混淆的表述
_EXPLANATION_PHRASE_FIXES: list[tuple[str, str]] = [
    (
        "「B. 混合」是错误的：混合不是公认的云计算部署模型，并且不会与本地、混合和云一起出现在 AWS 框架中。",
        "「B. Mixed」是错误的：Mixed 不是 AWS 认可的云计算部署模型；"
        "CLF 考试中的三种部署模型为本地部署、混合和云。",
    ),
    (
        "「B. 杂交种」是错误的：混合部署将本地基础设施与云资源相结合",
        "「B. 混合」是错误的：混合部署将本地基础设施与云资源相结合",
    ),
    (
        "「E. 杂交种」是错误的：混合是指将本地基础设施与云资源相结合的架构",
        "「E. 混合」是错误的：混合是指将本地基础设施与云资源相结合的架构",
    ),
    ("不会与本地、混合和云一起出现", "不会与本地部署、混合和云一起出现"),
]

# 整句英文选项（被误替换为英文）需恢复中文语意
_SEMANTIC_EN_RE = re.compile(
    r"\b("
    r"allows?|implement(?:s|ed|ing)?|using|provides?|enables?|requires?|reduces?|"
    r"helps?|supports?|manages?|includes?|ensures?|deploys?|configures?|"
    r"responsible\s+for|should|could|would|will|can|the\s+ability|"
    r"eliminates?|increases?|decreases?|improves?|responsible|"
    r"design|backup|restore|development|coupling|scaling|pricing|testing|"
    r"hosting|provision|reduce|minimize|maximize|operate|run(?:s|ning)?|"
    r"pay(?:s|ing)?|build(?:s|ing)?|create(?:s|ing)?|use(?:s|ing)?|"
    r"makes?|distributes?|automatically|(?<!Instance )stores?|bills?|scales?|destroys?|"
    r"sells?|performs?|offers?|removes?|generates?|launched?|continues?|"
    r"shares?|checks?|accepts?|predicts?|called|architect(?:s|ing)?|"
    r"notifies?|encrypts?|resiz(?:e|es|able|ing)"
    r")\b",
    re.IGNORECASE,
)

# 带括号缩写的完整产品名，如 Amazon Elastic Compute Cloud (Amazon EC2)
_SERVICE_PAREN_NAME_RE = re.compile(
    r"^(?:Amazon|AWS)\s+[\w][\w\s-]*\((?:Amazon|AWS)\s+[\w][\w\s.-]*\)"
    r"(?:\s+[\w]+)?$",
)

# 真题中常以英文出现的纯考点词（整项为关键词，无中文叙述）
_ENGLISH_KEYWORD_ONLY: set[str] = {
    "Pilot Light", "Pilot light", "Warm Standby", "Warm standby",
    "Multi-site active-active", "Multi-Site Active-Active",
    "Placement Groups",
    "Lambda@Edge", "PostgreSQL",
    "AWS Auto Scaling",
    "AWS Cloud Adoption Framework (AWS CAF)",
    "AWS Identity and Access Management (IAM)",
    "AWS Identity and Access Management (AWS IAM)",
    "SDK", "ACL", "SSH", "API",
    "Mixed",
    "IaaS", "SaaS", "PaaS", "IaaS & SaaS",
    "Platform as a Service (PaaS)",
    "Infrastructure as a Service (IaaS)",
    "Software as a Service (SaaS)",
    "Networking as a Service (NaaS)",
}

_AWS_SENTENCE_VERBS = {
    "is", "are", "was", "were", "allows", "provides", "manages", "takes",
    "holds", "will", "can", "has", "have", "should", "would", "could",
    "makes", "automatically", "distributes", "stores", "bills", "scales",
    "eliminates", "destroys", "sells", "performs", "offers", "removes",
    "generates", "continues", "shares", "checks", "accepts", "predicts",
    "runs", "helps", "enables", "requires", "reduces", "supports",
}


def should_force_english_option(en: str) -> bool:
    """选项正文应保留英文原文（部署模型、服务名、标准考点词）。"""
    en = (en or "").strip()
    if not en:
        return False
    if is_official_zh_exam_term(en):
        return False
    if should_force_cloud_concepts_english(en):
        return True
    if en in _FORCE_ENGLISH_OPTION_TERMS:
        return True
    if en.lower() in {t.lower() for t in _FORCE_ENGLISH_OPTION_TERMS}:
        return True
    if _DEPLOYMENT_MODEL_RE.fullmatch(en):
        return True
    if _CLOUD_SERVICE_MODEL_RE.fullmatch(en):
        return True
    if _IAAS_ACRONYM_RE.fullmatch(en):
        return True
    if re.fullmatch(r"EC2 [Ii]nstances?", en):
        return True
    return is_english_keyword_only_option(en)


def is_english_keyword_only_option(en: str) -> bool:
    """选项本身仅为服务名/考点关键词（非中文叙述句）。"""
    en = (en or "").strip()
    if not en:
        return False
    if en in _ENGLISH_KEYWORD_ONLY:
        return True
    if re.fullmatch(r"[A-Z]{2,8}(@Edge)?", en):
        return True
    if "," in en:
        parts = [p.strip() for p in en.split(",") if p.strip()]
        if parts and all(p.startswith(("Amazon ", "AWS ")) for p in parts):
            if all(
                not _SEMANTIC_EN_RE.search(p) and len(p.split()) <= 5
                for p in parts
            ):
                return True
        return False
    if _SERVICE_PAREN_NAME_RE.fullmatch(en):
        return True
    if en.startswith(_SERVICE_NAME_PREFIXES):
        if _SEMANTIC_EN_RE.search(en):
            return False
        parts = en.split()
        if len(parts) >= 2 and parts[1].lower() in _AWS_SENTENCE_VERBS:
            return False
        if len(parts) >= 6:
            return False
        return True
    if _is_service_glossary_entry(en):
        return True
    return False


def option_body_needs_chinese_restore(body: str) -> bool:
    """判断选项正文是否应为中文叙述（却被整段替换成英文）。"""
    body = (body or "").strip()
    if not body or re.search(r"[\u4e00-\u9fff]", body):
        return False
    if is_english_keyword_only_option(body):
        return False
    if should_force_cloud_concepts_english(body):
        return False
    if _SEMANTIC_EN_RE.search(body):
        return True
    return len(body.split()) >= 7


def _fix_en_zh_spacing(text: str) -> str:
    text = re.sub(r"([A-Za-z0-9)])([\u4e00-\u9fff])", r"\1 \2", text)
    text = re.sub(r"([\u4e00-\u9fff])([A-Za-z(])", r"\1 \2", text)
    return re.sub(r"  +", " ", text)


def normalize_ec2_terms(text: str) -> str:
    """将孤立出现的 EC2 实例统一为 Amazon EC2 instances。"""
    if not text:
        return text
    text = re.sub(r"(?<!Amazon )EC2 instances", "Amazon EC2 instances", text, flags=re.IGNORECASE)
    text = re.sub(r"(?<!Amazon )EC2 Instances", "Amazon EC2 instances", text)
    text = re.sub(r"(?<!Amazon )EC2 实例", "Amazon EC2 instances", text)
    text = re.sub(r"(?<!Amazon )EC2实例", "Amazon EC2 instances", text)
    text = re.sub(
        r"(Amazon EC2 instances)([\u4e00-\u9fff])",
        r"\1 \2",
        text,
    )
    return text


def fix_explanation_phrases(text: str) -> str:
    if not text:
        return text
    for old, new in _EXPLANATION_PHRASE_FIXES:
        if old in text:
            text = text.replace(old, new)
    return text


def _apply_replacements(text: str, replacements: Iterable[tuple[str, str]]) -> str:
    if not text:
        return text
    for zh, en in replacements:
        if zh in text:
            text = text.replace(zh, en)
    for old, new in _POST_FIXES:
        if old in text:
            text = text.replace(old, new)
    return _fix_en_zh_spacing(text)


def restore_option(option: str) -> str:
    """还原误译服务名，再把官方中文考试术语写成考试指南用词。"""
    if not option or ". " not in option:
        text = _apply_replacements(option, _REPLACEMENTS)
        text = normalize_ec2_terms(text)
        return apply_official_zh_exam_terms(text, whole_option=True)
    letter, body = option.split(". ", 1)
    body = _apply_replacements(body, _REPLACEMENTS)
    body = normalize_ec2_terms(body)
    return apply_official_zh_exam_terms(f"{letter}. {body}", whole_option=True)


def restore_aws_english_terms(text: str, *, domain: str = "") -> str:
    """还原误译服务名，再套用官方中文考试术语。"""
    text = _apply_replacements(text, _REPLACEMENTS)
    text = normalize_ec2_terms(text)
    text = fix_explanation_phrases(text)
    if domain == "Cloud Concepts":
        text = normalize_cloud_concepts_text(text)
    return apply_official_zh_exam_terms(text)


def restore_question_fields(question: dict) -> dict:
    """就地修复题目 dict 的 question / options / explanation。"""
    domain = question.get("domain", "")
    if question.get("question"):
        question["question"] = restore_aws_english_terms(
            question["question"], domain=domain,
        )
    if question.get("options"):
        question["options"] = [restore_option(o) for o in question["options"]]
    if question.get("explanation"):
        question["explanation"] = restore_aws_english_terms(
            question["explanation"], domain=domain,
        )
    apply_official_zh_to_question(question)
    return question