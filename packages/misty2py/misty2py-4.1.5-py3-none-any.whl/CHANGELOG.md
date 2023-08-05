# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 4.1.4 - 15-06-2021

### Fixed

- a build import in `misty2py.basic_skills.expression`

## 4.1.3 - 15-06-2021

### Added

- project directory to `.env.example`
- unit tests with 86% coverage

## 4.1.2 - 15-06-2021

### Added

- `misty2py.basic_skills` with useful basic skills: `cancel_skills`, `expression`, `free_memory`, `movement` and `speak`
- added several utility functions to `misty2py.utils`, including `misty2py.utils.status` to track the execution status of skills and path and message manipulating functions

### Changed

- fixed missing type hinting
- black formatting

## 4.1.1 - 01-06-2021

### Added

- additional unit tests for the `utils.utils` sub-package
- `pytest-cov` for measuring the test coverage

### Changed

- `README.md` now contains clearer instructions on running the tests and obtaining the test coverage report

## 4.1.0 - 19-05-2021

### Changed

- `misty2py.utils.env_loader` now contains optional parameter `env_path` for custom path to the environmental values

### Added

- a pytest for custom `env_path` for `env_loader`

## 4.0.0 - 19-05-2021

### Removed

- the sub-package `skills` -> this will become a separate package due to different dependencies which basic `misty2py` does not use
- the dependencies that are no longer needed
- documentation concerning `skills` sub-package
- `misty2py.utils.status` module removed as it is only used in the `skills` subpackage

## 3.0.2 - 19-05-2021

### Added

- new skills `remote_control`, `explore` and `face_recognition`
- new utility module `status` to track the execution status of a script

### Changed

- renamed `misty2py/skills/greeting.py` to `misty2py/skills/hey_misty.py`

## 3.0.1 - 11-05-2021

### Changed

- fixed style mistakes in documentation

## 3.0.0 - 11-05-2021

### Added

- `skills/template.py` - a template for developing a skill with misty2py
- `skills/greeting.py` - a skill of Misty reacting to the *"Hey Misty"* keyphrase
- `skills/free_memory.py` - a skill that removes non-system audio, video, image and recording files from Misty's memory
- `misty2py.utils` sub-package - various utility functions, some of which were used before in `misty2py.utils` module

### Changed

- changed the architecture of the entire package to be easier to understand and use:
  - moved `misty2py.utils` module to `misty2py.utils.utils`
  - added a sub-package `misty2py.skills`
- updated pytests to match changes in architecture

## 2.0.1 - 05-05-2021

### Added

- `skills` folder for example skills
- `skills/battery_printer.py` as an example skill involving an event emitter
- `skills/listening_expression.py`
- `skills/angry_expression.py`

### Changed

- automatically generated event names now contain the event type

### Fixed

- `construct_transition_dict` raised TypeError when attempting to compare str to int; fix: explicitly casting str to int

## 2.0.0 - 04-05-2021

### Added

- data shortcuts for system images
- `MistyEventHandler` class
- `event_emitter` in `MistyEvent` and `MistyEventHandler`

### Changed

- documentation of data shortcuts in `README.md` to include added data shortcuts
- refinement the event-related architecture to be clearer
- documentation of event-related changes in `README.md`

## 1.0.0 - 10-03-2021

### Added

- Support for custom defined action and information keywords.
- Support for custom defined data shortcuts.
- Unit tests to test the added features.
- Support for all currently available Misty API endpoints for GET, POST and DELETE methods.
- Event types support.

### Changed

- `Misty.perform_action()` now takes one optional argument `data` instead of three optional arguments `dict`, `string` and `data_method`.
- Several functions now return keyword `"status"` instead of `"result"`.
- README to reflect support for custom definitions and event types.
- README to include documentation of supported keywords and shortcuts.
- Renamed `tests\test_unit.py` to `tests\test_base.py` to reflect on purposes of the tests.

### Note

This release was wrongly tagged as it is not downstream compatible and was published without documentation by mistake.

## 0.0.1 - 21-02-2021

### Added

- This CHANGELOG to track changes.
- README with basic information.
- The package misty2py itself supporting:
  - `api/led` endpoint under the keyword `led`,
  - `api/blink/settings` endpoint under the keyword `blink_settings`,
  - the keyword `led_off` for a json dictionary with values 0 for red, green and blue.

---

## Yanked 0.0.2 - 10-03-2021

### Added

- Support for custom defined action and information keywords.
- Support for custom defined data shortcuts.
- Unit tests to test the added features.
- Support for all currently available Misty API endpoints for GET, POST and DELETE methods.
- Event types support.

### Changed

- `Misty.perform_action()` now takes one optional argument `data` instead of three optional arguments `dict`, `string` and `data_method`.
- Several functions now return keyword `"status"` instead of `"result"`.
- README to reflect support for custom definitions and event types.
- README to include documentation of supported supported keywords and shortcuts.
- Renamed `tests\test_unit.py` to `tests\test_base.py` to reflect on purposes of the tests.

### Note

This release was wrongly tagged as it is not downstream compatible and was published without documentation by mistake.