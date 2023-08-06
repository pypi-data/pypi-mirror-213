# Copyright (C) 2023, NG:ITL
import os.path
import subprocess
from pathlib import Path


NOTEPAD_EXECUTABLE_PATH = Path(r"C:\Windows\System32\notepad.exe")
NOTEPADPP_EXECUTABLE_PATH = Path(r"C:\Program Files (x86)\Notepad++\notepad++.exe")


def _is_notepadpp_available() -> bool:
    return os.path.isfile(NOTEPADPP_EXECUTABLE_PATH)


def _open_file_with_notepadpp(filepath: Path) -> None:
    subprocess.Popen(
        [NOTEPADPP_EXECUTABLE_PATH, "-nosession", filepath],
        creationflags=subprocess.DETACHED_PROCESS,
    )


def _open_file_with_notepad(filepath: Path) -> None:
    subprocess.Popen([NOTEPAD_EXECUTABLE_PATH, filepath], creationflags=subprocess.DETACHED_PROCESS)


def open_file_viewer(filepath: Path) -> None:
    if _is_notepadpp_available():
        _open_file_with_notepadpp(filepath)
    else:
        _open_file_with_notepad(filepath)
