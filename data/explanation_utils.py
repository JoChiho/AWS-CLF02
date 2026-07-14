# -*- coding: utf-8 -*-
"""解析文本结构化工具（CloudCertPrep 错误选项分段等）。"""

from __future__ import annotations

import re


def _split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]


def _split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return []
    parts = re.split(r"(?<=[。！？])\s*", text)
    return [p.strip() for p in parts if p.strip()]


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


def _keywords_for_match(text: str, limit: int = 6) -> list[str]:
    """提取用于匹配句子的关键词（去标点、取有意义片段）。"""
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", " ", text)
    tokens = [t for t in cleaned.split() if len(t) >= 2]
    if not tokens:
        return [text[:8]] if text else []
    keys: list[str] = []
    for token in tokens:
        if token not in keys:
            keys.append(token)
        if len(keys) >= limit:
            break
    if len(text) >= 4:
        keys.append(text[: min(12, len(text))])
    return keys


def _score_sentence_for_option(sentence: str, option_text: str) -> int:
    sentence_l = sentence.lower()
    option_l = option_text.lower()
    if option_l and option_l in sentence_l:
        return 1000 + len(option_l)
    if option_l and sentence_l.startswith(option_l[: min(8, len(option_l))]):
        return 800
    score = 0
    for kw in _keywords_for_match(option_text):
        if kw.lower() in sentence_l:
            score += len(kw)
    return score


def structure_wrong_option_analysis(
    wrong_text: str,
    options: list[str],
    correct_answers: list[str],
) -> list[str]:
    """
    将一整段错误选项分析拆成与自建题库一致的分段格式：

    「A. 选项文字」是错误的：原因说明
    """
    wrong_text = (wrong_text or "").strip()
    if not wrong_text:
        return []

    wrong_opts = _option_entries(options, correct_answers)
    if not wrong_opts:
        return _split_paragraphs(wrong_text)

    # 已是结构化格式则直接按段落返回
    if wrong_text.count("是错误的") >= 2 and "「" in wrong_text:
        blocks = _split_paragraphs(wrong_text)
        if len(blocks) > 1:
            return blocks

    sentences = _split_sentences(wrong_text)
    if not sentences:
        return [wrong_text]

    # 句数与错误选项数一致时，按顺序一一对应（CloudCertPrep 常见模式）
    if len(sentences) == len(wrong_opts):
        return [
            f"「{letter}. {opt}」是错误的：{sent.rstrip('。！？')}。"
            for (letter, opt), sent in zip(wrong_opts, sentences)
        ]

    # 否则按关键词将句子归属到最匹配的错误选项
    assigned: dict[str, list[str]] = {letter: [] for letter, _ in wrong_opts}
    for sent in sentences:
        best_letter = ""
        best_score = 0
        for letter, opt in wrong_opts:
            score = _score_sentence_for_option(sent, opt)
            if score > best_score:
                best_score = score
                best_letter = letter
        if best_letter and best_score > 0:
            assigned[best_letter].append(sent.rstrip("。！？"))
        elif wrong_opts:
            # 兜底：按顺序填入尚未分配的选项
            for letter, _ in wrong_opts:
                if len(assigned[letter]) < 1:
                    assigned[letter].append(sent.rstrip("。！？"))
                    break

    blocks: list[str] = []
    for letter, opt in wrong_opts:
        sents = assigned.get(letter) or []
        if not sents:
            continue
        reason = "。".join(sents)
        if not reason.endswith("。"):
            reason += "。"
        blocks.append(f"「{letter}. {opt}」是错误的：{reason}")

    return blocks if blocks else [wrong_text]


def rebuild_explanation_text(
    explanation: str,
    options: list[str],
    correct_answers: list[str],
) -> str:
    """在保留「正确答案」区块的前提下，重写错误选项分析分段。"""
    raw = (explanation or "").replace("\\n", "\n").strip()
    if not raw or "错误选项分析" not in raw:
        return explanation

    match = re.split(r"\n\n错误选项分析[：:]\s*\n\n", raw, maxsplit=1)
    if len(match) != 2:
        return explanation

    head, wrong_part = match
    key_split = re.split(r"\n\n\*\*(?:重点考点|考试重点)", wrong_part, maxsplit=1)
    wrong_body = key_split[0].strip()
    key_suffix = ""
    if len(key_split) == 2:
        key_suffix = "\n\n**重点考点" + key_split[1]

    blocks = structure_wrong_option_analysis(
        wrong_body, options, correct_answers,
    )
    if len(blocks) <= 1 and blocks == _split_paragraphs(wrong_body):
        return explanation

    new_wrong = "\n\n".join(blocks)
    return f"{head}\n\n错误选项分析：\n\n{new_wrong}{key_suffix}"