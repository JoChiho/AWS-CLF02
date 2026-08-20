# -*- coding: utf-8 -*-
"""
用户进度持久化模块（User Progress Persistence）

负责：
- 最近 10 次作答会话记录（timestamp, mode, total, correct, accuracy）
- 每道题目的累计正确/错误次数（永久累计，用于错题本）
- 提供查询、更新、错题本生成等功能

存储文件：项目根目录下的 user_data.json（与 main.py 同级，便于用户备份）
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from app_paths import get_app_root
from data.banks import BANK_CLOUDCERTPREP, BANK_KEYWORD_DRILL, BANK_NATIVE

# 进度文件位置（开发模式：项目根；打包后：exe 同级目录）
PROGRESS_FILE = get_app_root() / "user_data.json"

# 连续答对次数达到此值后自动标为「已掌握」
MASTER_STREAK_REQUIRED = 2

# CloudCertPrep 板块在 user_data.json 中的独立键（不污染自建 320 题进度）
CLOUDCERTPREP_PROGRESS_KEY = BANK_CLOUDCERTPREP


def _now_iso() -> str:
    """返回当前时间的 ISO 格式字符串"""
    return datetime.now().isoformat(timespec="seconds")


def _default_bank_section() -> Dict[str, Any]:
    """单个题库板块的进度结构（CloudCertPrep 等）。"""
    return {
        "sessions": [],
        "question_stats": {},
        "preferences": {},
    }


def _default_progress() -> Dict[str, Any]:
    """返回一个全新的进度数据结构"""
    return {
        "version": 1,
        "last_updated": _now_iso(),
        "sessions": [],           # 自建题库：最近 10 次会话
        "question_stats": {},     # 自建题库：qid -> 统计
        "preferences": {},        # 自建题库：UI 偏好
        CLOUDCERTPREP_PROGRESS_KEY: _default_bank_section(),
        BANK_KEYWORD_DRILL: _default_bank_section(),
    }


def _normalize_loaded_progress(data: Dict[str, Any]) -> Dict[str, Any]:
    """补齐版本与板块字段，兼容旧版 user_data.json。"""
    if "version" not in data:
        data["version"] = 1
    if "sessions" not in data:
        data["sessions"] = []
    if "question_stats" not in data:
        data["question_stats"] = {}
    if "last_updated" not in data:
        data["last_updated"] = _now_iso()
    if "preferences" not in data:
        data["preferences"] = {}
    for bank_key in (CLOUDCERTPREP_PROGRESS_KEY, BANK_KEYWORD_DRILL):
        section = data.setdefault(bank_key, _default_bank_section())
        for key in ("sessions", "question_stats", "preferences"):
            section.setdefault(key, [] if key == "sessions" else {})
    return data


def _get_bank_section(progress: Dict[str, Any], bank_id: str = BANK_NATIVE) -> Dict[str, Any]:
    """
    返回指定题库的进度分区。
    自建题库（native）使用顶层 sessions/question_stats/preferences，保持向后兼容。
    """
    if bank_id == BANK_NATIVE:
        progress.setdefault("sessions", [])
        progress.setdefault("question_stats", {})
        progress.setdefault("preferences", {})
        return progress
    section = progress.setdefault(bank_id, _default_bank_section())
    section.setdefault("sessions", [])
    section.setdefault("question_stats", {})
    section.setdefault("preferences", {})
    return section


def _default_question_stat() -> Dict[str, Any]:
    return {
        "correct_count": 0,
        "wrong_count": 0,
        "last_attempt": None,
        "last_answer": [],
        "consecutive_correct": 0,
        "mastered": False,
        "mastered_at": None,
    }


def _normalize_question_stat(qstat: Dict[str, Any]) -> Dict[str, Any]:
    """为旧版 user_data 补齐错题本扩展字段"""
    base = _default_question_stat()
    base.update(qstat)
    return base


def load_progress() -> Dict[str, Any]:
    """
    加载用户进度。
    如果文件不存在或损坏，返回默认空结构（静默处理，不打断用户）。
    """
    if not PROGRESS_FILE.exists():
        return _default_progress()

    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return _normalize_loaded_progress(data)
    except Exception:
        # 文件损坏时返回默认结构，避免程序崩溃
        return _default_progress()


def save_progress(data: Dict[str, Any]) -> bool:
    """
    保存进度到磁盘。
    返回是否成功。
    """
    try:
        data["last_updated"] = _now_iso()
        # 保证各板块 sessions 只保留最近 10 次（最新在前）
        sections = [data]
        for value in data.values():
            if isinstance(value, dict) and "sessions" in value:
                sections.append(value)
        for section in sections:
            if isinstance(section, dict) and len(section.get("sessions", [])) > 10:
                section["sessions"] = section["sessions"][:10]

        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def record_session(
    mode: str,
    total: int,
    correct: int,
    duration_sec: int = 0,
    answered: Optional[int] = None,
    bank_id: str = BANK_NATIVE,
) -> Dict[str, Any]:
    """
    记录一次练习会话（在用户点击“完成测试”时调用）。

    支持中途提交查看正确率：
    - total: 本次练习加载的题目总数（题库规模）
    - answered: 实际作答的题目数（若未提供则视为 = total）
    - correct: 作答题目中答对的数量
    - accuracy: 按 correct / answered 计算（更符合中途查看场景）

    mode 示例：
        "all"                           → 全部题目
        "single"                        → 单选题
        "multi"                         → 多选题
        "domain:Cloud Concepts"         → 按领域
        "wrong_book"                    → 错题本练习
    """
    progress = load_progress()
    section = _get_bank_section(progress, bank_id)

    answered = answered if answered is not None else total
    accuracy = (correct / answered * 100.0) if answered > 0 else 0.0

    session = {
        "timestamp": _now_iso(),
        "mode": mode,
        "total": total,
        "answered": answered,
        "correct": correct,
        "accuracy": round(accuracy, 1),
        "duration_sec": int(duration_sec),
    }

    section.setdefault("sessions", []).insert(0, session)
    section["sessions"] = section["sessions"][:10]

    save_progress(progress)
    return session


def update_question_stat(
    qid: str,
    is_correct: bool,
    user_answer: List[str],
    bank_id: str = BANK_NATIVE,
) -> None:
    """
    更新某道题的累计统计（每次用户提交答案并判定正误后调用）。
    """
    if not qid:
        return

    progress = load_progress()
    section = _get_bank_section(progress, bank_id)
    stats = section.setdefault("question_stats", {})

    qstat = _normalize_question_stat(stats.setdefault(qid, _default_question_stat()))

    if is_correct:
        qstat["correct_count"] += 1
        qstat["consecutive_correct"] = qstat.get("consecutive_correct", 0) + 1
        if qstat["consecutive_correct"] >= MASTER_STREAK_REQUIRED:
            qstat["mastered"] = True
            qstat["mastered_at"] = _now_iso()
    else:
        qstat["wrong_count"] += 1
        qstat["consecutive_correct"] = 0
        qstat["mastered"] = False
        qstat["mastered_at"] = None

    qstat["last_attempt"] = _now_iso()
    qstat["last_answer"] = user_answer[:]

    stats[qid] = qstat
    save_progress(progress)


def get_recent_sessions(
    limit: int = 10,
    bank_id: str = BANK_NATIVE,
) -> List[Dict[str, Any]]:
    """获取最近 N 次会话（默认 10），最新在前"""
    progress = load_progress()
    section = _get_bank_section(progress, bank_id)
    sessions = section.get("sessions", [])
    return sessions[:limit]


def get_question_stats(
    qid: str,
    bank_id: str = BANK_NATIVE,
) -> Optional[Dict[str, Any]]:
    """获取某题的累计统计"""
    progress = load_progress()
    section = _get_bank_section(progress, bank_id)
    raw = section.get("question_stats", {}).get(qid)
    return _normalize_question_stat(raw) if raw else None


def set_question_mastered(
    qid: str,
    mastered: bool = True,
    bank_id: str = BANK_NATIVE,
) -> bool:
    """手动标记/取消「已掌握」"""
    if not qid:
        return False

    progress = load_progress()
    section = _get_bank_section(progress, bank_id)
    stats = section.setdefault("question_stats", {})
    if qid not in stats:
        return False

    qstat = _normalize_question_stat(stats[qid])
    qstat["mastered"] = mastered
    qstat["mastered_at"] = _now_iso() if mastered else None
    if mastered:
        qstat["consecutive_correct"] = max(
            qstat.get("consecutive_correct", 0), MASTER_STREAK_REQUIRED
        )
    stats[qid] = qstat
    return save_progress(progress)


def _sort_wrong_entries(
    entries: List[Dict[str, Any]],
    sort_by: str,
) -> List[Dict[str, Any]]:
    if sort_by == "wrong_count":
        return sorted(
            entries,
            key=lambda e: (-e["wrong_count"], -e["error_rate"], e.get("last_attempt") or ""),
        )
    if sort_by == "last_wrong":
        return sorted(
            entries,
            key=lambda e: e.get("last_attempt") or "",
            reverse=True,
        )
    return sorted(
        entries,
        key=lambda e: (-e["error_rate"], -e["wrong_count"], e.get("last_attempt") or ""),
    )


def get_wrong_book_entries(
    sort_by: str = "error_rate",
    domain: Optional[str] = None,
    include_mastered: bool = False,
    bank_id: str = BANK_NATIVE,
) -> List[Dict[str, Any]]:
    """
    返回错题本条目（含统计与题目摘要），支持领域筛选与是否包含已掌握题目。
    """
    from data.banks import get_bank

    bank = get_bank(bank_id)
    stats = get_all_question_stats(bank_id=bank_id)
    entries: List[Dict[str, Any]] = []

    for qid, raw in stats.items():
        s = _normalize_question_stat(raw)
        if s.get("wrong_count", 0) <= 0:
            continue
        if not include_mastered and s.get("mastered"):
            continue

        q = bank.get_question_by_id(qid)
        q_domain = q.get("domain", "") if q else ""
        if domain and q_domain != domain:
            continue

        c = s.get("correct_count", 0)
        w = s.get("wrong_count", 0)
        total = c + w
        rate = (w / total * 100.0) if total > 0 else 0.0
        preview = ""
        if q:
            text = q.get("question", "")
            preview = (text[:72] + "...") if len(text) > 75 else text

        entries.append({
            "id": qid,
            "domain": q_domain,
            "correct_count": c,
            "wrong_count": w,
            "error_rate": round(rate, 1),
            "consecutive_correct": s.get("consecutive_correct", 0),
            "mastered": bool(s.get("mastered")),
            "last_attempt": s.get("last_attempt"),
            "question_preview": preview or "(题目不存在)",
        })

    return _sort_wrong_entries(entries, sort_by)


def get_all_question_stats(
    bank_id: str = BANK_NATIVE,
) -> Dict[str, Dict[str, Any]]:
    """获取所有题目的累计统计（用于构建错题本）"""
    progress = load_progress()
    section = _get_bank_section(progress, bank_id)
    return section.get("question_stats", {}).copy()


def get_wrong_question_ids(
    sort_by: str = "error_rate",
    domain: Optional[str] = None,
    include_mastered: bool = False,
    bank_id: str = BANK_NATIVE,
) -> List[str]:
    """
    返回错题 ID 列表（默认排除已掌握题目）。

    sort_by: error_rate | wrong_count | last_wrong
    """
    return [
        e["id"]
        for e in get_wrong_book_entries(
            sort_by, domain, include_mastered, bank_id=bank_id
        )
    ]


def count_mastered_wrong_questions(
    bank_id: str = BANK_NATIVE,
) -> int:
    """统计已标为掌握、但仍保留历史错题记录的题目数"""
    return sum(
        1
        for raw in get_all_question_stats(bank_id=bank_id).values()
        if _normalize_question_stat(raw).get("wrong_count", 0) > 0
        and _normalize_question_stat(raw).get("mastered")
    )


def get_accuracy_trend(
    bank_id: str = BANK_NATIVE,
) -> Dict[str, Any]:
    """
    返回最近 10 次会话的正确率趋势统计。
    包含：最近一次、平均值、最高、最低、趋势方向（简单判断）。
    """
    sessions = get_recent_sessions(10, bank_id=bank_id)
    if not sessions:
        return {
            "count": 0,
            "latest": None,
            "avg": None,
            "max": None,
            "min": None,
            "trend": "no_data"
        }

    accuracies = [s["accuracy"] for s in sessions if "accuracy" in s]

    avg = sum(accuracies) / len(accuracies) if accuracies else None
    latest = accuracies[0] if accuracies else None
    max_a = max(accuracies) if accuracies else None
    min_a = min(accuracies) if accuracies else None

    trend = "stable"
    if len(accuracies) >= 3:
        # 简单趋势：最近 3 次平均 vs 前 3 次（如果有）
        recent3 = sum(accuracies[:3]) / min(3, len(accuracies))
        older = accuracies[3:6]
        if older:
            older_avg = sum(older) / len(older)
            if recent3 - older_avg > 5:
                trend = "improving"
            elif older_avg - recent3 > 5:
                trend = "declining"

    return {
        "count": len(sessions),
        "latest": latest,
        "avg": round(avg, 1) if avg is not None else None,
        "max": max_a,
        "min": min_a,
        "trend": trend,
        "sessions": sessions
    }


def clear_all_progress() -> bool:
    """清空所有进度（慎用，主要用于调试）"""
    try:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
        return True
    except Exception:
        return False


def get_practice_font_scale(
    bank_id: str = BANK_NATIVE,
) -> float:
    """读取练习模式用户字体缩放（默认 1.0）。"""
    try:
        section = _get_bank_section(load_progress(), bank_id)
        raw = section.get("preferences", {}).get("practice_font_scale", 1.0)
        return float(raw)
    except (TypeError, ValueError):
        return 1.0


def set_practice_font_scale(
    scale: float,
    bank_id: str = BANK_NATIVE,
) -> bool:
    """保存练习模式用户字体缩放。"""
    data = load_progress()
    section = _get_bank_section(data, bank_id)
    prefs = section.setdefault("preferences", {})
    prefs["practice_font_scale"] = round(float(scale), 2)
    return save_progress(data)


def get_progress_file_path() -> Path:
    """返回进度文件完整路径，便于用户定位"""
    return PROGRESS_FILE


# 便捷调试入口
if __name__ == "__main__":
    print("Progress module self-test")
    print("Progress file location:", get_progress_file_path())
    p = load_progress()
    print("Current sessions:", len(p.get("sessions", [])))
    print("Tracked questions:", len(p.get("question_stats", {})))
    print("Wrong question count:", len(get_wrong_question_ids()))
    trend = get_accuracy_trend()
    print("Accuracy trend:", trend)