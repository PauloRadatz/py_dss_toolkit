# -*- coding: utf-8 -*-
"""
Compare runtime of export-based vs loop-based nodal voltage extraction.

Uses the 1_3PAS_1 feeder and times:
  - voltage_ln_nodes      (dss.export.voltages_ln)
  - voltage_ln_nodes_loop (per-bus Python loop)
  - voltage_ll_nodes      (dss.export.voltages_ll)
  - voltage_ll_nodes_loop (per-bus Python loop)

Requires the OpenDSS C++ backend (ExportV in OpenDSSC.dll).
"""

from __future__ import annotations

import os
import pathlib
import statistics
import time

import pandas as pd
import py_dss_interface
from py_dss_toolkit import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath(
    "feeders", "1_3PAS_1", "Master__202312598_1_3PAS_1_------1-----.dss"
)

WARMUP = 2
REPEATS = 5


def _time_call(label: str, fn, repeats: int = REPEATS) -> tuple[float, object]:
    for _ in range(WARMUP):
        fn()

    samples = []
    result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = fn()
        samples.append(time.perf_counter() - t0)

    mean_s = statistics.mean(samples)
    print(f"  {label:<28}  mean={mean_s:.4f}s  min={min(samples):.4f}s  max={max(samples):.4f}s")
    return mean_s, result


def _report_frame_diff(
    fast: tuple[pd.DataFrame, pd.DataFrame],
    loop: tuple[pd.DataFrame, pd.DataFrame],
    name: str,
) -> None:
    fast_mag, fast_ang = fast
    loop_mag, loop_ang = loop

    shared_cols = sorted(set(fast_mag.columns) & set(loop_mag.columns))
    if not shared_cols:
        print(f"  {name}: no shared columns to compare")
        return

    fast_mag_s = fast_mag[shared_cols]
    loop_mag_s = loop_mag[shared_cols]
    fast_ang_s = fast_ang[shared_cols]
    loop_ang_s = loop_ang[shared_cols]

    mag_diff = (fast_mag_s - loop_mag_s).abs()
    ang_diff = (fast_ang_s - loop_ang_s).abs()
    max_mag = mag_diff.max().max()
    max_ang = ang_diff.max().max()

    extra_loop = sorted(set(loop_mag.columns) - set(fast_mag.columns))
    extra_fast = sorted(set(fast_mag.columns) - set(loop_mag.columns))

    print(f"  {name}: shapes export={fast_mag.shape} loop={loop_mag.shape}")
    if extra_loop or extra_fast:
        if extra_loop:
            print(f"    loop-only columns: {extra_loop[:8]}{'...' if len(extra_loop) > 8 else ''}")
        if extra_fast:
            print(f"    export-only columns: {extra_fast[:8]}{'...' if len(extra_fast) > 8 else ''}")

    try:
        pd.testing.assert_frame_equal(fast_mag_s, loop_mag_s, rtol=1e-5, atol=1e-8, check_exact=False)
        pd.testing.assert_frame_equal(fast_ang_s, loop_ang_s, rtol=1e-5, atol=1e-8, check_exact=False)
        print(f"  {name}: shared columns match (rtol=1e-5)")
    except AssertionError:
        print(f"  {name}: max |diff| on shared columns — mag={max_mag:.3e} pu, ang={max_ang:.3e} deg")


def main() -> None:
    if not dss_file.is_file():
        raise FileNotFoundError(f"DSS file not found: {dss_file.resolve()}")

    dss = py_dss_interface.DSS(windows_version="cpp")
    dss_tools.update_dss(dss)
    dss.text(f"compile [{dss_file.resolve()}]")
    dss_tools.simulation.solve_snapshot()

    num_buses = dss.circuit.num_buses
    print(f"Feeder: {dss_file.name}")
    print(f"Buses:  {num_buses}")
    print(f"Warmup: {WARMUP}  Repeats: {REPEATS}\n")

    results = dss_tools.results

    print("Line-to-neutral (LN)")
    t_ln_export, ln_export = _time_call("voltage_ln_nodes (export)", lambda: results.voltage_ln_nodes)
    t_ln_loop, ln_loop = _time_call("voltage_ln_nodes_loop", lambda: results.voltage_ln_nodes_loop)
    _report_frame_diff(ln_export, ln_loop, "LN")
    print(f"  speedup (loop/export): {t_ln_loop / t_ln_export:.2f}x\n")

    print("Line-to-line (LL)")
    t_ll_export, ll_export = _time_call("voltage_ll_nodes (export)", lambda: results.voltage_ll_nodes)
    t_ll_loop, ll_loop = _time_call("voltage_ll_nodes_loop", lambda: results.voltage_ll_nodes_loop)
    _report_frame_diff(ll_export, ll_loop, "LL")
    print(f"  speedup (loop/export): {t_ll_loop / t_ll_export:.2f}x\n")

    print("Summary")
    print(f"  LN export: {t_ln_export:.4f}s   LN loop: {t_ln_loop:.4f}s   ({t_ln_loop / t_ln_export:.2f}x faster with export)")
    print(f"  LL export: {t_ll_export:.4f}s   LL loop: {t_ll_loop:.4f}s   ({t_ll_loop / t_ll_export:.2f}x faster with export)")


if __name__ == "__main__":
    main()
