# -*- coding: utf-8 -*-
"""
Windows 打包脚本：生成 dist/AWS-CLF-C02-Quiz/ 目录分发包。

用法（在项目根目录）：
    python build/build_windows.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "build" / "clf_quiz.spec"
DIST_DIR = ROOT / "dist" / "AWS-CLF-C02-Quiz"
USER_DATA_NAME = "user_data.json"
USER_DATA_BACKUP = ROOT / ".user_data.dist.bak.json"


def _backup_user_progress() -> Path | None:
    """COLLECT 会删掉整个 dist 目录，必须先把做题记录拷到 dist 外。"""
    sources = [
        DIST_DIR / USER_DATA_NAME,
        ROOT / USER_DATA_NAME,
    ]
    existing = [p for p in sources if p.exists() and p.stat().st_size > 2]
    if not existing:
        print("未发现已有 user_data.json，打包后将是空白进度。")
        return None

    def _stamp(path: Path) -> str:
        try:
            import json

            data = json.loads(path.read_text(encoding="utf-8"))
            return str(data.get("last_updated") or "")
        except Exception:
            return ""

    chosen = max(existing, key=lambda p: (_stamp(p), p.stat().st_mtime))
    shutil.copy2(chosen, USER_DATA_BACKUP)
    print(f"已备份做题记录: {chosen} -> {USER_DATA_BACKUP}")
    return USER_DATA_BACKUP


def _restore_user_progress(backup: Path | None) -> None:
    if backup is None or not backup.exists():
        return
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    dest = DIST_DIR / USER_DATA_NAME
    shutil.copy2(backup, dest)
    root_copy = ROOT / USER_DATA_NAME
    if root_copy.resolve() != backup.resolve():
        shutil.copy2(backup, root_copy)
    print(f"已还原做题记录: {backup} -> {dest}")


def main() -> int:
    if shutil.which("pyinstaller") is None:
        print("未找到 pyinstaller，请先执行：")
        print("    pip install -r requirements-dev.txt")
        return 1

    print("=" * 60)
    print("AWS CLF-C02 Quiz — PyInstaller build")
    print("=" * 60)
    print(f"Project root: {ROOT}")
    print(f"Spec file:    {SPEC}")
    print()

    backup = _backup_user_progress()

    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(SPEC), "--noconfirm"],
        cwd=str(ROOT),
        check=False,
    )
    if result.returncode != 0:
        _restore_user_progress(backup)
        print("\nBuild FAILED.")
        print("若 dist 被占用，请先关闭 AWS-CLF-C02-Quiz.exe 后重试。")
        print("做题记录已保留在 .user_data.dist.bak.json，不会因打包失败丢失。")
        return result.returncode

    exe = DIST_DIR / "AWS-CLF-C02-Quiz.exe"
    if not exe.exists():
        _restore_user_progress(backup)
        print(f"\nBuild finished but executable not found: {exe}")
        return 1

    _restore_user_progress(backup)

    print("\nBuild OK.")
    print(f"  Output: {DIST_DIR}")
    print(f"  Run:    {exe}")
    print("\n提示：将 dist/AWS-CLF-C02-Quiz/ 整个文件夹复制到目标机器即可运行；")
    print("      user_data.json（错题本/做题记录）已保留在 exe 同级目录。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())