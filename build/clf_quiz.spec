# -*- mode: python ; coding: utf-8 -*-
"""
AWS CLF-C02 刷题系统 Windows GUI 打包配置。

用法（在项目根目录）：
    pyinstaller build/clf_quiz.spec
"""
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

ROOT = Path(SPECPATH).resolve().parent

block_cipher = None

ctk_datas = collect_data_files("customtkinter")
ctk_hidden = collect_submodules("customtkinter")

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=ctk_datas,
    hiddenimports=[
        *ctk_hidden,
        "data",
        "data.single_choice",
        "data.multi_choice",
        "data.mock_exam",
        "data.progress",
        "core",
        "core.engine",
        "core.parser",
        "app_paths",
        "gui",
        "gui.app",
        "gui.menu",
        "gui.quiz_view",
        "gui.stats_view",
        "gui.mock_exam",
        "gui.wrong_book_view",
        "gui.constants",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AWS-CLF-C02-Quiz",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="AWS-CLF-C02-Quiz",
)