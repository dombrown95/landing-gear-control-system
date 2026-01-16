import json
import time
from pathlib import Path

from lgcs.controller import LandingGearController


DEFAULT_CONFIG = {
    "deploy_time_s": 2.0,
    "retract_time_s": 2.0,
    "tick_s": 0.25,
    "sleep_enabled": False,
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