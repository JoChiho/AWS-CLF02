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

    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(SPEC), "--noconfirm"],
        cwd=str(ROOT),
        check=False,
    )
    if result.returncode != 0:
        print("\nBuild FAILED.")
        return result.returncode

    exe = DIST_DIR / "AWS-CLF-C02-Quiz.exe"
    if not exe.exists():
        print(f"\nBuild finished but executable not found: {exe}")
        return 1

    print("\nBuild OK.")
    print(f"  Output: {DIST_DIR}")
    print(f"  Run:    {exe}")
    print("\n提示：将 dist/AWS-CLF-C02-Quiz/ 整个文件夹复制到目标机器即可运行；")
    print("      user_data.json 会保存在 exe 同级目录。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())