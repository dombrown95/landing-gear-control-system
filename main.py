from enum import Enum, auto

class GearState(Enum):
    """Defines the discrete states of the landing gear control system."""
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    TRANSITIONING_UP = auto()
    DOWN_LOCKED = auto()

class LandingGearController:
    def __init__(self):
        """Initialises the gear controller in the UP_LOCKED state."""
        self.state = GearState.UP_LOCKED
    
    def log(self, message):
        """Outputs a status message for the landing gear system state."""
        print(f"[{self.state.name}] {message}")

    def command_gear_down(self):
        """Commands the landing gear system to retract if currently locked down."""
        if self.state == GearState.UP_LOCKED:
            self.state = GearState.TRANSITIONING_DOWN
            self.log("Gear deploying")
            self.state = GearState.DOWN_LOCKED
            self.log("Gear locked down")
        else:
            self.log("Command rejected")

    def command_gear_up(self):
        """Commands the landing gear system to deploy if currently locked up."""
        if self.state == GearState.DOWN_LOCKED:
            self.state = GearState.TRANSITIONING_UP
            self.log("Gear retracting")
            self.state = GearState.UP_LOCKED
            self.log("Gear locked up")
        else:
            self.log("Command rejected")

controller = LandingGearController()
controller.command_gear_down()
controller.command_gear_up()