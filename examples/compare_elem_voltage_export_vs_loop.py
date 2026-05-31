# -*- coding: utf-8 -*-
"""
Compare runtime of element voltage extraction via three paths:

  1. In-memory export  — ``dss.export.elem_voltages`` (ExportV mode 2)
  2. File export       — ``dss.text("export elemvoltages <path>")`` + read/parse
  3. Python loop       — ``voltages_elements_loop`` (per-element CktElement API)

Also breaks down in-memory and file paths into fetch / parse / DataFrame steps.

Requires the OpenDSS C++ backend (ExportV in OpenDSSC.dll).
"""

from __future__ import annotations

import os
import pathlib
import statistics
import tempfile
import time
from typing import Tuple

import pandas as pd
import py_dss_interface
from py_dss_toolkit import dss_tools
from py_dss_toolkit.results.SnapShot.snapshot_utils import create_terminal_list
from py_dss_toolkit.results.SnapShot.voltages_element_utils import _loop_element_names

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
    print(f"  {label:<36}  mean={mean_s:.4f}s  min={min(samples):.4f}s  max={max(samples):.4f}s")
    return mean_s, result


def _records_to_dataframes(
    vmags_records: dict,
    vangs_records: dict,
    elements: list,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    vmags_df = pd.DataFrame.from_dict(vmags_records, orient="index")
    vmags_df = vmags_df.reindex(elements)
    vangs_df = pd.DataFrame.from_dict(vangs_records, orient="index")
    vangs_df = vangs_df.reindex(elements)
    return vmags_df, vangs_df


def _parse_inmemory_csv(csv: str, dss: py_dss_interface.DSS) -> Tuple[dict, dict, list]:
    """Parse enhanced in-memory CSV (Node/V/Ang/Vpu blocks)."""
    lines = csv.splitlines()
    parsed_vmags = dict()
    parsed_vangs = dict()

    for line in lines[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        element = parts[0].replace('"', "").lower()
        num_terminals = int(parts[1])
        num_conductors = int(parts[2])
        nvalues = num_terminals * num_conductors

        nodes = list()
        vpus = list()
        vangs = list()
        k = 3
        for _ in range(nvalues):
            if k + 3 >= len(parts):
                break
            nodes.append(int(parts[k]))
            vangs.append(float(parts[k + 2]))
            vpus.append(float(parts[k + 3]))
            k += 4

        terminal_list = create_terminal_list(nodes, num_terminals)
        parsed_vmags[element] = {
            col: vpus[order] for order, col in enumerate(terminal_list)
        }
        parsed_vangs[element] = {
            col: vangs[order] for order, col in enumerate(terminal_list)
        }

    elements = _loop_element_names(dss)
    vmags_records = {el: parsed_vmags[el] for el in elements if el in parsed_vmags}
    vangs_records = {el: parsed_vangs[el] for el in elements if el in parsed_vangs}
    return vmags_records, vangs_records, elements


def _element_kv_meta(dss: py_dss_interface.DSS) -> dict:
    """Per-element terminal labels and kV-base divisors (same rules as the loop path)."""
    meta = dict()

    is_there_pd = dss.circuit.pd_element_first()
    while is_there_pd:
        element = dss.cktelement.name.lower()
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors
        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        nvalues = num_terminals * num_conductors

        bus1 = dss.cktelement.bus_names[0].split(".")[0].lower()
        bus2 = dss.cktelement.bus_names[1].split(".")[0].lower()
        dss.circuit.set_active_bus(bus1)
        kv_base1 = dss.bus.kv_base * 1000.0
        dss.circuit.set_active_bus(bus2)
        kv_base2 = dss.bus.kv_base * 1000.0

        kv_factors = list()
        half = int(nvalues / 2)
        for i in range(nvalues):
            kv_factors.append(kv_base1 if i < half else kv_base2)

        meta[element] = (nodes, kv_factors)
        if not dss.circuit.pd_element_next():
            is_there_pd = False

    is_there_pc = dss.circuit.pc_element_first()
    while is_there_pc:
        element = dss.cktelement.name.lower()
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors
        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        nvalues = num_terminals * num_conductors

        bus1 = dss.cktelement.bus_names[0].split(".")[0].lower()
        dss.circuit.set_active_bus(bus1)
        kv_base1 = dss.bus.kv_base * 1000.0
        kv_factors = [kv_base1] * nvalues

        meta[element] = (nodes, kv_factors)
        if not dss.circuit.pc_element_next():
            is_there_pc = False

    return meta


def _parse_file_export_text(
    text: str,
    dss: py_dss_interface.DSS,
    kv_meta: dict | None = None,
) -> Tuple[dict, dict, list]:
    """Parse file ``export elemvoltages`` CSV (V/Ang pairs, lower precision)."""
    if kv_meta is None:
        kv_meta = _element_kv_meta(dss)

    lines = text.splitlines()
    parsed_vmags = dict()
    parsed_vangs = dict()

    for line in lines[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        element = parts[0].replace('"', "").lower()
        num_terminals = int(parts[1])
        num_conductors = int(parts[2])
        nvalues = num_terminals * num_conductors

        vmags = list()
        vangs = list()
        k = 3
        for _ in range(nvalues):
            if k + 1 >= len(parts):
                break
            vmags.append(float(parts[k]))
            vangs.append(float(parts[k + 1]))
            k += 2

        if element not in kv_meta:
            continue
        terminal_list, kv_factors = kv_meta[element]
        vpus = [vmags[i] / kv_factors[i] for i in range(len(vmags))]

        parsed_vmags[element] = {
            col: vpus[order] for order, col in enumerate(terminal_list)
        }
        parsed_vangs[element] = {
            col: vangs[order] for order, col in enumerate(terminal_list)
        }

    elements = _loop_element_names(dss)
    vmags_records = {el: parsed_vmags[el] for el in elements if el in parsed_vmags}
    vangs_records = {el: parsed_vangs[el] for el in elements if el in parsed_vangs}
    return vmags_records, vangs_records, elements


def _report_frame_diff(
    fast: tuple[pd.DataFrame, pd.DataFrame],
    loop: tuple[pd.DataFrame, pd.DataFrame],
    name: str,
    rtol: float = 1e-5,
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

    print(f"  {name}: shapes test={fast_mag.shape} loop={loop_mag.shape}")
    try:
        pd.testing.assert_frame_equal(
            fast_mag_s, loop_mag_s, rtol=rtol, atol=1e-8, check_exact=False
        )
        pd.testing.assert_frame_equal(
            fast_ang_s, loop_ang_s, rtol=rtol, atol=1e-8, check_exact=False
        )
        print(f"  {name}: shared columns match (rtol={rtol:g})")
    except AssertionError:
        print(
            f"  {name}: max |diff| on shared columns — "
            f"mag={max_mag:.3e} pu, ang={max_ang:.3e} deg"
        )


def _print_csv_sample(dss: py_dss_interface.DSS, max_lines: int = 3) -> None:
    csv = dss.export.elem_voltages
    lines = csv.splitlines()
    print(f"\nIn-memory export sample (Node/V/Ang/Vpu, first {max_lines} data rows):")
    for line in lines[: max_lines + 1]:
        print(f"  {line[:120]}{'...' if len(line) > 120 else ''}")


def main() -> None:
    if not dss_file.is_file():
        raise FileNotFoundError(f"DSS file not found: {dss_file.resolve()}")

    dss = py_dss_interface.DSS(windows_version="cpp")
    dss_tools.update_dss(dss)
    dss.text(f"compile [{dss_file.resolve()}]")
    dss_tools.simulation.solve_snapshot()

    results = dss_tools.results
    num_elements = len(results.voltages_elements[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = pathlib.Path(tmpdir) / "elem_voltages.csv"

        print(f"Feeder: {dss_file.name}")
        print(f"Elements (PD+PC): {num_elements}")
        print(f"Warmup: {WARMUP}  Repeats: {REPEATS}")

        _print_csv_sample(dss)

        # --- In-memory export breakdown ---
        print("\nIn-memory export breakdown")
        holder = {"csv": "", "records": None, "file_text": ""}

        t_fetch, holder["csv"] = _time_call(
            "1) dss.export.elem_voltages",
            lambda: dss.export.elem_voltages,
        )
        t_parse, holder["records"] = _time_call(
            "2) parse CSV + element order",
            lambda: _parse_inmemory_csv(holder["csv"], dss),
        )
        t_df, inmem_dfs = _time_call(
            "3) records -> DataFrames",
            lambda: _records_to_dataframes(*holder["records"]),
        )
        t_inmem_full = t_fetch + t_parse + t_df
        print(f"  {'sum (1+2+3)':<36}  {t_inmem_full:.4f}s")

        # --- File export breakdown ---
        print("\nFile export breakdown (dss.text + read + parse)")
        kv_meta = _element_kv_meta(dss)

        def _export_file() -> pathlib.Path:
            dss.text(f"export elemvoltages {file_path.resolve()}")
            return file_path

        t_file_write, _ = _time_call(
            "1) dss.text export elemvoltages",
            _export_file,
        )
        t_file_read, holder["file_text"] = _time_call(
            "2) read file from disk",
            lambda: file_path.read_text(encoding="utf-8"),
        )
        t_file_parse, file_records = _time_call(
            "3) parse file + kVBase -> pu",
            lambda: _parse_file_export_text(holder["file_text"], dss, kv_meta),
        )
        t_file_df, file_dfs = _time_call(
            "4) records -> DataFrames",
            lambda: _records_to_dataframes(*file_records),
        )
        t_file_full = t_file_write + t_file_read + t_file_parse + t_file_df
        print(f"  {'sum (1+2+3+4)':<36}  {t_file_full:.4f}s")

        file_sample = holder["file_text"].splitlines()[:4]
        print("\nFile export sample (V/Ang only, lower precision):")
        for line in file_sample:
            print(f"  {line[:120]}{'...' if len(line) > 120 else ''}")

        # --- End-to-end comparison ---
        print("\nEnd-to-end comparison (toolkit API)")
        t_toolkit_export, toolkit_export_dfs = _time_call(
            "voltages_elements (toolkit)",
            lambda: results.voltages_elements,
        )
        t_loop, loop_dfs = _time_call(
            "voltages_elements_loop",
            lambda: results.voltages_elements_loop,
        )

        def _file_pipeline() -> Tuple[pd.DataFrame, pd.DataFrame]:
            dss.text(f"export elemvoltages {file_path.resolve()}")
            text = file_path.read_text(encoding="utf-8")
            rec = _parse_file_export_text(text, dss, kv_meta)
            return _records_to_dataframes(*rec)

        t_file_pipeline, _ = _time_call(
            "file export pipeline (full)",
            _file_pipeline,
        )

        _report_frame_diff(inmem_dfs, loop_dfs, "In-memory vs loop")
        _report_frame_diff(file_dfs, loop_dfs, "File vs loop", rtol=1e-4)

        print("\nSummary")
        print(f"  In-memory fetch+parse+df : {t_inmem_full:.4f}s")
        print(f"    fetch only             : {t_fetch:.4f}s  ({100 * t_fetch / t_inmem_full:.0f}%)")
        print(f"    parse only             : {t_parse:.4f}s  ({100 * t_parse / t_inmem_full:.0f}%)")
        print(f"    DataFrame only         : {t_df:.4f}s  ({100 * t_df / t_inmem_full:.0f}%)")
        print(f"  File write+read+parse+df : {t_file_full:.4f}s")
        print(f"    OpenDSS write only     : {t_file_write:.4f}s  ({100 * t_file_write / t_file_full:.0f}%)")
        print(f"    disk read only         : {t_file_read:.4f}s  ({100 * t_file_read / t_file_full:.0f}%)")
        print(f"    parse + kVBase only    : {t_file_parse:.4f}s  ({100 * t_file_parse / t_file_full:.0f}%)")
        print(f"    DataFrame only         : {t_file_df:.4f}s  ({100 * t_file_df / t_file_full:.0f}%)")
        print(f"  Toolkit export           : {t_toolkit_export:.4f}s")
        print(f"  File pipeline (full)     : {t_file_pipeline:.4f}s")
        print(f"  Loop                     : {t_loop:.4f}s")


if __name__ == "__main__":
    main()
