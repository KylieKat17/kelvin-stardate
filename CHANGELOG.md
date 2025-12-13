# CHANGELOG
*(Temporal Corrections, Feature Drift, Regret Mitigation)*

All notable changes to this project are documented here.

This project does **not** follow strict semantic versioning in the academic sense,
but versions *do* reflect meaningful changes in behavior, output, or assumptions.

Dates are Earth dates. Stardates would be irresponsible here.

---

## [Unreleased]

Things that are planned, partially implemented, or looming ominously.
See `TODO.md` for details.

- Error code display unification across CLI and internal exceptions
- Packaging work (`pyproject.toml`, pip installability)
- Canon date references (likely YAML-backed)
- Output formatting improvements (tables, styling cleanup)
- CHANGELOG exists now, so future entries will be cleaner

---

## [1.4] – 2025-12-13
### CLI Maturity Pass / Multi-Mode Stabilization

This is the first version where the CLI feels *intentional* instead of “good enough.”

### Added
- Interactive CLI with guided menus and help loop
- Subcommand-based CLI (`earth-to`, `sd-to`)
- Flag-based CLI usage (`--from-earth`, `--from-sd`)
- Multiple conversion modes:
  - `no_leap` (Orci-style ordinal year)
  - `gregorian` (Earth leap-year calendar)
  - `astronomical` (fractional year model)
  - `all` (side-by-side comparison)
- Automatic stardate type detection (Kelvin vs astronomical)
- Color-coded output by mode (via `colorama`)
- Error codes for common failure cases
- Month parsing by name or number
- Leap-day validation

### Changed
- Output formatting standardized so:
  - inputs are always echoed
  - results are grouped and labeled
  - human-readable dates are shown alongside ISO dates
- CLI behavior now prefers recovery and redisplay over hard exits

### Known Issues
- Error code styling is not fully consistent across all CLI paths
- Color definitions are still global instead of centralized
- Output formatting logic is duplicated in a few places

---

## [1.3] – 2025-12-06
### Astronomical Model Introduction

### Added
- Astronomical stardate conversion:
  - continuous year model (365.2425 days)
  - explicit separation from Kelvin-style ordinal logic
- Explicit astronomical conversion functions in the core library

### Changed
- Conversion logic refactored to reduce coupling between models
- CLI updated to support selecting astronomical mode directly

---

## [1.2] – 2025-11-28
### Gregorian Reality Check Fixed

### Fixed
- Gregorian leap-year handling
- Leap-day validation for Earth → stardate conversion

### Changed
- Internal date validation logic hardened
- CLI error handling improved for invalid calendar dates

---

## [1.1] – 2025-11-24
### Error Codes & Defensive Programming Era

### Added
- Custom exception classes
- Structured error codes (`E001`, `E002`, etc.)
- Clear separation between:
  - user input errors
  - internal conversion errors
- Help-triggered re-prompt flow instead of immediate exit

### Changed
- CLI behavior now prefers explanation over failure
- Invalid input no longer silently produces nonsense

---

## [1.0] – 2025-11-12
### Initial Version

### Added
- Core Kelvin Timeline stardate <--> Earth date conversion
- Orci-style ordinal year model (365-day year, no leap years)
- Minimal CLI for manual conversion
- Basic library API

### Notes
- This version worked, but was fragile
- Assumptions were implicit
- Output formatting was inconsistent
- The project immediately outgrew this version

---

## Versioning Notes

- Versions reflect *behavioral* stability, not marketing milestones
- Minor version bumps usually indicate:
  - new conversion models
  - CLI UX changes
  - assumption changes
- Patch-level changes are tracked implicitly unless they matter

---

## Final Note

This changelog exists so Future Me does not have to reconstruct
intent from commit diffs and memory.

Time is complicated enough without that.
