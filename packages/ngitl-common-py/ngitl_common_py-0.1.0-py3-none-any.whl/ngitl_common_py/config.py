# Copyright (C) 2023, NG:ITL
import json
import os
from pathlib import Path
from typing import Optional, Any

SEARCH_PATHS = [Path.cwd(), Path.cwd().parent, Path.home()]

AVAILABLE_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

__config = {}


class ConfigEntryError(Exception):
    def __init__(self, msg: str, *args):
        super().__init__(args)
        self.msg = msg

    def __str__(self):
        return self.msg


class ConfigEntryInvalidLogLevelError(ConfigEntryError):
    def __init__(self, log_level: str, *args):
        super().__init__(
            f"Invalid log level requested: {log_level}, available log level: {AVAILABLE_LOG_LEVELS}",
            args,
        )


class ConfigEntryNotADirectoryError(ConfigEntryError):
    def __init__(self, directory_path: Path, *args):
        super().__init__(
            f'Invalid config entry, directory "{directory_path}" is not a valid directory!',
            args,
        )


class ConfigEntryFileNotFoundError(ConfigEntryError):
    def __init__(self, file_path: Path, *args):
        super().__init__(f'Invalid config entry, file "{file_path}" is not a valid file!', args)


def find_config_file(config_filename: str) -> Optional[Path]:
    for search_path in SEARCH_PATHS:
        filepath_to_check = search_path / config_filename
        if filepath_to_check.exists():
            return filepath_to_check
    return None


def read_config(config_file_path: Path):
    with open(config_file_path) as json_data_file:
        global __config
        __config = json.load(json_data_file)


def write_config_to_file(config_file_path: Path):
    with open(config_file_path, "w") as output_file:
        json.dump(__config, output_file, indent=4)


def validate_directory_path(directory_path: Path, required_permission: int):
    if not os.path.isdir(directory_path):
        raise ConfigEntryNotADirectoryError(directory_path)
    elif not os.access(directory_path, required_permission):
        raise PermissionError(directory_path)


def validate_file_path(file_path: Path):
    if not os.path.isfile(file_path):
        raise ConfigEntryFileNotFoundError(file_path)


def validate_log_level(log_level_str: str):
    if log_level_str not in AVAILABLE_LOG_LEVELS:
        raise ConfigEntryInvalidLogLevelError(log_level_str)


def get_config() -> dict:
    global __config
    return __config


def get_config_param(name: str) -> Any:
    global __config
    return __config[name]


def set_config_param(name: str, value: Any) -> None:
    global __config
    __config[name] = value
