import time
from lgcs.controller import LandingGearController

def run_for(controller: LandingGearController, seconds: float, tick_s: float = 0.25) -> None:
    steps = int(seconds / tick_s)
    for _ in range(steps):
        controller.update(tick_s)
        time.sleep(tick_s)  # optional: remove if you want it to run instantly

def main():
    controller = LandingGearController(deploy_time_s=2.0, retract_time_s=2.0)

    controller.command_gear_down()
    run_for(controller, seconds=3.0)

    controller.command_gear_up()
    run_for(controller, seconds=3.0)

if __name__ == "__main__":
    main()