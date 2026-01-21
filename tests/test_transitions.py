"""
LGCS Verification Tests

Author: Dom Brown
Date: 21-01-2026

Requirement IDs:
FR1: Simulate landing gear deployment behaviour.
FR2: Simulate landing gear retraction behaviour.
FR3: Manage discrete gear states.
FR4: Perform deterministic, time-based state transitions.

Verification Summary:
This test suite provides automated verification that the Landing Gear Controller
transitions between expected gear states within the specified simulated time
intervals and correctly rejects invalid command sequences.

Change Log:
- 21-01-2026: Initial automated verification tests for gear state transitions.
"""

from lgcs.controller import LandingGearController, GearState

def test_deploy_reaches_down_locked_after_deploy_time():
    controller = LandingGearController(deploy_time_s=1.0, retract_time_s=1.0)

    controller.command_gear_down()
    assert controller.state == GearState.TRANSITIONING_DOWN

    # Advance simulated time just past deploy_time_s
    controller.update(1.01)
    assert controller.state == GearState.DOWN_LOCKED


def test_retract_reaches_up_locked_after_retract_time():
    controller = LandingGearController(deploy_time_s=1.0, retract_time_s=1.0)

    controller.command_gear_down()
    controller.update(1.01)
    assert controller.state == GearState.DOWN_LOCKED

    controller.command_gear_up()
    assert controller.state == GearState.TRANSITIONING_UP

    controller.update(1.01)
    assert controller.state == GearState.UP_LOCKED


def test_rejects_invalid_command_from_wrong_state():
    controller = LandingGearController()

    # Gear can't retract when already up
    controller.command_gear_up()
    assert controller.state == GearState.UP_LOCKED