"""
Landing Gear Control System (LGCS)
Landing Gear Controller Module

Author: Dom Brown
Date: 07-01-2026

Requirement IDs:
FR1: Simulate landing gear deployment behaviour.
FR2: Simulate landing gear retraction behaviour.
FR3: Manage discrete gear states.
FR4: Perform deterministic, time-based state transitions.
FR7: Reject and log invalid command sequences.

Module Summary:
Implements the core state machine for the LGCS prototype, including
command handling, state transitions and time-based behaviour used
by the simulation and verification tests.

Change Log:
- 07-01-2026: Initial controller implementation with basic state handling.
- 14-01-2026: Added retract behaviour and state validation.
- 16-01-2026: Introduced time-based transitions using elapsed time.
- 21-01-2026: Updated logging hooks to support structured logging (FR7).
"""

from enum import Enum, auto
import logging

logger = logging.getLogger("lgcs.controller")

class GearState(Enum):
    """Defines the discrete states of the landing gear control system."""
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    TRANSITIONING_UP = auto()
    DOWN_LOCKED = auto()

class LandingGearController:
    def __init__(self, deploy_time_s: float = 2.0, retract_time_s: float = 2.0):
        """Initialises the gear controller and transition timings."""
        self.state = GearState.UP_LOCKED

        # Configuration for deploy and retract times
        self.deploy_time_s = float(deploy_time_s)
        self.retract_time_s = float(retract_time_s)

        # Internal simulation state
        self._transition_elapsed_s = 0.0

    def log(self, message: str) -> None:
        """Logs a status message for the landing gear system state."""
        logger.info("[%s] %s", self.state.name, message)

    def _start_transition(self, new_state: GearState, action_msg: str) -> None:
        """Starts a transition state and resets the transition timer."""
        self.state = new_state
        self._transition_elapsed_s = 0.0
        self.log(action_msg)

    def update(self, dt_s: float) -> None:
        """Advances the simulation by dt_s seconds and completes transitions when due."""
        if dt_s < 0:
            raise ValueError("dt_s must be non-negative")

        if self.state in (GearState.TRANSITIONING_DOWN, GearState.TRANSITIONING_UP):
            self._transition_elapsed_s += dt_s

            if self.state == GearState.TRANSITIONING_DOWN:
                if self._transition_elapsed_s >= self.deploy_time_s:
                    self.state = GearState.DOWN_LOCKED
                    self.log("Gear locked down")

            elif self.state == GearState.TRANSITIONING_UP:
                if self._transition_elapsed_s >= self.retract_time_s:
                    self.state = GearState.UP_LOCKED
                    self.log("Gear locked up")

    def command_gear_down(self) -> None:
        """Begins gear deployment if currently UP_LOCKED."""
        if self.state == GearState.UP_LOCKED:
            self._start_transition(GearState.TRANSITIONING_DOWN, "Gear deploying")
        else:
            self.log("Command rejected")

    def command_gear_up(self) -> None:
        """Begins gear retraction if currently DOWN_LOCKED."""
        if self.state == GearState.DOWN_LOCKED:
            self._start_transition(GearState.TRANSITIONING_UP, "Gear retracting")
        else:
            self.log("Command rejected")