# -*- coding: utf-8 -*-
"""
Compare three paths to the same dss_tools DataFrame shapes:

  1. Toolkit loop (baseline)
     - results.voltage_ln_nodes_loop
     - results.powers_elements
     - results.currents_elements
     - results.losses_elements

  2. Useall-style loop (ServCalculoOpenDss DadosDosElementosOpenDSS pattern)
     - AtivaElemento: set_active_element + set_active_bus(bus2)
     - Multiple property reads per iteration (voltages, pu, currents, powers, losses)
     - Assembled into the same DataFrame layouts as toolkit

  3. File export (Useall fast path)
     - export voltages | Export Elempowers | export currents | export losses
     - Export NodeOrder (for powers/currents column mapping)

Requires OpenDSS C++ backend (DSS(windows_version="cpp")).
"""

from __future__ import annotations

import os
import pathlib
import statistics
import tempfile
import time
from typing import Callable, Tuple

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
RTOL = 1e-4
SIMULATE_FULL_USEALL_READS = True

MAIN_EXPORTS = (
    ("export voltages", "voltages"),
    ("Export Elempowers", "powers"),
    ("export currents", "currents"),
    ("export losses", "losses"),
)
NODEORDER_CMD = ("Export NodeOrder", "nodeorder")


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
        f"  {label:<42}  mean={mean_s:.4f}s  "
        f"min={min(samples):.4f}s  max={max(samples):.4f}s"
    )
    return mean_s, result


def _records_to_pair_df(
    mag_records: dict,
    ang_records: dict,
    index: list,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    mag_df = pd.DataFrame.from_dict(mag_records, orient="index").reindex(index)
    ang_df = pd.DataFrame.from_dict(ang_records, orient="index").reindex(index)
    return mag_df, ang_df


def _parse_nodeorder(text: str) -> dict[str, tuple[int, int, list[int]]]:
    """element -> (nterms, nconds, node list in conductor order)."""
    out: dict[str, tuple[int, int, list[int]]] = {}
    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        elem = parts[0].replace('"', "").lower()
        nterms = int(parts[1])
        nconds = int(parts[2])
        nvalues = nterms * nconds
        nodes = [int(parts[3 + i]) for i in range(nvalues) if 3 + i < len(parts)]
        out[elem] = (nterms, nconds, nodes)
    return out


def _parse_voltages_file(text: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    vmags_records = dict()
    vangs_records = dict()
    buses = list()

    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        bus = parts[0].replace('"', "").split(".")[0].lower()
        buses.append(bus)

        vmag_row = dict()
        vang_row = dict()
        k = 2
        while k + 4 <= len(parts):
            node = parts[k]
            if node != "0":
                vmag_row[f"node{int(node)}"] = float(parts[k + 3])
                vang_row[f"node{int(node)}"] = float(parts[k + 2])
            k += 4

        vmags_records[bus] = vmag_row
        vangs_records[bus] = vang_row

    return _records_to_pair_df(vmags_records, vangs_records, buses)


def _parse_elem_pq_file(
    text: str,
    nodeorder: dict[str, tuple[int, int, list[int]]],
    elements: list[str],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    parsed_p = dict()
    parsed_q = dict()

    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        element = parts[0].replace('"', "").lower()
        if element not in nodeorder:
            continue

        nterms = int(parts[1])
        nconds = int(parts[2])
        nvalues = nterms * nconds
        nodes = nodeorder[element][2]
        terminal_list = create_terminal_list(nodes, nterms)

        p_vals = list()
        q_vals = list()
        k = 3
        for _ in range(nvalues):
            if k + 1 >= len(parts):
                break
            p_vals.append(float(parts[k]))
            q_vals.append(float(parts[k + 1]))
            k += 2

        parsed_p[element] = {
            col: p_vals[i] for i, col in enumerate(terminal_list) if i < len(p_vals)
        }
        parsed_q[element] = {
            col: q_vals[i] for i, col in enumerate(terminal_list) if i < len(q_vals)
        }

    p_records = {el: parsed_p[el] for el in elements if el in parsed_p}
    q_records = {el: parsed_q[el] for el in elements if el in parsed_q}
    idx = [el for el in elements if el in p_records]
    return _records_to_pair_df(p_records, q_records, idx)


def _parse_currents_header(header: str) -> tuple[int, int]:
    """Return (max_term, max_cond) from export currents header."""
    max_term = 0
    max_cond = 0
    for col in header.split(","):
        col = col.strip()
        if col.startswith("I") and "_" in col and not col.startswith("Iresid"):
            body = col[1:]
            term_s, cond_s = body.split("_", 1)
            max_term = max(max_term, int(term_s))
            max_cond = max(max_cond, int(cond_s))
    return max_term, max_cond


def _parse_currents_file(
    text: str,
    nodeorder: dict[str, tuple[int, int, list[int]]],
    elements: list[str],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    lines = text.splitlines()
    max_term, max_cond = _parse_currents_header(lines[0])
    cols_per_term = max_cond * 2 + 2

    parsed_i = dict()
    parsed_ang = dict()

    for line in lines[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        element = parts[0].replace('"', "").lower()
        if element not in nodeorder:
            continue

        nterms, nconds, nodes = nodeorder[element]
        terminal_list = create_terminal_list(nodes, nterms)

        imags = list()
        iangs = list()
        for t in range(1, nterms + 1):
            for c in range(1, nconds + 1):
                off = 1 + (t - 1) * cols_per_term + (c - 1) * 2
                if off + 1 < len(parts):
                    imags.append(float(parts[off]))
                    iangs.append(float(parts[off + 1]))

        parsed_i[element] = {
            col: imags[i] for i, col in enumerate(terminal_list) if i < len(imags)
        }
        parsed_ang[element] = {
            col: iangs[i] for i, col in enumerate(terminal_list) if i < len(iangs)
        }

    i_records = {el: parsed_i[el] for el in elements if el in parsed_i}
    ang_records = {el: parsed_ang[el] for el in elements if el in parsed_ang}
    idx = [el for el in elements if el in i_records]
    return _records_to_pair_df(i_records, ang_records, idx)


def _pd_element_names(dss: py_dss_interface.DSS) -> list[str]:
    elements = list()
    is_there_pd = dss.circuit.pd_element_first()
    while is_there_pd:
        elements.append(dss.cktelement.name.lower())
        if not dss.circuit.pd_element_next():
            is_there_pd = False
    return elements


def _parse_losses_file(text: str, pd_elements: list[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """PD-only losses; toolkit uses cktelement.losses in kW/kvar."""
    pd_set = set(pd_elements)
    p_records = dict()
    q_records = dict()

    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        raw = parts[0].replace('"', "")
        if "." in raw:
            element = f"{raw.split('.')[0].lower()}.{raw.split('.', 1)[1].lower()}"
        else:
            element = raw.lower()
        if element not in pd_set:
            continue
        p_records[element] = {"P losses (kW)": float(parts[1]) / 1000.0}
        q_records[element] = {"Q losses (kvar)": float(parts[2]) / 1000.0}

    idx = [el for el in pd_elements if el in p_records]
    p_df = pd.DataFrame.from_dict(p_records, orient="index").reindex(idx)
    q_df = pd.DataFrame.from_dict(q_records, orient="index").reindex(idx)
    return p_df, q_df


def _export_file(dss: py_dss_interface.DSS, out_dir: pathlib.Path, cmd: str, key: str) -> pathlib.Path:
    fp = out_dir / f"{key}.csv"
    dss.text(f"{cmd} {fp.resolve()}")
    return fp


def _ativa_elemento(dss: py_dss_interface.DSS, element: str) -> str:
    """Python port of Useall UtilOpenDss.AtivaElemento (bus2 downstream when available)."""
    dss.circuit.set_active_element(element)
    bus_names = dss.cktelement.bus_names
    if len(bus_names) >= 2:
        bus = bus_names[1].split(".")[0].lower()
    else:
        bus = bus_names[0].split(".")[0].lower()
    dss.circuit.set_active_bus(bus)
    return bus


def _useall_reads_after_activate(dss: py_dss_interface.DSS) -> None:
    """Simulate Useall per-line API chatter (RetornaTensoes/Pu/Corrente/Demanda/Perdas)."""
    if not SIMULATE_FULL_USEALL_READS:
        return
    _ = dss.bus.voltages
    _ = dss.bus.nodes
    _ = dss.bus.pu_voltages
    _ = dss.bus.nodes
    _ = dss.cktelement.currents_mag_ang
    _ = dss.bus.nodes
    _ = dss.cktelement.powers
    _ = dss.bus.nodes
    _ = dss.cktelement.phase_losses
    _ = dss.bus.nodes


def _bus_nodal_from_active_bus(dss: py_dss_interface.DSS) -> tuple[dict, dict]:
    """Nodal pu/angle records from active bus (matches toolkit vmag_angle_pu)."""
    nodes = list(dss.bus.nodes)
    vpu = dss.bus.vmag_angle_pu
    vmag_row = dict()
    vang_row = dict()
    for order, node in enumerate(nodes):
        if 2 * order + 1 < len(vpu):
            vmag_row[f"node{int(node)}"] = float(vpu[2 * order])
            vang_row[f"node{int(node)}"] = float(vpu[2 * order + 1])
    return vmag_row, vang_row


def collect_useall_voltages(dss: py_dss_interface.DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Useall line loop + fill remaining buses for full toolkit index."""
    vmags_records = dict()
    vangs_records = dict()
    seen_buses = set()

    for line in dss.lines.names:
        elem = f"line.{line.lower()}"
        bus = _ativa_elemento(dss, elem)
        _useall_reads_after_activate(dss)
        vmag_row, vang_row = _bus_nodal_from_active_bus(dss)
        vmags_records[bus] = vmag_row
        vangs_records[bus] = vang_row
        seen_buses.add(bus)

    buses = [bus.lower().split(".")[0] for bus in dss.circuit.buses_names]
    for bus in buses:
        if bus in seen_buses:
            continue
        dss.circuit.set_active_bus(bus)
        num_nodes = dss.bus.num_nodes
        nodes = dss.bus.nodes
        vmags = dss.bus.vmag_angle_pu[: 2 * num_nodes: 2]
        vangs = dss.bus.vmag_angle_pu[1: 2 * num_nodes: 2]
        vmags_records[bus] = {
            f"node{node}": vmags[order] for order, node in enumerate(nodes)
        }
        vangs_records[bus] = {
            f"node{node}": vangs[order] for order, node in enumerate(nodes)
        }

    return _records_to_pair_df(vmags_records, vangs_records, buses)


def collect_useall_powers(
    dss: py_dss_interface.DSS,
    elements: list[str],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    element_nodes = dict()
    element_p = dict()
    element_q = dict()

    for element in elements:
        _ativa_elemento(dss, element)
        _useall_reads_after_activate(dss)
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors
        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        nvalues = 2 * num_terminals * num_conductors
        p = dss.cktelement.powers[:nvalues:2]
        q = dss.cktelement.powers[1:nvalues:2]
        element_nodes[element] = nodes
        element_p[element] = p
        element_q[element] = q

    p_records = {
        el: {col: element_p[el][i] for i, col in enumerate(nodes)}
        for el, nodes in element_nodes.items()
    }
    q_records = {
        el: {col: element_q[el][i] for i, col in enumerate(nodes)}
        for el, nodes in element_nodes.items()
    }
    idx = [el for el in elements if el in p_records]
    return _records_to_pair_df(p_records, q_records, idx)


def collect_useall_currents(
    dss: py_dss_interface.DSS,
    elements: list[str],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    element_nodes = dict()
    element_i = dict()
    element_ang = dict()

    for element in elements:
        _ativa_elemento(dss, element)
        _useall_reads_after_activate(dss)
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors
        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        nvalues = 2 * num_terminals * num_conductors
        cma = dss.cktelement.currents_mag_ang[:nvalues]
        element_nodes[element] = nodes
        element_i[element] = cma[:nvalues:2]
        element_ang[element] = cma[1:nvalues:2]

    i_records = {
        el: {col: element_i[el][i] for i, col in enumerate(nodes)}
        for el, nodes in element_nodes.items()
    }
    ang_records = {
        el: {col: element_ang[el][i] for i, col in enumerate(nodes)}
        for el, nodes in element_nodes.items()
    }
    idx = [el for el in elements if el in i_records]
    return _records_to_pair_df(i_records, ang_records, idx)


def collect_useall_losses(
    dss: py_dss_interface.DSS,
    pd_elements: list[str],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Uses cktelement.losses (toolkit parity; Useall lines use PhaseLosses)."""
    p_records = dict()
    q_records = dict()

    for element in pd_elements:
        _ativa_elemento(dss, element)
        _useall_reads_after_activate(dss)
        losses = dss.cktelement.losses
        p_records[element] = {"P losses (kW)": losses[0] / 1000.0}
        q_records[element] = {"Q losses (kvar)": losses[1] / 1000.0}

    p_df = pd.DataFrame.from_dict(p_records, orient="index").reindex(pd_elements)
    q_df = pd.DataFrame.from_dict(q_records, orient="index").reindex(pd_elements)
    return p_df, q_df


def collect_useall_style_all(
    dss: py_dss_interface.DSS,
    pd_pc_elements: list[str],
    pd_elements: list[str],
) -> tuple:
    return (
        collect_useall_voltages(dss),
        collect_useall_powers(dss, pd_pc_elements),
        collect_useall_currents(dss, pd_pc_elements),
        collect_useall_losses(dss, pd_elements),
    )


def _report_pair_diff(
    file_dfs: Tuple[pd.DataFrame, pd.DataFrame],
    loop_dfs: Tuple[pd.DataFrame, pd.DataFrame],
    name: str,
) -> None:
    f_a, f_b = file_dfs
    l_a, l_b = loop_dfs
    shared_idx = sorted(set(f_a.index) & set(l_a.index))
    shared_cols_a = sorted(set(f_a.columns) & set(l_a.columns))
    shared_cols_b = sorted(set(f_b.columns) & set(l_b.columns))

    print(f"  {name}: file={f_a.shape} loop={l_a.shape} shared rows={len(shared_idx)}")
    if not shared_idx or not shared_cols_a:
        print(f"  {name}: insufficient overlap to compare")
        return

    try:
        pd.testing.assert_frame_equal(
            f_a.loc[shared_idx, shared_cols_a],
            l_a.loc[shared_idx, shared_cols_a],
            rtol=RTOL,
            atol=1e-6,
            check_exact=False,
        )
        pd.testing.assert_frame_equal(
            f_b.loc[shared_idx, shared_cols_b],
            l_b.loc[shared_idx, shared_cols_b],
            rtol=RTOL,
            atol=1e-6,
            check_exact=False,
        )
        print(f"  {name}: match on shared index/columns (rtol={RTOL:g})")
    except AssertionError:
        d1 = (f_a.loc[shared_idx, shared_cols_a] - l_a.loc[shared_idx, shared_cols_a]).abs().max().max()
        d2 = (f_b.loc[shared_idx, shared_cols_b] - l_b.loc[shared_idx, shared_cols_b]).abs().max().max()
        print(f"  {name}: max |diff| frame1={d1:.3e} frame2={d2:.3e}")


def _speedup_label(t_loop: float, t_file: float) -> str:
    if t_file < t_loop:
        return f"file is {t_loop / t_file:.2f}x faster"
    return f"loop is {t_file / t_loop:.2f}x faster"


def _fastest_label(t_toolkit: float, t_useall: float, t_file: float) -> str:
    times = {"toolkit": t_toolkit, "useall": t_useall, "file": t_file}
    winner = min(times, key=times.get)
    best = times[winner]
    others = {k: v for k, v in times.items() if k != winner}
    slowest = max(others.values())
    return f"{winner} ({slowest / best:.2f}x vs slowest)"


def main() -> None:
    if not dss_file.is_file():
        raise FileNotFoundError(f"DSS file not found: {dss_file.resolve()}")

    dss = py_dss_interface.DSS(windows_version="cpp")
    dss_tools.update_dss(dss)
    dss.text(f"compile [{dss_file.resolve()}]")
    dss_tools.simulation.solve_snapshot()

    results = dss_tools.results
    pd_pc_elements = _loop_element_names(dss)
    pd_elements = _pd_element_names(dss)

    print(f"Feeder: {dss_file.name}")
    print(f"PD+PC elements: {len(pd_pc_elements)}")
    print(f"Buses: {dss.circuit.num_buses}")
    print(f"Warmup: {WARMUP}  Repeats: {REPEATS}\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = pathlib.Path(tmpdir)

        # Pre-export NodeOrder once for parsers (not timed in per-metric file runs)
        nodeorder_path = _export_file(dss, out_dir, NODEORDER_CMD[0], NODEORDER_CMD[1])
        nodeorder_text = nodeorder_path.read_text(encoding="utf-8")
        nodeorder = _parse_nodeorder(nodeorder_text)

        timings: dict[str, tuple[float, float, float]] = {}

        # --- LN voltages ---
        print("--- LN voltages ---")
        t_loop, loop_v = _time_call("toolkit: voltage_ln_nodes_loop", lambda: results.voltage_ln_nodes_loop)
        t_useall, useall_v = _time_call(
            "useall: line AtivaElemento + bus reads",
            lambda: collect_useall_voltages(dss),
        )

        def _file_voltages():
            fp = _export_file(dss, out_dir, "export voltages", "voltages_bench")
            text = fp.read_text(encoding="utf-8")
            return _parse_voltages_file(text)

        t_file, file_v = _time_call("file: export voltages + parse", _file_voltages)
        t_write, v_path = _time_call(
            "  breakdown: OpenDSS write",
            lambda: _export_file(dss, out_dir, "export voltages", "voltages_bd"),
        )
        holder = {"text": ""}
        t_read, holder["text"] = _time_call(
            "  breakdown: disk read",
            lambda: v_path.read_text(encoding="utf-8"),
        )
        t_parse, _ = _time_call(
            "  breakdown: parse",
            lambda: _parse_voltages_file(holder["text"]),
        )
        _report_pair_diff(useall_v, loop_v, "Useall vs toolkit LN")
        _report_pair_diff(file_v, loop_v, "File vs toolkit LN")
        print(f"  Fastest: {_fastest_label(t_loop, t_useall, t_file)}\n")
        timings["LN voltages"] = (t_loop, t_useall, t_file)

        # --- Powers ---
        print("--- Powers ---")
        t_loop, loop_p = _time_call("toolkit: powers_elements", lambda: results.powers_elements)
        t_useall, useall_p = _time_call(
            "useall: AtivaElemento + reads",
            lambda: collect_useall_powers(dss, pd_pc_elements),
        )

        def _file_powers():
            fp = _export_file(dss, out_dir, "Export Elempowers", "powers_bench")
            text = fp.read_text(encoding="utf-8")
            return _parse_elem_pq_file(text, nodeorder, pd_pc_elements)

        t_file, file_p = _time_call("file: Export Elempowers + parse", _file_powers)
        _report_pair_diff(useall_p, loop_p, "Useall vs toolkit Powers")
        _report_pair_diff(file_p, loop_p, "File vs toolkit Powers")
        print(f"  Fastest: {_fastest_label(t_loop, t_useall, t_file)}\n")
        timings["Powers"] = (t_loop, t_useall, t_file)

        # --- Currents ---
        print("--- Currents ---")
        t_loop, loop_i = _time_call("toolkit: currents_elements", lambda: results.currents_elements)
        t_useall, useall_i = _time_call(
            "useall: AtivaElemento + reads",
            lambda: collect_useall_currents(dss, pd_pc_elements),
        )

        def _file_currents():
            fp = _export_file(dss, out_dir, "export currents", "currents_bench")
            text = fp.read_text(encoding="utf-8")
            return _parse_currents_file(text, nodeorder, pd_pc_elements)

        t_file, file_i = _time_call("file: export currents + parse", _file_currents)
        _report_pair_diff(useall_i, loop_i, "Useall vs toolkit Currents")
        _report_pair_diff(file_i, loop_i, "File vs toolkit Currents")
        print(f"  Fastest: {_fastest_label(t_loop, t_useall, t_file)}\n")
        timings["Currents"] = (t_loop, t_useall, t_file)

        # --- Losses ---
        print("--- Losses ---")
        t_loop, loop_l = _time_call("toolkit: losses_elements", lambda: results.losses_elements)
        t_useall, useall_l = _time_call(
            "useall: AtivaElemento + reads",
            lambda: collect_useall_losses(dss, pd_elements),
        )

        def _file_losses():
            fp = _export_file(dss, out_dir, "export losses", "losses_bench")
            text = fp.read_text(encoding="utf-8")
            return _parse_losses_file(text, pd_elements)

        t_file, file_l = _time_call("file: export losses + parse", _file_losses)
        _report_pair_diff(useall_l, loop_l, "Useall vs toolkit Losses")
        _report_pair_diff(file_l, loop_l, "File vs toolkit Losses")
        print(f"  Fastest: {_fastest_label(t_loop, t_useall, t_file)}\n")
        timings["Losses"] = (t_loop, t_useall, t_file)

        # --- Combined ---
        print("--- Combined (all four quantities, one snapshot) ---")

        def _all_toolkit():
            return (
                results.voltage_ln_nodes_loop,
                results.powers_elements,
                results.currents_elements,
                results.losses_elements,
            )

        def _all_useall():
            return collect_useall_style_all(dss, pd_pc_elements, pd_elements)

        def _all_files():
            paths = {
                key: _export_file(dss, out_dir, cmd, f"all_{key}").read_text(encoding="utf-8")
                for cmd, key in MAIN_EXPORTS
            }
            no_path = _export_file(dss, out_dir, NODEORDER_CMD[0], "all_nodeorder")
            no = _parse_nodeorder(no_path.read_text(encoding="utf-8"))
            return (
                _parse_voltages_file(paths["voltages"]),
                _parse_elem_pq_file(paths["powers"], no, pd_pc_elements),
                _parse_currents_file(paths["currents"], no, pd_pc_elements),
                _parse_losses_file(paths["losses"], pd_elements),
            )

        t_loop_all, all_loop = _time_call("toolkit: all four properties", _all_toolkit)
        t_useall_all, all_useall = _time_call("useall: all four collectors", _all_useall)
        t_file_all, all_file = _time_call("file: all exports + NodeOrder + parse", _all_files)
        labels = ("LN voltages", "Powers", "Currents", "Losses")
        for label, u_dfs, l_dfs in zip(labels, all_useall, all_loop):
            _report_pair_diff(u_dfs, l_dfs, f"Useall vs toolkit {label}")
        for label, f_dfs, l_dfs in zip(labels, all_file, all_loop):
            _report_pair_diff(f_dfs, l_dfs, f"File vs toolkit {label}")
        print(f"  Combined fastest: {_fastest_label(t_loop_all, t_useall_all, t_file_all)}\n")

        num_lines = len(dss.lines.names)
        reads_per_line = 10 if SIMULATE_FULL_USEALL_READS else 0
        reads_per_elem = 2 + reads_per_line  # set_active_element + set_active_bus + reads

        # --- Summary ---
        print("--- Summary ---")
        print(
            f"  {'Quantity':<14} {'Toolkit':>10} {'Useall':>10} {'File':>10}  Fastest"
        )
        print(f"  {'-' * 14} {'-' * 10} {'-' * 10} {'-' * 10}  {'-' * 20}")
        for name, (tl, tu, tf) in timings.items():
            print(
                f"  {name:<14} {tl:10.4f} {tu:10.4f} {tf:10.4f}  "
                f"{_fastest_label(tl, tu, tf)}"
            )
        print(
            f"  {'COMBINED':<14} {t_loop_all:10.4f} {t_useall_all:10.4f} {t_file_all:10.4f}  "
            f"{_fastest_label(t_loop_all, t_useall_all, t_file_all)}"
        )
        print()
        print(f"Useall API pattern: AtivaElemento (set_active_element + set_active_bus bus2)")
        print(f"  Full reads per iteration: {SIMULATE_FULL_USEALL_READS}")
        print(f"  Lines: {num_lines} x (~2 + {reads_per_line} reads) = ~{num_lines * reads_per_elem}")
        print(f"  PD+PC elements: {len(pd_pc_elements)} x (~2 + {reads_per_line} reads)")
        print(f"  PD losses: {len(pd_elements)} x (~2 + {reads_per_line} reads)")
        print("NodeOrder export: pre-exported once for file parsers (not timed in useall path).")
        print("LN voltages file breakdown (write/read/parse): "
              f"{t_write:.4f}s / {t_read:.4f}s / {t_parse:.4f}s")
        print()
        print("Interpretation:")
        print("  - Toolkit loop: minimal API calls (fastest in Python ctypes).")
        print("  - Useall loop: mirrors C# AtivaElemento + multi-read pattern.")
        print("  - File export: bulk OpenDSS writes; may beat Useall even if slower than toolkit.")


if __name__ == "__main__":
    main()
