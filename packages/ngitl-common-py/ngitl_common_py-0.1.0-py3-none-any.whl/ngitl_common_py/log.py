# Copyright (C) 2023, NG:ITL
import logging
import datetime
import sys
from pathlib import Path
from typing import Optional


EMERGENCY_LOGGING_LOG_FILE_DIRECTORY_PATH = Path.cwd()
EMERGENCY_LOGGING_LOG_LEVEL = "DEBUG"

LOG_FORMAT = "%(asctime)s [%(levelname)s][%(module)s]: %(message)s"

log_file_path: Optional[Path] = None


def init_logging(log_file_directory: Path, component_name: str, logging_level: str):
    global log_file_path
    timestamp = datetime.datetime.now()
    timestamp_prefix = timestamp.strftime("%Y%m%d-%H%M%S")
    log_file_path = log_file_directory / f"{timestamp_prefix}_{component_name}.log"
    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file_path)
    logging.basicConfig(
        handlers=[stdout_handler, file_handler],
        level=logging_level,
        format=LOG_FORMAT,
    )
    logging.info("Logging initialized!")


def init_emergency_logging(component_name: str):
    global log_file_path
    log_file_path = EMERGENCY_LOGGING_LOG_FILE_DIRECTORY_PATH / f"{component_name}_emergency.log"
    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file_path)
    logging.basicConfig(
        handlers=[stdout_handler, file_handler],
        level=EMERGENCY_LOGGING_LOG_LEVEL,
        format=LOG_FORMAT,
    )
    logging.error("Emergency log initialized!")
