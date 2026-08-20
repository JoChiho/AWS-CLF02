#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 CloudCertPrep 仓库导入 CLF-C02 题库并生成中文化 Python 数据文件。

用法：
    python tools/import_cloudcertprep.py              # 全量导入（约 1050 题）
    python tools/import_cloudcertprep.py --limit 50   # 验证用：仅处理前 50 题
    python tools/import_cloudcertprep.py --no-translate  # 仅用缓存/跳过翻译（调试）

依赖：pip install deep-translator
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.aws_english_terms import (  # noqa: E402
    option_body_needs_chinese_restore,
    restore_aws_english_terms,
    restore_option,
    restore_question_fields,
    should_force_english_option,
)
from data.cloudcertprep.domains import DOMAIN_FILE_MAP, SOURCE_RAW_BASE  # noqa: E402

CACHE_FILE = ROOT / "tools" / "cloudcertprep_translation_cache.json"
REPORT_FILE = ROOT / "docs" / "cloudcertprep_import_report.txt"
OUT_SINGLE = ROOT / "data" / "cloudcertprep" / "single_choice.py"
OUT_MULTI = ROOT / "data" / "cloudcertprep" / "multi_choice.py"

_CN_COUNT = {
    1: "一", 2: "两", 3: "三", 4: "四", 5: "五",
    6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
}

# AWS / 技术术语保护（翻译前替换为占位符，译后还原）
_PROTECTED_TERMS = sorted(
    {
        "AWS Well-Architected Framework", "Well-Architected Framework",
        "Shared Responsibility Model", "Amazon EC2", "Amazon S3", "Amazon RDS",
        "Amazon VPC", "Amazon EBS", "Amazon EFS", "Amazon SQS", "Amazon SNS",
        "Amazon CloudFront", "Amazon Route 53", "Amazon CloudWatch",
        "Amazon GuardDuty", "Amazon Inspector", "Amazon Macie", "Amazon Cognito",
        "Amazon DynamoDB", "Amazon Redshift", "Amazon Aurora", "Amazon Lambda",
        "Amazon API Gateway", "Amazon ECS", "Amazon EKS", "Amazon EMR",
        "Amazon Athena", "Amazon Kinesis", "Amazon ElastiCache", "Amazon Glacier",
        "Amazon Lightsail", "Amazon WorkSpaces", "Amazon Connect",
        "AWS IAM", "AWS KMS", "AWS WAF", "AWS Shield", "AWS Config",
        "AWS CloudTrail", "AWS CloudFormation", "AWS Organizations",
        "AWS Control Tower", "AWS Trusted Advisor", "AWS Cost Explorer",
        "AWS Budgets", "AWS Artifact", "AWS Security Hub", "AWS Secrets Manager",
        "AWS Systems Manager", "AWS Direct Connect", "AWS Global Accelerator",
        "AWS Transit Gateway", "AWS Network Firewall", "AWS Firewall Manager",
        "AWS Certificate Manager", "AWS CloudHSM", "AWS Directory Service",
        "IAM Identity Center", "Service Control Policies", "Availability Zone",
        "Availability Zones", "Edge Locations", "Local Zones", "Wavelength Zones",
        "Reserved Instances", "On-Demand Instances", "Spot Instances",
        "Savings Plans", "Cost and Usage Report", "Multi-Factor Authentication",
        "EC2", "S3", "RDS", "VPC", "EBS", "EFS", "SQS", "SNS", "IAM", "KMS",
        "WAF", "API", "CLI", "SDK", "JSON", "HTTPS", "TLS", "SSL", "DNS",
        "DDoS", "MFA", "ACL", "NACL", "SCP", "CMK", "SSE", "PII", "RTO", "RPO",
        "CapEx", "OpEx", "Route 53", "CloudFront", "CloudWatch", "CloudTrail",
        "CloudFormation", "GuardDuty", "Inspector", "Macie", "Cognito",
        "DynamoDB", "Redshift", "Lambda", "CloudHSM", "Artifact", "Organizations",
        "Elastic Load Balancing", "Elastic Load Balancer", "Application Load Balancer",
        "Network Load Balancer", "Auto Scaling", "Elastic Beanstalk", "Elastic File System",
        "Elastic Block Store", "Serverless", "Multi-Factor Authentication", "Internet Gateway",
        "NAT Gateway", "Virtual Private Gateway", "Consolidated Billing", "Dedicated Hosts",
        "Dedicated Instances", "Placement Groups", "Security Groups", "Network ACL",
        "AWS Fargate", "AWS Batch", "AWS Glue", "AWS Step Functions", "AWS AppSync",
        "AWS DataSync", "AWS Snowball", "AWS Snowmobile", "AWS Outposts", "AWS App Runner",
        "AWS Migration Hub", "AWS Service Catalog", "AWS Marketplace", "AWS CodePipeline",
        "AWS CodeBuild", "AWS CodeDeploy", "AWS CodeCommit", "AWS Database Migration Service",
        "AWS Storage Gateway", "AWS Resource Groups", "AWS Health Dashboard",
        "AWS Cost and Usage Report", "AWS Well-Architected Tool", "AWS Pricing Calculator",
        "AWS Management Console", "AWS Professional Services", "Amazon Pinpoint",
        "Amazon Comprehend", "Amazon Transcribe", "Amazon Rekognition", "Amazon Polly",
        "Amazon Lex", "Amazon Neptune", "Amazon DocumentDB", "Amazon OpenSearch Service",
        "Amazon EventBridge", "Amazon API Gateway", "Amazon ElastiCache", "Amazon EMR",
        "Amazon ECS", "Amazon EKS", "Amazon MQ", "Amazon WorkSpaces", "Amazon AppStream",
        "Operational Excellence", "Performance Efficiency", "Cost Optimization",
        "Reliability", "Shared Responsibility Model", "On-Demand", "Spot Fleet",
    },
    key=len,
    reverse=True,
)


def _protect_terms(text: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    protected = text
    for i, term in enumerate(_PROTECTED_TERMS):
        if term in protected:
            token = f"⟦T{i}⟧"
            mapping[token] = term
            protected = protected.replace(term, token)
    return protected, mapping


def _restore_terms(text: str, mapping: dict[str, str]) -> str:
    for token, term in mapping.items():
        text = text.replace(token, term)
    return text


def _cache_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_cache() -> dict[str, str]:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_cache(cache: dict[str, str]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def _get_translator():
    try:
        from deep_translator import GoogleTranslator
    except ImportError as exc:
        raise SystemExit(
            "缺少 deep-translator，请运行：pip install deep-translator"
        ) from exc
    return GoogleTranslator(source="en", target="zh-CN")


_SPLIT = "\n<<<CCP_SPLIT>>>\n"
_translator = None


def _translate_protected(text: str) -> str:
    global _translator
    if _translator is None:
        _translator = _get_translator()
    protected, mapping = _protect_terms(text)
    for attempt in range(4):
        try:
            translated = _translator.translate(protected)
            break
        except Exception:
            if attempt == 3:
                translated = text
            else:
                time.sleep(1.0 * (attempt + 1))
    else:
        translated = text
    translated = _restore_terms(translated or text, mapping)
    translated = _polish_translation(translated)
    return restore_aws_english_terms(translated)


def translate_text(text: str, cache: dict[str, str], *, enabled: bool = True) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    key = _cache_key(text)
    if key in cache:
        return cache[key]
    if not enabled:
        cache[key] = text
        return text
    translated = _translate_protected(text)
    cache[key] = translated
    return translated


def translate_batch(texts: list[str], cache: dict[str, str], *, enabled: bool = True) -> list[str]:
    """批量翻译，减少 API 调用次数。"""
    results = [""] * len(texts)
    pending: list[tuple[int, str]] = []
    for i, text in enumerate(texts):
        text = (text or "").strip()
        if not text:
            continue
        key = _cache_key(text)
        if key in cache:
            results[i] = cache[key]
        elif not enabled:
            cache[key] = text
            results[i] = text
        else:
            pending.append((i, text))

    if pending:
        combined = _SPLIT.join(t for _, t in pending)
        ckey = _cache_key(combined)
        if ckey in cache:
            parts = cache[ckey].split(_SPLIT)
        else:
            translated = _translate_protected(combined)
            cache[ckey] = translated
            parts = translated.split(_SPLIT)
            time.sleep(0.12)
        if len(parts) != len(pending):
            parts = [_translate_protected(t) for _, t in pending]
        for (idx, orig), part in zip(pending, parts):
            part = _polish_translation(part.strip())
            cache[_cache_key(orig)] = part
            results[idx] = part
    return results


def _polish_translation(text: str) -> str:
    fixes = {
        "亚马逊": "Amazon",
        "云观察": "CloudWatch",
        "云跟踪": "CloudTrail",
        "云形成": "CloudFormation",
        "负责共担": "责任共担",
        "按需实例": "On-Demand 实例",
    }
    for old, new in fixes.items():
        text = text.replace(old, new)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _cn_select_count(n: int) -> str:
    return _CN_COUNT.get(n, str(n))


def _normalize_answer(raw: dict) -> list[str]:
    ans = raw.get("answer", [])
    if isinstance(ans, str):
        return [ans]
    return list(ans)


def _format_options(options: dict[str, str]) -> list[str]:
    letters = sorted(options.keys())
    return [f"{letter}. {options[letter]}" for letter in letters]


def _split_explanation(en: str) -> tuple[str, str]:
    en = (en or "").strip()
    if not en:
        return "", ""
    parts = [p.strip() for p in re.split(r"\n+", en) if p.strip()]
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], "\n".join(parts[1:])


def _format_explanation_zh(
    correct_zh: str,
    wrong_zh: str,
    *,
    options_zh: list[str],
    correct_answers: list[str],
) -> str:
    from data.explanation_utils import rebuild_explanation_text

    if not correct_zh and not wrong_zh:
        return "（暂无解析）"
    if wrong_zh:
        base = (
            "正确答案：\n\n"
            f"「{correct_zh}」\n\n"
            "错误选项分析：\n\n"
            f"{wrong_zh}"
        )
        return rebuild_explanation_text(base, options_zh, correct_answers)
    return f"正确答案：\n\n「{correct_zh}」"


def convert_question(
    raw: dict,
    domain: str,
    *,
    seq_single: int,
    seq_multi: int,
    cache: dict[str, str],
    translate: bool,
) -> tuple[dict, int, int]:
    is_multi = bool(raw.get("isMultiAnswer"))
    answers = _normalize_answer(raw)
    options_en = raw.get("options") or {}

    question_en = (raw.get("question") or "").strip()
    correct_en, wrong_en = _split_explanation(raw.get("explanation", ""))
    opt_texts = [options_en[letter] for letter in sorted(options_en.keys())]
    batch = [question_en, correct_en, wrong_en] + opt_texts
    batch_zh = translate_batch(batch, cache, enabled=translate)

    question_zh = batch_zh[0]
    correct_zh = batch_zh[1]
    wrong_zh = batch_zh[2]
    opt_zh_list = batch_zh[3:]

    if is_multi and len(answers) >= 2:
        count_token = _cn_select_count(len(answers))
        if "选择" not in question_zh:
            question_zh = f"{question_zh}（选择{count_token}项）"

    options_zh = []
    for letter, opt_zh, opt_en in zip(
        sorted(options_en.keys()), opt_zh_list, opt_texts,
    ):
        en_stripped = (opt_en or "").strip()
        if (
            should_force_english_option(en_stripped)
            and not option_body_needs_chinese_restore(en_stripped)
        ):
            options_zh.append(f"{letter}. {en_stripped}")
        else:
            options_zh.append(restore_option(f"{letter}. {opt_zh}"))

    explanation_zh = _format_explanation_zh(
        correct_zh,
        wrong_zh,
        options_zh=options_zh,
        correct_answers=answers,
    )

    if is_multi:
        qid = f"CCP-M{seq_multi:03d}"
        seq_multi += 1
    else:
        qid = f"CCP-S{seq_single:03d}"
        seq_single += 1

    item = {
        "id": qid,
        "question": question_zh,
        "question_en": question_en,
        "options": options_zh,
        "correct_answers": answers,
        "explanation": explanation_zh,
        "domain": domain,
        "is_multi": is_multi,
        "source": "cloudcertprep",
        "source_id": raw.get("id", ""),
    }
    if raw.get("taskStatement"):
        item["task_statement"] = raw["taskStatement"]
    if raw.get("services"):
        item["services"] = raw["services"]

    restore_question_fields(item)
    return item, seq_single, seq_multi


def fetch_domain_json(domain_num: int) -> list[dict]:
    url = f"{SOURCE_RAW_BASE}/domain{domain_num}.json"
    with urllib.request.urlopen(url, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _py_repr_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def write_question_file(
    path: Path,
    var_name: str,
    questions: list[dict],
    *,
    title: str,
) -> None:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""',
        title,
        "",
        "来源：https://github.com/nastaso/cloudcertprep （MIT）",
        "运行 tools/import_cloudcertprep.py 可重新生成。",
        '"""',
        f"{var_name} = [",
    ]
    for q in questions:
        lines.append("    {")
        for key in (
            "id", "question", "question_en", "options", "correct_answers",
            "explanation", "domain", "is_multi", "source", "source_id",
            "task_statement", "services",
        ):
            if key not in q:
                continue
            val = q[key]
            if key == "options":
                lines.append(f'        "options": {json.dumps(val, ensure_ascii=False)},')
            elif key == "correct_answers":
                lines.append(f'        "correct_answers": {json.dumps(val, ensure_ascii=False)},')
            elif key == "services":
                lines.append(f'        "services": {json.dumps(val, ensure_ascii=False)},')
            elif isinstance(val, bool):
                lines.append(f'        "{key}": {str(val)},')
            else:
                lines.append(f'        "{key}": {_py_repr_str(str(val))},')
        lines.append("    },")
    lines.append("]")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_report(
    singles: list[dict],
    multis: list[dict],
    *,
    elapsed: float,
    translated: bool,
) -> None:
    from collections import Counter

    c = Counter()
    for q in singles + multis:
        c[q["domain"]] += 1
    total = len(singles) + len(multis)
    lines = [
        "CloudCertPrep CLF-C02 导入报告",
        "=" * 40,
        f"总题数: {total}",
        f"单选: {len(singles)}",
        f"多选: {len(multis)}",
        f"翻译: {'是' if translated else '否（使用缓存/原文）'}",
        f"耗时: {elapsed:.1f}s",
        "",
        "领域分布:",
    ]
    for domain, n in sorted(c.items()):
        lines.append(f"  {domain}: {n} ({100 * n / total:.1f}%)")
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="导入 CloudCertPrep CLF-C02 题库")
    parser.add_argument("--limit", type=int, default=0, help="仅处理前 N 题（0=全部）")
    parser.add_argument(
        "--no-translate",
        action="store_true",
        help="不调用翻译 API（仅用缓存，无缓存则保留英文）",
    )
    args = parser.parse_args()

    cache = _load_cache()
    translate = not args.no_translate
    singles: list[dict] = []
    multis: list[dict] = []
    seq_s, seq_m = 1, 1
    processed = 0
    t0 = time.time()

    for domain_num, domain_name in DOMAIN_FILE_MAP.items():
        raw_list = fetch_domain_json(domain_num)
        print(f"domain{domain_num} ({domain_name}): {len(raw_list)} 题")
        for raw in raw_list:
            if args.limit and processed >= args.limit:
                break
            item, seq_s, seq_m = convert_question(
                raw,
                domain_name,
                seq_single=seq_s,
                seq_multi=seq_m,
                cache=cache,
                translate=translate,
            )
            if item["is_multi"]:
                multis.append(item)
            else:
                singles.append(item)
            processed += 1
            if processed % 25 == 0:
                _save_cache(cache)
                print(f"  已处理 {processed} 题…")
        if args.limit and processed >= args.limit:
            break

        _save_cache(cache)
        write_question_file(
            OUT_SINGLE,
            "SINGLE_CHOICE_QUESTIONS",
            singles,
            title="CloudCertPrep CLF-C02 单选题库（自动生成，请勿手改）",
        )
        write_question_file(
            OUT_MULTI,
            "MULTI_CHOICE_QUESTIONS",
            multis,
            title="CloudCertPrep CLF-C02 多选题库（自动生成，请勿手改）",
        )
        print(f"  已写入检查点：单选 {len(singles)} + 多选 {len(multis)}")

    _save_cache(cache)
    elapsed = time.time() - t0
    write_report(singles, multis, elapsed=elapsed, translated=translate)
    print(f"\n完成：单选 {len(singles)} + 多选 {len(multis)} = {len(singles) + len(multis)} 题")
    print(f"输出：{OUT_SINGLE.name}, {OUT_MULTI.name}")
    print(f"报告：{REPORT_FILE}")


if __name__ == "__main__":
    main()