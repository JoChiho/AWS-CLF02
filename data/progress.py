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

# 进度文件位置（开发模式：项目根；打包后：exe 同级目录）
PROGRESS_FILE = get_app_root() / "user_data.json"

# 连续答对次数达到此值后自动标为「已掌握」
MASTER_STREAK_REQUIRED = 2


def _now_iso() -> str:
    """返回当前时间的 ISO 格式字符串"""
    return datetime.now().isoformat(timespec="seconds")


def _default_progress() -> Dict[str, Any]:
    """返回一个全新的进度数据结构"""
    return {
        "version": 1,
        "last_updated": _now_iso(),
        "sessions": [],           # 最近 10 次会话，最新在前
        "question_stats": {},     # qid -> 累计统计 + consecutive_correct + mastered
    }


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

        # 简单版本兼容与字段兜底
        if "version" not in data:
            data["version"] = 1
        if "sessions" not in data:
            data["sessions"] = []
        if "question_stats" not in data:
            data["question_stats"] = {}
        if "last_updated" not in data:
            data["last_updated"] = _now_iso()

        return data
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
        # 保证 sessions 只保留最近 10 次（最新在前）
        if len(data.get("sessions", [])) > 10:
            data["sessions"] = data["sessions"][:10]

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
    answered: Optional[int] = None
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

    # 新会话插到最前面
    progress.setdefault("sessions", []).insert(0, session)

    # 裁剪到最近 10 次
    progress["sessions"] = progress["sessions"][:10]

    save_progress(progress)
    return session


def update_question_stat(
    qid: str,
    is_correct: bool,
    user_answer: List[str]
) -> None:
    """
    更新某道题的累计统计（每次用户提交答案并判定正误后调用）。
    """
    if not qid:
        return

    progress = load_progress()
    stats = progress.setdefault("question_stats", {})

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


def get_recent_sessions(limit: int = 10) -> List[Dict[str, Any]]:
    """获取最近 N 次会话（默认 10），最新在前"""
    progress = load_progress()
    sessions = progress.get("sessions", [])
    return sessions[:limit]


def get_question_stats(qid: str) -> Optional[Dict[str, Any]]:
    """获取某题的累计统计"""
    progress = load_progress()
    raw = progress.get("question_stats", {}).get(qid)
    return _normalize_question_stat(raw) if raw else None


def set_question_mastered(qid: str, mastered: bool = True) -> bool:
    """手动标记/取消「已掌握」"""
    if not qid:
        return False

    progress = load_progress()
    stats = progress.setdefault("question_stats", {})
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
) -> List[Dict[str, Any]]:
    """
    返回错题本条目（含统计与题目摘要），支持领域筛选与是否包含已掌握题目。
    """
    from data import get_question_by_id

    stats = get_all_question_stats()
    entries: List[Dict[str, Any]] = []

    for qid, raw in stats.items():
        s = _normalize_question_stat(raw)
        if s.get("wrong_count", 0) <= 0:
            continue
        if not include_mastered and s.get("mastered"):
            continue

        q = get_question_by_id(qid)
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


def get_all_question_stats() -> Dict[str, Dict[str, Any]]:
    """获取所有题目的累计统计（用于构建错题本）"""
    progress = load_progress()
    return progress.get("question_stats", {}).copy()


def get_wrong_question_ids(
    sort_by: str = "error_rate",
    domain: Optional[str] = None,
    include_mastered: bool = False,
) -> List[str]:
    """
    返回错题 ID 列表（默认排除已掌握题目）。

    sort_by: error_rate | wrong_count | last_wrong
    """
    return [
        e["id"]
        for e in get_wrong_book_entries(sort_by, domain, include_mastered)
    ]


def count_mastered_wrong_questions() -> int:
    """统计已标为掌握、但仍保留历史错题记录的题目数"""
    return sum(
        1
        for raw in get_all_question_stats().values()
        if _normalize_question_stat(raw).get("wrong_count", 0) > 0
        and _normalize_question_stat(raw).get("mastered")
    )


def get_accuracy_trend() -> Dict[str, Any]:
    """
    返回最近 10 次会话的正确率趋势统计。
    包含：最近一次、平均值、最高、最低、趋势方向（简单判断）。
    """
    sessions = get_recent_sessions(10)
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