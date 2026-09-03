# -*- coding: utf-8 -*-
"""解析文本结构化工具（CloudCertPrep 错误选项分段等）。"""

from __future__ import annotations

import re


def _split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]


def _split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", (text or "").strip())
    text = text.replace("**", "").strip()
    if not text:
        return []
    # 只按句号类标点拆；分号后的从句仍属同一选项说明
    parts = re.split(r"(?<=[。！？])\s*", text)
    return [p.strip() for p in parts if p.strip() and p.strip() not in "：:"]


def _option_entries(
    options: list[str],
    correct_answers: list[str],
) -> list[tuple[str, str]]:
    correct = set(correct_answers or [])
    entries: list[tuple[str, str]] = []
    for opt in options:
        match = re.match(r"^([A-E])\.\s*(.+)$", (opt or "").strip())
        if match and match.group(1) not in correct:
            entries.append((match.group(1), match.group(2).strip()))
    return entries


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", (text or "")).lower()


def _strip_alias(text: str) -> str:
    """去掉选项中的括号别名，如 (Amazon EBS)。"""
    return re.sub(r"\([^)]{1,40}\)", " ", text or "")


def _latin_tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z0-9]{1,}", _compact(_strip_alias(text))))


def _cjk_ngrams(text: str, sizes: tuple[int, ...] = (4, 3)) -> set[str]:
    cjk = "".join(re.findall(r"[\u4e00-\u9fff]+", text or ""))
    grams: set[str] = set()
    for n in sizes:
        if len(cjk) < n:
            continue
        for i in range(0, len(cjk) - n + 1):
            grams.add(cjk[i : i + n])
    return grams


def _lcs_len(a: str, b: str) -> int:
    if not a or not b:
        return 0
    if len(a) > 160:
        a = a[:160]
    if len(b) > 160:
        b = b[:160]
    prev = [0] * (len(b) + 1)
    best = 0
    for ca in a:
        curr = [0] * (len(b) + 1)
        for j, cb in enumerate(b, 1):
            if ca == cb:
                curr[j] = prev[j - 1] + 1
                if curr[j] > best:
                    best = curr[j]
        prev = curr
    return best


def _shared_latin(option_texts: list[str]) -> set[str]:
    counts: dict[str, int] = {}
    for text in option_texts:
        for tok in _latin_tokens(text):
            counts[tok] = counts.get(tok, 0) + 1
    return {tok for tok, n in counts.items() if n >= 2 and len(tok) >= 3}


def _unique_markers(option_text: str, sibling_texts: list[str]) -> set[str]:
    """仅保留本选项独有的 4 字中文片段和较长英文词，避免 3-gram 误伤。"""
    mine = _cjk_ngrams(option_text, (4,)) | {
        tok for tok in _latin_tokens(option_text) if len(tok) >= 4
    }
    others: set[str] = set()
    for sib in sibling_texts:
        if sib == option_text:
            continue
        others |= _cjk_ngrams(sib, (4,)) | {
            tok for tok in _latin_tokens(sib) if len(tok) >= 4
        }
    return mine - others


def _score_sentence_for_option(
    sentence: str,
    option_text: str,
    sibling_texts: list[str] | None = None,
    shared_latin: set[str] | None = None,
) -> int:
    sent = sentence or ""
    opt = option_text or ""
    s_comp = _compact(sent)
    o_comp = _compact(_strip_alias(opt))
    if not s_comp or not o_comp:
        return 0

    siblings = [t for t in (sibling_texts or []) if t != opt]

    if len(o_comp) >= 8 and o_comp in s_comp:
        return 1000 + len(o_comp)
    if len(o_comp) >= 8 and s_comp in o_comp:
        return 900 + len(s_comp)

    score = 0
    # 句首即选项（「高可用性」应对「高可用通过…」；对比句里的「可靠性」不应抢分）
    subject_hit = False
    for n in range(min(4, len(o_comp)), 2, -1):
        if s_comp.startswith(o_comp[:n]):
            score += 140 + n * 10
            subject_hit = True
            break
    if not subject_hit and len(o_comp) < 8 and o_comp in s_comp:
        score += 20

    distinct = o_comp
    s_for_lcs = s_comp
    if shared_latin:
        for tok in sorted(shared_latin, key=len, reverse=True):
            distinct = distinct.replace(tok, "")
            s_for_lcs = s_for_lcs.replace(tok, "")
    lcs = _lcs_len(s_for_lcs, distinct)
    if lcs >= 4:
        score += lcs * 6
    elif lcs >= 3:
        score += lcs * 3

    sent_markers = _latin_tokens(sent) | _cjk_ngrams(sent, (4,))
    unique = _unique_markers(opt, siblings)
    hits = unique & sent_markers
    if hits:
        score += 22 * len(hits)

    return score


_STRUCTURED_WRONG_RE = re.compile(
    r"「(?:([A-E])\.\s*)?([^」]+)」(?:是错误的|不是本题答案|不是本题应选的项)[：:](.*)",
    re.DOTALL,
)

_FALLBACK_REASON = "该项不是本题的正确选择"


def _all_option_entries(options: list[str]) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for opt in options:
        match = re.match(r"^([A-E])\.\s*(.+)$", (opt or "").strip())
        if match:
            entries.append((match.group(1), match.group(2).strip()))
    return entries


def _best_option_letter(
    text: str,
    candidates: list[tuple[str, str]],
    *,
    sibling_texts: list[str] | None = None,
    shared_latin: set[str] | None = None,
    prefer: str = "",
) -> tuple[str, int]:
    scores: dict[str, int] = {}
    for letter, opt in candidates:
        scores[letter] = _score_sentence_for_option(
            text, opt, sibling_texts, shared_latin,
        )
    if prefer and prefer in scores:
        best_letter = prefer
        best_score = scores[prefer]
    else:
        best_letter = ""
        best_score = 0
    for letter, score in scores.items():
        if score > best_score:
            best_score = score
            best_letter = letter
    return best_letter, best_score


def _wrong_label(question: str = "") -> str:
    q = question or ""
    if re.search(r"不是|不属于|不正确|except|not a benefit|which.+not", q, re.I):
        return "不是本题应选的项"
    return "是错误的"


def structure_wrong_option_analysis(
    wrong_text: str,
    options: list[str],
    correct_answers: list[str],
    *,
    question: str = "",
) -> list[str]:
    """
    将错误选项分析拆成与选项字母、选项正文一致的分段。

    按选项内容匹配原因，不按 A/B/C 出现顺序硬套，避免把正确选项的说明
    标成「是错误的」。
    """
    wrong_text = (wrong_text or "").strip()
    if not wrong_text:
        return []

    all_opts = _all_option_entries(options)
    wrong_opts = _option_entries(options, correct_answers)
    if not wrong_opts:
        return _split_paragraphs(wrong_text)

    opt_by_letter = {letter: text for letter, text in all_opts}
    wrong_set = {letter for letter, _ in wrong_opts}
    label = _wrong_label(question)
    sibling_texts = [text for _, text in all_opts]
    shared = _shared_latin(sibling_texts)

    assigned: dict[str, list[str]] = {letter: [] for letter, _ in wrong_opts}

    def _hint_from_quote(hint_letter: str, hint_text: str) -> str:
        if hint_letter in wrong_set:
            quoted = (hint_text or "").strip()
            actual = opt_by_letter.get(hint_letter, "")
            if not quoted or not actual:
                return hint_letter
            if (
                quoted[:10] in actual
                or actual[:10] in quoted
                or _score_sentence_for_option(quoted, actual, sibling_texts, shared) >= 8
            ):
                return hint_letter
        if hint_text:
            hinted, hscore = _best_option_letter(
                hint_text, wrong_opts,
                sibling_texts=sibling_texts, shared_latin=shared,
            )
            if hinted and hscore >= 8:
                return hinted
            compact_hint = _compact(hint_text)
            for letter, opt in wrong_opts:
                if compact_hint and (
                    compact_hint[:12] in _compact(opt)
                    or _compact(opt)[:12] in compact_hint
                ):
                    return letter
        return ""

    def _unique_hit_count(reason: str, option_text: str) -> int:
        markers = _unique_markers(option_text, sibling_texts)
        found = _latin_tokens(reason) | _cjk_ngrams(reason, (4,))
        return len(markers & found)

    def _assign(
        reason: str,
        hint_letter: str = "",
        hint_text: str = "",
        prev_target: str = "",
    ) -> str:
        reason = (reason or "").strip().rstrip("。！？；;")
        if not reason or reason in "*＊":
            return prev_target
        header_hint = _hint_from_quote(hint_letter, hint_text)
        default = prev_target if prev_target in wrong_set else header_hint
        best, score = _best_option_letter(
            reason, wrong_opts,
            sibling_texts=sibling_texts, shared_latin=shared, prefer=default,
        )
        target = ""
        if best and score >= 12 and best != default:
            default_score = _score_sentence_for_option(
                reason, opt_by_letter.get(default, ""), sibling_texts, shared,
            ) if default else 0
            best_unique = _unique_hit_count(reason, opt_by_letter.get(best, ""))
            default_unique = _unique_hit_count(
                reason, opt_by_letter.get(default, ""),
            ) if default else 0
            steal = (
                (best_unique >= 2 and default_unique == 0)
                or (score >= default_score + 30 and best_unique >= 1)
            )
            target = best if steal or not default else default
        elif best and score >= 12:
            target = best
        elif default:
            target = default
        if target in assigned:
            assigned[target].append(reason)
            return target
        return prev_target

    structured_hits = 0
    last_target = ""
    for para in _split_paragraphs(wrong_text):
        cleaned = para.strip().strip("*").strip()
        if not cleaned or cleaned in "：:":
            continue
        match = _STRUCTURED_WRONG_RE.search(cleaned)
        if match:
            structured_hits += 1
            hint_letter = match.group(1) or ""
            hint_text = (match.group(2) or "").strip()
            reason = match.group(3)
            sents = _split_sentences(reason) or [reason]
            block_default = _hint_from_quote(hint_letter, hint_text)
            last_target = block_default or last_target
            for sent in sents:
                last_target = _assign(sent, hint_letter, hint_text, last_target)
        else:
            for sent in _split_sentences(cleaned):
                last_target = _assign(sent, prev_target=last_target)

    if structured_hits == 0:
        last_target = ""
        for sent in _split_sentences(wrong_text):
            last_target = _assign(sent, prev_target=last_target)

    blocks: list[str] = []
    for letter, opt in wrong_opts:
        sents = assigned.get(letter) or []
        uniq: list[str] = []
        for sent in sents:
            if sent and sent not in uniq and sent != _FALLBACK_REASON:
                uniq.append(sent)
        if not uniq:
            uniq = [_FALLBACK_REASON]
        reason = "。".join(uniq)
        if not reason.endswith("。"):
            reason += "。"
        blocks.append(f"「{letter}. {opt}」{label}：{reason}")

    return blocks if blocks else [wrong_text]


def rebuild_explanation_text(
    explanation: str,
    options: list[str],
    correct_answers: list[str],
    *,
    question: str = "",
) -> str:
    """在保留「正确答案」区块的前提下，重写错误选项分析分段。"""
    raw = (explanation or "").replace("\\n", "\n").strip()
    if not raw or "错误选项分析" not in raw:
        return explanation

    match = re.split(r"\n\n错误选项分析[：:]\s*\n\n", raw, maxsplit=1)
    if len(match) != 2:
        match = re.split(r"错误选项分析[：:]\s*", raw, maxsplit=1)
    if len(match) != 2:
        return explanation

    head, wrong_part = match
    head = head.rstrip()
    key_split = re.split(r"\n\n\*\*(?:重点考点|考试重点)", wrong_part, maxsplit=1)
    wrong_body = key_split[0].strip()
    key_suffix = ""
    if len(key_split) == 2:
        key_suffix = "\n\n**重点考点" + key_split[1]

    blocks = structure_wrong_option_analysis(
        wrong_body, options, correct_answers, question=question,
    )
    if not blocks:
        return explanation

    new_wrong = "\n\n".join(blocks)
    return f"{head}\n\n错误选项分析：\n\n{new_wrong}{key_suffix}"