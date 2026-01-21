# Landing Gear Control System (LGCS) Prototype

This repository contains a Python-based prototype of a Landing Gear Control System (LGCS),
developed to demonstrate state-based control logic, configuration management and
quality assurance (QA) practices.

## Overview
The prototype simulates landing gear deployment and retraction using a discrete
state machine with time-based transitions. It is currently a prototype
and does not represent a certified aircraft system.

## Key Features
- State-machine-based landing gear controller.
- Time-stepped simulation with configurable timing.
- Structured logging of state transitions and command handling.
- Automated unit tests with continuous integration (GitHub Actions).

## Configuration Management
- Baseline tagged as `baseline-v1.0`
- Post-baseline improvements released as:
  - `v1.1`: Automated unit testing and CI
  - `v1.2`: Structured logging for traceability

## Running the Prototype
```
python main.py
```

## Running Tests
```
python -m pytest
```