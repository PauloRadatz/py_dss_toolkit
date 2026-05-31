# -*- coding: utf-8 -*-
"""
Fair benchmark mirroring the Useall OpenDSS C# pattern (UtilOpenDss_pr.cs).

Useall slow path (DadosDosElementosOpenDSS):
  For each Line segment → SetActiveElement + SetActiveBus, then read
  voltages, pu, currents, powers, and phase losses via the COM/API loop.

Useall fast path (ExportarDadosCalculadosOpenDss + LerExport*):
  Five bulk native exports per snapshot, then read/parse CSV from disk:
    export voltages | export currents | Export Elempowers | export losses | Export NodeOrder

This script compares three Python equivalents on the 1_3PAS_1 feeder:

  1. useall_loop          — per-line API calls (like ServCalculoOpenDss_pr.cs)
  2. useall_file_export   — five file exports + read + parse
  3. useall_hybrid        — in-memory ``dss.export.voltages_ln`` + four file exports

In-memory ExportV modes available today: voltages_ln (0), voltages_ll (1),
elem_voltages (2). Currents, elempowers, losses, and NodeOrder still require
file export (or per-element API).

Requires OpenDSS C++ backend (``DSS(windows_version="cpp")``).
"""

from __future__ import annotations

import math
import os
import pathlib
import statistics
import tempfile
import time
from dataclasses import dataclass, field
from typing import Callable

import py_dss_interface
from py_dss_toolkit import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath(
    "feeders", "1_3PAS_1", "Master__202312598_1_3PAS_1_------1-----.dss"
)

WARMUP = 2
REPEATS = 5

EXPORT_COMMANDS = (
    ("export voltages", "voltages", "EXP_VOLTAGES.CSV"),
    ("export currents", "currents", "EXP_CURRENTS.CSV"),
    ("Export Elempowers", "powers", "EXP_ElemPowers.CSV"),
    ("export losses", "losses", "EXP_LOSSES.CSV"),
    ("Export NodeOrder", "nodeorder", "EXP_NodeOrder.CSV"),
)


@dataclass
class LineSnapshot:
    """Per-line quantities collected the way Useall's loop path does."""

    name: str
    bus: str
    nodes: list
    v_ln_kv: list = field(default_factory=list)
    pu: list = field(default_factory=list)
    i_mag: list = field(default_factory=list)
    p_kw: list = field(default_factory=list)
    q_kvar: list = field(default_factory=list)
    loss_kw: list = field(default_factory=list)


def _time_call(label: str, fn: Callable, repeats: int = REPEATS) -> tuple[float, object]:
    for _ in range(WARMUP):
        fn()

    samples = []
    result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = fn()
        samples.append(time.perf_counter() - t0)

    mean_s = statistics.mean(samples)
    print(
        f"  {label:<40}  mean={mean_s:.4f}s  "
        f"min={min(samples):.4f}s  max={max(samples):.4f}s"
    )
    return mean_s, result


def _phase_map(values: list, nodes: list, stride: int = 2) -> list:
    """Map conductor/bus values onto phases 1..3 (index 0 unused), like Useall."""
    out = [0.0, 0.0, 0.0, 0.0]
    if not nodes or not values:
        return out
    n = min(len(nodes), len(values) // stride if stride > 1 else len(values))
    for i in range(n):
        phase = int(nodes[i])
        if 1 <= phase <= 3:
            if stride == 2:
                re, im = values[2 * i], values[2 * i + 1]
                out[phase] = math.hypot(re, im) if stride == 2 and im is not None else float(re)
            else:
                out[phase] = float(values[i])
    return out


def _phase_map_pq(powers: list, nodes: list) -> tuple[list, list]:
    p_out = [0.0, 0.0, 0.0, 0.0]
    q_out = [0.0, 0.0, 0.0, 0.0]
    if not nodes or len(powers) < 2 * len(nodes):
        return p_out, q_out
    for i, phase in enumerate(nodes):
        if 1 <= int(phase) <= 3:
            p_out[int(phase)] = float(powers[2 * i])
            q_out[int(phase)] = float(powers[2 * i + 1])
    return p_out, q_out


def collect_useall_loop(dss: py_dss_interface.DSS) -> list[LineSnapshot]:
    """Mirror ServCalculoOpenDss_pr.DadosDosElementosOpenDSS for Line elements."""
    rows: list[LineSnapshot] = []

    for line in dss.lines.names:
        elem = f"line.{line.lower()}"
        dss.circuit.set_active_element(elem)

        bus2 = dss.cktelement.bus_names[1].split(".")[0].lower()
        dss.circuit.set_active_bus(bus2)

        nodes = list(dss.bus.nodes)
        voltages = dss.bus.voltages
        pu = dss.bus.pu_voltages
        currents = dss.cktelement.currents_mag_ang
        powers = dss.cktelement.powers
        phase_losses = dss.cktelement.phase_losses

        i_mag = [
            currents[i]
            for i in range(0, min(len(currents), 2 * len(nodes)), 2)
        ]
        loss_kw = [
            phase_losses[i]
            for i in range(0, min(len(phase_losses), 2 * len(nodes)), 2)
        ]
        p_kw, q_kvar = _phase_map_pq(list(powers), nodes)

        rows.append(
            LineSnapshot(
                name=line.lower(),
                bus=bus2,
                nodes=nodes,
                v_ln_kv=_phase_map(list(voltages), nodes),
                pu=_phase_map(list(pu), nodes),
                i_mag=_phase_map(i_mag, nodes, stride=1),
                p_kw=p_kw,
                q_kvar=q_kvar,
                loss_kw=_phase_map(loss_kw, nodes, stride=1),
            )
        )

    return rows


def _write_exports(dss: py_dss_interface.DSS, out_dir: pathlib.Path) -> dict[str, pathlib.Path]:
    paths: dict[str, pathlib.Path] = {}
    for cmd, key, _default in EXPORT_COMMANDS:
        fp = out_dir / f"{key}.csv"
        dss.text(f"{cmd} {fp.resolve()}")
        paths[key] = fp
    return paths


def _read_exports(paths: dict[str, pathlib.Path]) -> dict[str, str]:
    return {key: fp.read_text(encoding="utf-8") for key, fp in paths.items()}


def _parse_nodeorder(text: str) -> dict[str, list[int]]:
    nodes_by_elem: dict[str, list[int]] = {}
    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        elem = parts[0].replace('"', "").lower()
        nterms = int(parts[1])
        nconds = int(parts[2])
        nvalues = nterms * nconds
        nodes = [int(parts[3 + i]) for i in range(nvalues) if 3 + i < len(parts)]
        nodes_by_elem[elem] = nodes
    return nodes_by_elem


def build_line_bus2_map(dss: py_dss_interface.DSS) -> dict[str, str]:
    """Downstream bus per line (bus2), matching Useall AtivaElemento."""
    mapping: dict[str, str] = {}
    for line in dss.lines.names:
        elem = f"line.{line.lower()}"
        dss.circuit.set_active_element(elem)
        mapping[line.lower()] = dss.cktelement.bus_names[1].split(".")[0].lower()
    return mapping


def _parse_voltages_text(text: str) -> dict[str, dict]:
    """Parse export voltages CSV → {bus: {pu phases, v phases}}."""
    by_bus: dict[str, dict] = {}
    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        bus = parts[0].replace('"', "").split(".")[0].lower()
        pu = [0.0, 0.0, 0.0, 0.0]
        v_kv = [0.0, 0.0, 0.0, 0.0]
        k = 2
        while k + 4 <= len(parts):
            node = int(parts[k])
            if node != 0 and 1 <= node <= 3:
                mag_v = float(parts[k + 1])
                pu[node] = float(parts[k + 3])
                v_kv[node] = mag_v / 1000.0
            k += 4
        by_bus[bus] = {"pu": pu, "v_ln_kv": v_kv}
    return by_bus


def _parse_currents_file(text: str) -> dict[str, list[float]]:
    by_elem: dict[str, list[float]] = {}
    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        elem = parts[0].replace('"', "").lower()
        if not elem.startswith("line."):
            continue
        vals = [float(parts[i]) for i in range(1, len(parts), 2)]
        by_elem[elem.replace("line.", "")] = vals
    return by_elem


def _parse_powers_file(text: str) -> dict[str, tuple[list, list]]:
    by_elem: dict[str, tuple[list, list]] = {}
    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        elem = parts[0].replace('"', "").lower()
        if not elem.startswith("line."):
            continue
        nterms = int(parts[1])
        nconds = int(parts[2])
        nvalues = nterms * nconds
        p_vals, q_vals = [], []
        k = 3
        for _ in range(nvalues):
            if k + 1 >= len(parts):
                break
            p_vals.append(float(parts[k]))
            q_vals.append(float(parts[k + 1]))
            k += 2
        by_elem[elem.replace("line.", "")] = (p_vals, q_vals)
    return by_elem


def _parse_losses_file(text: str) -> dict[str, float]:
    by_elem: dict[str, float] = {}
    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        elem = parts[0].replace('"', "").lower()
        if not elem.startswith("line."):
            continue
        by_elem[elem.replace("line.", "")] = float(parts[1]) / 1000.0
    return by_elem


def _assemble_from_exports(
    texts: dict[str, str],
    line_bus2: dict[str, str],
    voltages_key: str = "voltages",
) -> list[LineSnapshot]:
    """Build line snapshots from exported CSV texts (Useall LerExport* style)."""
    v_by_bus = _parse_voltages_text(texts[voltages_key])
    i_by_line = _parse_currents_file(texts["currents"])
    pq_by_line = _parse_powers_file(texts["powers"])
    loss_by_line = _parse_losses_file(texts["losses"])
    nodes_by_elem = _parse_nodeorder(texts["nodeorder"])

    rows: list[LineSnapshot] = []
    for line_name, i_mag in i_by_line.items():
        elem = f"line.{line_name}"
        nodes = nodes_by_elem.get(elem, [])
        bus = line_bus2.get(line_name, "")
        v_row = v_by_bus.get(bus, {"pu": [0.0] * 4, "v_ln_kv": [0.0] * 4})

        p_vals, q_vals = pq_by_line.get(line_name, ([], []))
        flat_pq = [x for pair in zip(p_vals, q_vals) for x in pair]
        p_kw, q_kvar = _phase_map_pq(flat_pq, nodes) if flat_pq and nodes else (
            [0.0] * 4,
            [0.0] * 4,
        )

        rows.append(
            LineSnapshot(
                name=line_name,
                bus=bus,
                nodes=nodes,
                v_ln_kv=v_row["v_ln_kv"],
                pu=v_row["pu"],
                i_mag=_phase_map(i_mag, nodes, stride=1),
                p_kw=p_kw,
                q_kvar=q_kvar,
                loss_kw=[0.0, 0.0, 0.0, loss_by_line.get(line_name, 0.0)],
            )
        )
    return rows


def collect_useall_file_export(
    dss: py_dss_interface.DSS,
    out_dir: pathlib.Path,
    line_bus2: dict[str, str],
) -> list[LineSnapshot]:
    paths = _write_exports(dss, out_dir)
    texts = _read_exports(paths)
    return _assemble_from_exports(texts, line_bus2)


def collect_useall_hybrid(
    dss: py_dss_interface.DSS,
    out_dir: pathlib.Path,
    line_bus2: dict[str, str],
) -> list[LineSnapshot]:
    texts: dict[str, str] = {"voltages": dss.export.voltages_ln}
    for cmd, key, _ in EXPORT_COMMANDS[1:]:
        fp = out_dir / f"{key}.csv"
        dss.text(f"{cmd} {fp.resolve()}")
        texts[key] = fp.read_text(encoding="utf-8")
    return _assemble_from_exports(texts, line_bus2)


def _report_summary(loop_rows: list[LineSnapshot], fast_rows: list[LineSnapshot], label: str) -> None:
    print(f"  {label}: loop lines={len(loop_rows)}  export lines={len(fast_rows)}")
    common = {r.name for r in loop_rows} & {r.name for r in fast_rows}
    if not common:
        return
    max_pu_diff = 0.0
    max_i_diff = 0.0
    for name in sorted(common)[:200]:
        a = next(r for r in loop_rows if r.name == name)
        b = next(r for r in fast_rows if r.name == name)
        for ph in (1, 2, 3):
            max_pu_diff = max(max_pu_diff, abs(a.pu[ph] - b.pu[ph]))
            max_i_diff = max(max_i_diff, abs(a.i_mag[ph] - b.i_mag[ph]))
    print(f"  {label}: sample max |dpu|={max_pu_diff:.3e}  max |dI|={max_i_diff:.3e} A")


def main() -> None:
    if not dss_file.is_file():
        raise FileNotFoundError(f"DSS file not found: {dss_file.resolve()}")

    dss = py_dss_interface.DSS(windows_version="cpp")
    dss_tools.update_dss(dss)
    dss.text(f"compile [{dss_file.resolve()}]")
    dss_tools.simulation.solve_snapshot()

    num_lines = len(dss.lines.names)
    line_bus2 = build_line_bus2_map(dss)

    print(f"Feeder: {dss_file.name}")
    print(f"Line segments: {num_lines}")
    print(f"Warmup: {WARMUP}  Repeats: {REPEATS}")
    print()
    print("Useall exports per snapshot:")
    for cmd, key, _ in EXPORT_COMMANDS:
        mem = "in-memory (ExportV mode 0)" if key == "voltages" else "file only"
        print(f"  {cmd:<22}  [{mem}]")

    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = pathlib.Path(tmpdir)

        print("\n--- End-to-end (Useall-style) ---")
        t_loop, loop_rows = _time_call(
            "1) Per-line API loop (Useall slow)",
            lambda: collect_useall_loop(dss),
        )
        t_file, file_rows = _time_call(
            "2) Five file exports + parse",
            lambda: collect_useall_file_export(dss, out_dir, line_bus2),
        )
        t_hybrid, hybrid_rows = _time_call(
            "3) Hybrid (in-mem V + 4 files)",
            lambda: collect_useall_hybrid(dss, out_dir, line_bus2),
        )

        _report_summary(loop_rows, file_rows, "Loop vs file")
        _report_summary(loop_rows, hybrid_rows, "Loop vs hybrid")

        print(f"\n  Loop faster than file by:  {t_file / t_loop:.2f}x")
        print(f"  Loop faster than hybrid by: {t_hybrid / t_loop:.2f}x")

        # --- Breakdown: file export path ---
        print("\n--- File export breakdown ---")
        holder: dict = {"texts": {}}

        t_write, paths = _time_call(
            "  OpenDSS write (5 exports)",
            lambda: _write_exports(dss, out_dir),
        )
        t_read, holder["texts"] = _time_call(
            "  Read files from disk",
            lambda: _read_exports(paths),
        )
        t_parse, _ = _time_call(
            "  Parse CSV to LineSnapshot list",
            lambda: _assemble_from_exports(holder["texts"], line_bus2),
        )
        print(f"  {'sum write+read+parse':<40}  {t_write + t_read + t_parse:.4f}s")

        # --- Breakdown: loop API call mix ---
        print("\n--- Per-line loop breakdown (single pass, not timed separately) ---")
        api_counts = {
            "set_active_element": num_lines,
            "set_active_bus": num_lines,
            "bus.voltages + pu_voltages + nodes": num_lines * 3,
            "cktelement.currents_mag_ang + powers + phase_losses": num_lines * 3,
        }
        total_api = sum(api_counts.values())
        for name, count in api_counts.items():
            print(f"  {name:<40}  {count:>5} calls/snapshot")
        print(f"  {'TOTAL ctypes/API calls':<40}  {total_api:>5} calls/snapshot")

        print("\n--- Summary ---")
        print(f"  Per-line loop:     {t_loop:.4f}s  ({total_api} API calls)")
        print(f"  File export:       {t_file:.4f}s  (loop is {t_file / t_loop:.2f}x faster)")
        print(f"  Hybrid:            {t_hybrid:.4f}s  (loop is {t_hybrid / t_loop:.2f}x faster)")
        print(f"    OpenDSS writes:  {t_write:.4f}s  ({100 * t_write / t_file:.0f}% of file path)")
        print(f"    Disk read:       {t_read:.4f}s")
        print(f"    Python parse:    {t_parse:.4f}s")
        print()
        print("Note: Useall C# uses COM (dss_sharp), which is slower per call than Python ctypes.")
        print("      Their speedup vs loop is typically larger than shown here.")
        print("      In-memory ExportV for voltages avoids one file write/read vs pure file path.")


if __name__ == "__main__":
    main()
