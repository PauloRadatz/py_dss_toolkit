import gc
import os
import pathlib
import subprocess
import sys

import pytest

import py_dss_interface

from py_dss_toolkit import CreateStudy, dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file_13bus = pathlib.Path(script_path).joinpath("cases", "13bus", "IEEE13Nodeckt.dss")

_subprocess_failures = 0


def _should_run_individually(config=None):
    """
    On Linux, py-dss-interface (OpenDSS C++) can segfault when running
    multiple tests in the same process. Run each test in a subprocess.
    """
    if os.environ.get("_PY_DSS_TOOLKIT_IN_SUBPROCESS", "").lower() == "true":
        return False
    if "--run-together" in sys.argv:
        return False
    if os.environ.get("PY_DSS_TOOLKIT_RUN_TOGETHER", "").lower() == "true":
        return False
    if config and getattr(config.option, "run_together", False):
        return False
    return sys.platform == "linux"


_RUN_INDIVIDUALLY = _should_run_individually()


@pytest.fixture(scope="function")
def snapshot_study_13bus():
    study = CreateStudy.snapshot("My Study", dss_file=dss_file_13bus)

    return study

@pytest.fixture(scope="function")
def timeseries_study_13bus():

    study = CreateStudy.timeseries("My Study", dss_file=dss_file_13bus)

    return study

@pytest.fixture(scope="function")
def dss_tools_13bus():
    dss = py_dss_interface.DSS(windows_version="cpp")
    dss_tools.update_dss(dss)
    dss_tools.configuration.compile_dss(dss_file_13bus)

    return dss


def pytest_runtest_protocol(item, nextitem):
    """
    On Linux, run each test in a subprocess to prevent OpenDSS C++ segfaults.
    """
    if getattr(item.config.option, "collectonly", False):
        return None

    if not _should_run_individually(item.config):
        return None

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    test_nodeid = item.nodeid
    rel_path = os.path.relpath(str(item.fspath), project_root).replace("\\", "/")
    if "::" in test_nodeid:
        parts = test_nodeid.split("::", 1)
        test_nodeid = f"{rel_path}::{parts[1]}"
    else:
        test_nodeid = rel_path

    env = os.environ.copy()
    env["_PY_DSS_TOOLKIT_IN_SUBPROCESS"] = "true"

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        test_nodeid,
        "-v",
        "--tb=short",
        "--no-header",
        "--no-summary",
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )

        global _subprocess_failures
        if result.returncode != 0:
            _subprocess_failures += 1

        sys.stdout.write(result.stdout or "")
        if result.stderr:
            sys.stderr.write(result.stderr)
        sys.stdout.flush()
        sys.stderr.flush()

        gc.collect()
        return True
    except subprocess.TimeoutExpired:
        _subprocess_failures += 1
        return True
    except Exception:
        return None


def pytest_sessionfinish(session, exitstatus):
    if _RUN_INDIVIDUALLY and _subprocess_failures > 0:
        session.exitstatus = 1
