# Copyright (C) 2023, NG:ITL
import os
import tempfile
import unittest
from pathlib import Path

from ngitl_common_py import autostart


class WindowsAutostartTest(unittest.TestCase):

    def setUp(self) -> None:
        tmp_dir = tempfile.mkdtemp()
        autostart_dir = os.path.join(tmp_dir, 'autostart')
        os.mkdir(autostart_dir)
        self.test_link_file = Path(os.path.join(autostart_dir, 'test.lnk'))
        self.test_target_file = Path(__file__)

    def enable_autostart(self):
        autostart.activate_autostart(self.test_target_file, self.test_link_file)

    def disable_autostart(self):
        autostart.deactivate_autostart(self.test_link_file)

    def test_AutostartEnabled_IsAutostartIsEnabled_ReturnTrue(self):
        self.enable_autostart()
        self.assertTrue(autostart.is_autostart_enabled(self.test_link_file))

    def test_AutostartDisabled_IsAutostartIsEnabled_ReturnFalse(self):
        self.disable_autostart()
        self.assertFalse(autostart.is_autostart_enabled(self.test_link_file))

    def test_AutostartEnabled_IsLinkFileExisting_FileExisting(self):
        self.enable_autostart()
        self.assertTrue(os.path.isfile(self.test_link_file))

    def test_AutostartDisabled_IsLinkFileExisting_FileNotExisting(self):
        self.disable_autostart()
        self.assertFalse(os.path.isfile(self.test_link_file))
