#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审计 CloudCertPrep 题库翻译：检测「正确答案出现在题干」及与英文原题/翻译缓存的偏差。

用法：
    python tools/audit_cloudcertprep_translations.py
    python tools/audit_cloudcertprep_translations.py --json report.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.aws_english_terms import _build_glossary_service_reverse  # noqa: E402
from data.cloudcertprep.domains import DOMAIN_FILE_MAP, SOURCE_RAW_BASE  # noqa: E402
from tools.import_cloudcertprep import CACHE_FILE, _cn_select_count  # noqa: E402

import data.cloudcertprep.multi_choice as mc_mod  # noqa: E402
import data.cloudcertprep.single_choice as sc_mod  # noqa: E402

# 题干中合法出现服务名的英文句式（原题本就点名服务）
_LEGIT_SERVICE_CONTEXT = re.compile(
    r"\b(?:like|such as|using|with|for|from|to|including|e\.g\.|eg\.)\b",
    re.IGNORECASE,
)

# 忽略仅空格/标点差异的缓存比对
_NORMALIZE_WS = re.compile(r"\s+")


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


def _normalize_compare(text: str) -> str:
    text = _NORMALIZE_WS.sub("", text or "")
    return text.replace("（", "(").replace("）", ")")


def _expected_question_zh(
    question_en: str,
    cache: dict[str, str],
    *,
    is_multi: bool,
    answer_count: int,
) -> str | None:
    en = (question_en or "").strip()
    if not en:
        return None
    zh = cache.get(_cache_key(en))
    if not zh:
        return None
    if is_multi and answer_count >= 2 and "选择" not in zh:
        zh = f"{zh}（选择{_cn_select_count(answer_count)}项）"
    return zh


def _option_bodies(options: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for opt in options:
        if ". " in opt:
            letter, body = opt.split(". ", 1)
            out[letter.strip()] = body.strip()
    return out


def _service_tokens(text: str) -> set[str]:
    tokens: set[str] = set()
    for m in re.finditer(
        r"(?:Amazon|AWS)\s+[A-Za-z][A-Za-z0-9 .()/-]*[A-Za-z0-9)]",
        text,
    ):
        tokens.add(m.group(0).strip())
    for m in re.finditer(r"\bDMS\b", text):
        tokens.add("DMS")
    return tokens


def _english_mentions_service(question_en: str, service: str) -> bool:
    en = question_en or ""
    svc = service.strip()
    if not svc:
        return False
    if svc in en:
        return True
    # AWS Database Migration Service (AWS DMS) vs AWS DMS
    core = re.sub(r"^AWS\s+", "", svc)
    core = re.sub(r"^Amazon\s+", "", core)
    if core and core in en:
        return True
    return False


def _is_trivial_option(body: str) -> bool:
    """过短或纯数字的选项不参与题干循环检测。"""
    body = (body or "").strip()
    if len(body) <= 2:
        return True
    if re.fullmatch(r"[\d.%]+", body):
        return True
    return False


def _strip_option_paren(body: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", (body or "").strip()).strip()


def _detect_answer_in_stem(
    question: dict,
    source: dict | None,
) -> list[dict]:
    """检测「正确答案泄露到题干」：仅报告高置信度问题，避免框架名/类别名误报。"""
    issues: list[dict] = []
    zh = question.get("question", "")
    en = (source or {}).get("question") or question.get("question_en") or ""
    opts = _option_bodies(question.get("options", []))

    for letter in question.get("correct_answers", []):
        body = opts.get(letter, "")
        if not body or _is_trivial_option(body):
            continue

        # 完整选项正文出现在题干（长度门槛降低误报）
        if len(body) >= 8 and body in zh:
            issues.append({
                "type": "answer_in_stem_exact",
                "letter": letter,
                "option": body,
                "detail": "正确选项全文出现在题干",
            })
            continue

        # 服务名选项：英文原题未点名该服务，但中文题干出现同一服务名
        if body.startswith(("Amazon ", "AWS ")):
            core = _strip_option_paren(body)
            if len(core) >= 8 and core in zh and not _english_mentions_service(en, core):
                if not (_LEGIT_SERVICE_CONTEXT.search(en) and core.lower() in en.lower()):
                    issues.append({
                        "type": "answer_service_pollution",
                        "letter": letter,
                        "option": body,
                        "service": core,
                        "detail": "题干出现正确答案服务名，但英文原题未提及",
                    })

    return issues


def _detect_glossary_pollution(question: dict, source: dict | None) -> list[dict]:
    """检测术语表反向替换：英文为通用概念，中文却出现某服务名且该服务为正确答案。"""
    issues: list[dict] = []
    zh = question.get("question", "")
    en = ((source or {}).get("question") or question.get("question_en") or "").lower()
    if not en or not zh:
        return issues

    reverse = dict(_build_glossary_service_reverse())
    opts = _option_bodies(question.get("options", []))
    correct_bodies = [
        opts.get(letter, "")
        for letter in question.get("correct_answers", [])
    ]

    for zh_term, en_service in reverse.items():
        if zh_term not in zh:
            continue
        if en_service.lower() not in en:
            # 英文无该服务名，中文却通过通用词替换成服务
            for body in correct_bodies:
                if en_service in body or body.startswith(en_service.split()[0]):
                    issues.append({
                        "type": "glossary_pollution",
                        "zh_term": zh_term,
                        "en_service": en_service,
                        "option": body,
                        "detail": f"英文无「{en_service}」，题干含「{zh_term}」且正确答案为该服务",
                    })
                    break
    return issues


def count_critical_issues(report: dict) -> int:
    """高置信度题干问题：正确选项/服务名泄露（不含缓存空格差异与术语表启发式误报）。"""
    return len(report.get("answer_in_stem", []))


def audit_questions(
    *,
    fetch_source: bool = True,
) -> dict:
    cache = _load_cache()
    source_by_id = _fetch_source_by_id() if fetch_source else {}

    all_q = list(sc_mod.SINGLE_CHOICE_QUESTIONS) + list(mc_mod.MULTI_CHOICE_QUESTIONS)
    report = {
        "total": len(all_q),
        "answer_in_stem": [],
        "cache_mismatch_semantic": [],
        "glossary_pollution": [],
        "summary": {},
    }

    for q in all_q:
        sid = q.get("source_id", "")
        src = source_by_id.get(sid)
        en = (src or {}).get("question") or q.get("question_en") or ""
        zh = q.get("question", "")

        expected = _expected_question_zh(
            en,
            cache,
            is_multi=bool(q.get("is_multi")),
            answer_count=len(q.get("correct_answers", [])),
        )
        if expected and _normalize_compare(expected) != _normalize_compare(zh):
            report["cache_mismatch_semantic"].append({
                "id": q["id"],
                "source_id": sid,
                "question_en": en,
                "question_zh": zh,
                "expected_zh": expected,
            })

        for issue in _detect_answer_in_stem(q, src):
            report["answer_in_stem"].append({
                "id": q["id"],
                "source_id": sid,
                "question_en": en,
                "question_zh": zh,
                **issue,
            })

        for issue in _detect_glossary_pollution(q, src):
            if not any(
                x["id"] == q["id"] and x.get("type") == issue["type"]
                for x in report["glossary_pollution"]
            ):
                report["glossary_pollution"].append({
                    "id": q["id"],
                    "source_id": sid,
                    "question_en": en,
                    "question_zh": zh,
                    **issue,
                })

    report["summary"] = {
        "answer_in_stem": len(report["answer_in_stem"]),
        "cache_mismatch_semantic": len(report["cache_mismatch_semantic"]),
        "glossary_pollution": len(report["glossary_pollution"]),
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="审计 CloudCertPrep 翻译与题干循环问题")
    parser.add_argument("--json", type=Path, help="导出 JSON 报告路径")
    parser.add_argument("--no-source", action="store_true", help="不拉取英文原题")
    args = parser.parse_args()

    print("正在审计 CloudCertPrep 题库…")
    report = audit_questions(fetch_source=not args.no_source)

    s = report["summary"]
    print(f"共 {report['total']} 题")
    print(f"  正确答案出现在题干: {s['answer_in_stem']}")
    print(f"  与翻译缓存语义不一致: {s['cache_mismatch_semantic']}")
    print(f"  术语表污染（通用词→服务名）: {s['glossary_pollution']}")

    if report["answer_in_stem"]:
        print("\n【正确答案出现在题干】")
        for row in report["answer_in_stem"]:
            print(f"- {row['id']} ({row['source_id']}) [{row['type']}]")
            print(f"  EN: {row['question_en'][:100]}")
            print(f"  ZH: {row['question_zh'][:100]}")
            print(f"  选项 {row.get('letter')}: {row.get('option', '')[:80]}")
            if row.get("service"):
                print(f"  服务: {row['service']}")

    if report["glossary_pollution"]:
        print("\n【术语表污染】")
        for row in report["glossary_pollution"]:
            print(f"- {row['id']} ({row['source_id']}): {row['detail']}")
            print(f"  ZH: {row['question_zh'][:100]}")

    if args.json:
        args.json.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\n报告已写入 {args.json}")


if __name__ == "__main__":
    main()