# -*- coding: utf-8 -*-
"""应用路径工具回归测试"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from app_paths import get_app_root, get_bundle_root


class TestAppPaths(unittest.TestCase):
    def test_dev_mode_app_root_is_project_root(self):
        root = get_app_root()
        self.assertTrue((root / "main.py").exists())
        self.assertTrue((root / "data").is_dir())

    def test_frozen_mode_app_root_is_exe_parent(self):
        fake_exe = Path("C:/Apps/AWS-CLF-C02-Quiz/AWS-CLF-C02-Quiz.exe")
        with patch.object(sys, "frozen", True, create=True):
            with patch.object(sys, "executable", str(fake_exe)):
                root = get_app_root()
        self.assertEqual(root, fake_exe.parent)

    def test_frozen_bundle_root_uses_meipass(self):
        with patch.object(sys, "frozen", True, create=True):
            with patch.object(sys, "_MEIPASS", "C:/Temp/_MEI123", create=True):
                bundle = get_bundle_root()
        self.assertEqual(bundle, Path("C:/Temp/_MEI123"))


if __name__ == "__main__":
    unittest.main()