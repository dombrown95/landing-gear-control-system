"""
Landing Gear Control System (LGCS) Prototype
Author: Dom Brown
Date: 07-01-2026

Requirement IDs:
FR1: The system shall simulate landing gear deployment behaviour.
FR2: The system shall simulate landing gear retraction behaviour.
FR3: The system shall manage discrete gear states including: UP_LOCKED, TRANSITIONING_DOWN, DOWN_LOCKED, TRANSITIONING_UP.
FR4: The system shall perform deterministic, time-based state transitions between gear states.
FR5: The system shall allow configuration of deploy and retract durations.
FR6: The system shall execute the simulation using discrete time steps.
FR7: The system shall record state transitions and invalid command handling via logging.

Note: These requirements define the scope of the LGCS prototype and do not represent a complete or certifiable landing gear control system.

Code Summary:
System-level entry point for the LGCS prototype. This module loads configuration parameters, initialises the landing gear controller and executes a time-stepped simulation demonstrating deploy and retract behaviour.

Change Log:
- 07-01-2026: Initial prototype implementation.
- 14-01-2026: Added gear retract functionality and method docstrings.
- 16-01-2026: Introduced configuration driven timing and simulation loop.
- 21-01-2026: Added automated unit tests and CI pipeline for verification.
- 21-01-2026: Added structured logging to record state transitions and command handling.

"""

import json
import time
from pathlib import Path

from lgcs.controller import LandingGearController
from lgcs.logging_config import setup_logging


DEFAULT_CONFIG = {
    "deploy_time_s": 2.0,
    "retract_time_s": 2.0,
    "tick_s": 0.25,
    "sleep_enabled": False,

    # Logging
    "log_file": "lgcs.log",
    "log_level": "INFO",
    "log_to_console": True,
}


def load_config(path: str = "config.json") -> dict:
    """Loads simulation configuration from JSON, falling back to defaults if missing."""
    config_path = Path(path)

    if not config_path.exists():
        return DEFAULT_CONFIG.copy()

    with config_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    merged = DEFAULT_CONFIG.copy()
    merged.update(data)
    return merged


def run_for(controller: LandingGearController, seconds: float, tick_s: float, sleep_enabled: bool) -> None:
    """Runs the simulation for a fixed duration using a constant tick."""
    if tick_s <= 0:
        raise ValueError("tick_s must be > 0")

    steps = int(seconds / tick_s)
    for _ in range(steps):
        controller.update(tick_s)
        if sleep_enabled:
            time.sleep(tick_s)


def main() -> None:
    config = load_config()

    setup_logging(
        log_file=config["log_file"],
        level=config["log_level"],
        console=config["log_to_console"],
    )

    controller = LandingGearController(
        deploy_time_s = config["deploy_time_s"],
        retract_time_s = config["retract_time_s"],
    )

    controller.command_gear_down()
    run_for(controller, seconds = config["deploy_time_s"] + 1.0, tick_s = config["tick_s"], sleep_enabled = config["sleep_enabled"])

    controller.command_gear_up()
    run_for(controller, seconds = config["retract_time_s"] + 1.0, tick_s = config["tick_s"], sleep_enabled = config["sleep_enabled"])

if __name__ == "__main__":
    main()