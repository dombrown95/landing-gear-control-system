"""
LGCS Logging Configuration
Author: Dom Brown
Date: 21-01-2026

Requirement IDs:
FR7  - The system shall record state transitions and invalid command handling via logging.

Code Summary:
Provides centralised logging configuration for the LGCS prototype.
Configures log formatting, log levels and file output to support
observable system behaviour and QA evidence generation.

Change Log:
- 21-01-2026: Initial logging configuration added to support QA evidence.
"""

import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: str = "lgcs.log",
    level: str = "INFO",
    console: bool = True,
) -> None:
    """Configures application logging to file using a consistent format."""
    level_value = getattr(logging, level.upper(), logging.INFO)

    # Ensures the parent folder exists if a path is provided
    log_path = Path(log_file)
    if log_path.parent and str(log_path.parent) != ".":
        log_path.parent.mkdir(parents=True, exist_ok=True)

    handlers: list[logging.Handler] = [logging.FileHandler(log_path, encoding="utf-8")]
    if console:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=level_value,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
        force=True,
    )