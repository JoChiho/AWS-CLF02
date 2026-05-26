# -*- coding: utf-8 -*-
"""
AWS CLF-C02 认证考试刷题系统

入口文件（Entry Point）

默认行为：
    python main.py          → 启动图形界面（推荐）
    python main.py --cli    → 启动命令行版本（保留兼容）

所有题库数据统一存放在 data/ 目录，便于维护。
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="AWS CLF-C02 刷题系统")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="强制使用命令行（CLI）模式"
    )
    args = parser.parse_args()

    if args.cli:
        # ==================== 命令行模式 ====================
        print("🚀 正在启动命令行版本...")
        try:
            from core.engine import run_single_round, review_wrong_questions
        except ImportError as e:
            print("命令行模块加载失败：", e)
            return

        while True:
            result = run_single_round()
            if result.get("wrong_questions"):
                review_wrong_questions(result["wrong_questions"])

            again = input("\n是否再来一轮？(y/n)：").strip().lower()
            if again != "y":
                print("\n👋 感谢使用！祝你考试顺利！")
                break
            print("\n" + "=" * 70 + "\n新一轮开始！\n")
    else:
        # ==================== 图形界面模式（默认） ====================
        try:
            from gui.app import launch_gui
            launch_gui()
        except ImportError:
            print("未检测到图形界面依赖，请先执行以下命令安装：")
            print("    pip install customtkinter")
            print("\n安装完成后再次运行：python main.py 即可启动图形界面。")
        except Exception as e:
            print("图形界面启动失败：", e)
            print("如需使用命令行版本，请执行：python main.py --cli")


if __name__ == "__main__":
    main()