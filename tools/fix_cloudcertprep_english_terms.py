#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量将 CloudCertPrep 题库中误译为中文的 AWS 服务名/关键词还原为英文，
并恢复被误替换成整段英文的中文选项。

用法：
    python tools/fix_cloudcertprep_english_terms.py
    python tools/fix_cloudcertprep_english_terms.py --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import re

from data.aws_english_terms import (  # noqa: E402
    fix_explanation_phrases,
    is_english_keyword_only_option,
    normalize_ec2_terms,
    option_body_needs_chinese_restore,
    restore_aws_english_terms,
    restore_option,
    should_force_english_option,
)
from data.cloud_concepts_terms import (  # noqa: E402
    is_cloud_concepts_domain,
    normalize_cloud_concepts_question,
)
from data.cloudcertprep.domains import DOMAIN_FILE_MAP, SOURCE_RAW_BASE  # noqa: E402
from data.explanation_utils import rebuild_explanation_text  # noqa: E402
from tools.import_cloudcertprep import (  # noqa: E402
    CACHE_FILE,
    _cn_select_count,
    _split_explanation,
    write_question_file,
)


def _cache_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_cache() -> dict[str, str]:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _fetch_source_by_id() -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    for domain_num in DOMAIN_FILE_MAP:
        url = f"{SOURCE_RAW_BASE}/domain{domain_num}.json"
        with urllib.request.urlopen(url, timeout=120) as resp:
            items = json.loads(resp.read().decode("utf-8"))
        for raw in items:
            sid = raw.get("id")
            if sid:
                by_id[sid] = raw
    return by_id


# 翻译缓存未命中时的少量人工补译（整句选项）
_MANUAL_OPTION_ZH: dict[str, str] = {
    "Configure the underlying infrastructure of AWS services to meet all PCI DSS requirements": (
        "配置 AWS 服务的底层基础设施以满足所有 PCI DSS 要求"
    ),
}

_EXPLANATION_EN_TO_ZH: dict[str, str] = {
    "Configuring the underlying AWS infrastructure to meet PCI DSS requirements is not the customer's responsibility; AWS manages and maintains the physical infrastructure, hardware, and network to meet PCI standards, and customers are responsible only for how they configure the services built on top of that infrastructure.": (
        "配置底层 AWS 基础设施以满足 PCI DSS 要求并非客户的责任；"
        "AWS 负责管理和维护满足 PCI 标准的物理基础设施、硬件和网络，"
        "客户仅对其在此基础上配置的服务负责。"
    ),
}


def _cached_zh(text: str, cache: dict[str, str]) -> str | None:
    text = (text or "").strip()
    if not text:
        return None
    cached = cache.get(_cache_key(text))
    if cached and cached != text:
        return cached
    return _MANUAL_OPTION_ZH.get(text)


def _rebuild_question(
    question: dict,
    source: dict | None,
    cache: dict[str, str],
    *,
    domain: str = "",
) -> str:
    question_en = (
        (source or {}).get("question")
        or question.get("question_en")
        or ""
    ).strip()
    if question_en:
        cached = _cached_zh(question_en, cache)
        if cached and re.search(r"[\u4e00-\u9fff]", cached):
            zh = cached
        else:
            zh = question.get("question", "")
    else:
        zh = question.get("question", "")

    if question.get("is_multi"):
        answers = question.get("correct_answers", [])
        if len(answers) >= 2 and "选择" not in zh:
            zh = f"{zh}（选择{_cn_select_count(len(answers))}项）"

    return restore_aws_english_terms(zh, domain=domain)


def _rebuild_options(
    question: dict,
    source: dict | None,
    cache: dict[str, str],
) -> list[str]:
    options_en = (source or {}).get("options") or {}
    if not options_en:
        return [restore_option(o) for o in question.get("options", [])]

    rebuilt: list[str] = []
    for letter in sorted(options_en.keys()):
        en_body = (options_en[letter] or "").strip()
        current = next(
            (o for o in question.get("options", []) if o.startswith(f"{letter}. ")),
            f"{letter}. {en_body}",
        )
        _, current_body = (
            current.split(". ", 1) if ". " in current else (letter, current)
        )

        cached = _cached_zh(en_body, cache)
        if (
            should_force_english_option(en_body)
            and not option_body_needs_chinese_restore(en_body)
        ):
            zh_body = en_body
        elif cached and re.search(r"[\u4e00-\u9fff]", cached):
            zh_body = cached
        elif re.search(r"[\u4e00-\u9fff]", current_body):
            zh_body = current_body
        else:
            zh_body = en_body

        rebuilt.append(restore_option(f"{letter}. {zh_body}"))
    return rebuilt


def _rebuild_explanation(
    question: dict,
    source: dict | None,
    cache: dict[str, str],
    options: list[str],
    *,
    domain: str = "",
) -> str:
    if not source:
        return restore_aws_english_terms(
            question.get("explanation", ""),
            domain=domain,
        )

    expl_en = (source.get("explanation") or "").strip()
    correct_en, wrong_en = _split_explanation(expl_en)
    correct_zh = _cached_zh(correct_en, cache) or correct_en
    wrong_zh = _cached_zh(wrong_en, cache) if wrong_en else ""

    correct_zh = restore_aws_english_terms(
        normalize_ec2_terms(correct_zh),
        domain=domain,
    )
    wrong_zh = restore_aws_english_terms(
        normalize_ec2_terms(wrong_zh),
        domain=domain,
    )

    if not correct_zh and not wrong_zh:
        return restore_aws_english_terms(
            question.get("explanation", ""),
            domain=domain,
        )
    if wrong_zh:
        base = (
            "正确答案：\n\n"
            f"「{correct_zh}」\n\n"
            "错误选项分析：\n\n"
            f"{wrong_zh}"
        )
        text = rebuild_explanation_text(
            base,
            options,
            question.get("correct_answers", []),
        )
    else:
        text = f"正确答案：\n\n「{correct_zh}」"
    for en, zh in _EXPLANATION_EN_TO_ZH.items():
        text = text.replace(en, zh)
    return fix_explanation_phrases(normalize_ec2_terms(text))


def main() -> None:
    parser = argparse.ArgumentParser(description="还原 CloudCertPrep 题库 AWS 英文术语")
    parser.add_argument("--dry-run", action="store_true", help="仅统计变更，不写回文件")
    parser.add_argument(
        "--no-source",
        action="store_true",
        help="不拉取 CloudCertPrep 源 JSON",
    )
    args = parser.parse_args()

    cache = _load_cache()
    if not cache:
        raise SystemExit(f"未找到翻译缓存：{CACHE_FILE}")

    import data.cloudcertprep.multi_choice as mc_mod
    import data.cloudcertprep.single_choice as sc_mod

    importlib.reload(sc_mod)
    importlib.reload(mc_mod)

    source_by_id: dict[str, dict] = {}
    if not args.no_source:
        print("正在拉取 CloudCertPrep 源 JSON…")
        source_by_id = _fetch_source_by_id()
        print(f"  已加载 {len(source_by_id)} 道英文原题")

    singles = list(sc_mod.SINGLE_CHOICE_QUESTIONS)
    multis = list(mc_mod.MULTI_CHOICE_QUESTIONS)
    changed = 0
    restored_opts = 0

    for bucket in (singles, multis):
        for q in bucket:
            old_q = q.get("question", "")
            old_opts = list(q.get("options", []))
            old_exp = q.get("explanation", "")

            src = source_by_id.get(q.get("source_id", ""))
            domain = q.get("domain", "")
            q["question"] = _rebuild_question(q, src, cache, domain=domain)
            q["options"] = _rebuild_options(q, src, cache)
            q["explanation"] = _rebuild_explanation(
                q, src, cache, q["options"], domain=domain,
            )
            if is_cloud_concepts_domain(domain):
                normalize_cloud_concepts_question(q)

            for o in old_opts:
                body = o.split(". ", 1)[-1] if ". " in o else o
                if not re.search(r"[\u4e00-\u9fff]", body) and not is_english_keyword_only_option(body):
                    restored_opts += 1
                    break
            if (
                q.get("question") != old_q
                or q.get("options") != old_opts
                or q.get("explanation") != old_exp
            ):
                changed += 1

    total = len(singles) + len(multis)
    print(f"共 {total} 题，更新 {changed} 题；恢复中文语意选项约 {restored_opts} 题")

    if args.dry_run:
        return

    out_single = ROOT / "data" / "cloudcertprep" / "single_choice.py"
    out_multi = ROOT / "data" / "cloudcertprep" / "multi_choice.py"

    write_question_file(
        out_single,
        "SINGLE_CHOICE_QUESTIONS",
        singles,
        title="CloudCertPrep CLF-C02 单选题库（自动生成，请勿手改）",
    )
    write_question_file(
        out_multi,
        "MULTI_CHOICE_QUESTIONS",
        multis,
        title="CloudCertPrep CLF-C02 多选题库（自动生成，请勿手改）",
    )
    print(f"已写入 {out_single.name}、{out_multi.name}")

    from tools.audit_cloudcertprep_translations import (  # noqa: E402
        audit_questions,
        count_critical_issues,
    )

    importlib.reload(importlib.import_module("data.cloudcertprep.single_choice"))
    importlib.reload(importlib.import_module("data.cloudcertprep.multi_choice"))
    audit = audit_questions(fetch_source=not args.no_source)
    critical = count_critical_issues(audit)
    if critical:
        print(f"警告：仍有 {critical} 道高置信度题干问题，请运行 audit_cloudcertprep_translations.py")
    else:
        print("校验通过：未发现「正确答案出现在题干」或术语表污染问题")


if __name__ == "__main__":
    main()