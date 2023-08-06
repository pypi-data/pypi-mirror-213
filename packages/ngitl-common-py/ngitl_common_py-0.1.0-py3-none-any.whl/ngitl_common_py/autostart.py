# Copyright (C) 2023, NG:ITL
import os
import sys
import logging

from pathlib import Path

DEFAULT_TARGET_PATH = Path(sys.executable)
DEFAULT_SHORTCUT_PATH = (
    Path.home() / f"AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/{Path(sys.executable).stem}.lnk"
)


try:
    import win32com.client

    def activate_autostart(
        target_path: Path = DEFAULT_TARGET_PATH,
        shortcut_path: Path = DEFAULT_SHORTCUT_PATH,
    ) -> None:
        logging.debug(
            "activate autostart requested: target_path = %s, shortcut_path = %s",
            target_path,
            shortcut_path,
        )
        if not is_autostart_enabled(shortcut_path):
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target_path)
            shortcut.WorkingDirectory = str(target_path).rsplit("\\", 1)[0]
            shortcut.save()
        else:
            logging.warning("Autostart already enabled")

    def deactivate_autostart(shortcut_path: Path = DEFAULT_SHORTCUT_PATH) -> None:
        logging.debug("deactivate autostart requested: shortcut_path = %s", shortcut_path)
        if is_autostart_enabled(shortcut_path):
            os.remove(shortcut_path)
        else:
            logging.warning("Autostart already disabled")

    def is_autostart_enabled(shortcut_path: Path = DEFAULT_SHORTCUT_PATH) -> bool:
        return os.path.exists(shortcut_path)

except ModuleNotFoundError:

    def activate_autostart(
        target_path: Path = DEFAULT_TARGET_PATH,
        shortcut_path: Path = DEFAULT_SHORTCUT_PATH,
    ) -> None:
        logging.warning("Unable to activate autostart due to missing pywin32 package.")

    def deactivate_autostart(shortcut_path: Path = DEFAULT_SHORTCUT_PATH) -> None:
        logging.warning("Unable to deactivate autostart due to missing pywin32 package.")

    def is_autostart_enabled(shortcut_path: Path = DEFAULT_SHORTCUT_PATH) -> bool:
        return False
