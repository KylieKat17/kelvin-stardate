# test/conftest.py
# Because I hate the regular verbose terminal display

from collections import defaultdict
from pathlib import Path

import pytest

TEST_FILE_DESCRIPTIONS = {
    "test_core.py": "TESTING MAIN CONVERSION LOGIC",
    "test_validators_errors.py": "TESTING VALIDATION & ERROR CODES",
    "test_prompts_control_errors.py": "TESTING CLI CONTROL FLOW (HELP / QUIT / EMPTY)",
    "test_error_registry_complete.py": "TESTING FOR UNREGITERED ERROR CODES"
}

# ============================================================
# GLOBAL STATE
# ============================================================

_RESULTS = defaultdict(list)


# ============================================================
# CUSTOM CLI FLAG
# ============================================================

def pytest_addoption(parser):
    parser.addoption(
        "--pretty",
        action="store_true",
        default=False,
        help="Show grouped, aligned test summary by file."
    )


# ============================================================
# OUTPUT SUPPRESSION (ONLY WHEN --pretty IS USED)
# ============================================================

def pytest_configure(config):
    """
    Suppress default pytest progress output when using --pretty.
    """
    if config.getoption("--pretty"):
        config.option.verbose = 0
        config.option.quiet = 1


def pytest_report_teststatus(report, config):
    """
    Hide per-test progress symbols (dots / percentages).
    """
    if config.getoption("--pretty") and report.when == "call":
        return "", "", ""


# ============================================================
# TEST RESULT COLLECTION
# ============================================================

def pytest_runtest_logreport(report):
    """
    Capture per-test results (call phase only).
    """
    # Defensive: some plugins can emit lists
    if isinstance(report, list):
        for r in report:
            pytest_runtest_logreport(r)
        return

    if report.when != "call":
        return

    file = report.nodeid.split("::")[0]
    test = report.nodeid.split("::")[1]

    if report.failed:
        status = "FAILED"
    elif report.skipped:
        status = "SKIPPED"
    else:
        status = "PASSED"

    _RESULTS[file].append((test, status))


def describe_test_file(path: str) -> str:
    name = Path(path).name
    return TEST_FILE_DESCRIPTIONS.get(
        name,
        "TESTING UNSPECIFIED COMPONENT"
    )


# ============================================================
# CUSTOM KELVIN SUMMARY OUTPUT
# ============================================================

def pytest_sessionfinish(session, exitstatus):
    """
    Print custom grouped summary at the end (only with --pretty).
    """
    if not session.config.getoption("--pretty"):
        return

    total = sum(len(v) for v in _RESULTS.values())
    if total == 0:
        return

    # Global alignment widths (across all files)
    all_rows = [(name, status) for tests in _RESULTS.values() for (name, status) in tests]
    name_width = max(len(name) for name, _ in all_rows)
    status_width = max(len(status) for _, status in all_rows)

    print("\n\n========== KELVIN TEST SUMMARY ==========\n")

    completed = 0

    # Consistent ordering by file path
    for file_path in sorted(_RESULTS.keys()):
        tests = _RESULTS[file_path]
        header = describe_test_file(file_path)
        
        print(header)
        print(f"({file_path})")

        for name, status in tests:
            completed += 1
            percent = int((completed / total) * 100)

            # Right-aligned, fixed-width like pytest: [  3%], [ 53%], [100%]
            pct_str = f"[{percent:>3}%]"

            print(
                f"  {name.ljust(name_width)}   "
                f"{status.ljust(status_width)}   "
                f"{pct_str}"
            )

        print()
