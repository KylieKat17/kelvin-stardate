# test/conftest.py
# Because I hate the regular verbose terminal display

from collections import defaultdict
from pathlib import Path

import pytest

_RESULTS = defaultdict(list)


def pytest_addoption(parser):
    parser.addoption(
        "--pretty",
        action="store_true",
        default=False,
        help="Show grouped, aligned test summary by file."
    )


def pytest_runtest_logreport(report):
    """
    Capture per-test results (call phase only).
    """
    # Some plugins/edge cases can send a list; handle it defensively.
    if isinstance(report, list):
        for r in report:
            pytest_runtest_logreport(r)
        return

    if report.when != "call":
        return

    file = Path(report.nodeid.split("::")[0]).as_posix()
    test = report.nodeid.split("::")[1]

    if report.failed:
        status = "FAILED"
    elif report.skipped:
        status = "SKIPPED"
    else:
        status = "PASSED"

    _RESULTS[file].append((test, status))


def pytest_sessionfinish(session, exitstatus):
    """
    Print custom summary only if --pretty is enabled.
    """
    if not session.config.getoption("--pretty"):
        return

    total = sum(len(v) for v in _RESULTS.values())
    if total == 0:
        return

    print("\n\n========== CUSTOM TEST SUMMARY ==========\n")

    completed = 0

    for file, tests in _RESULTS.items():
        print(file)

        max_name = max(len(name) for name, _ in tests)
        max_status = max(len(status) for _, status in tests)

        for name, status in tests:
            completed += 1
            percent = int((completed / total) * 100)

            print(
                f"  {name.ljust(max_name)}   "
                f"{status.ljust(max_status)}   "
                f"{percent:>3}%"
            )

        print()
