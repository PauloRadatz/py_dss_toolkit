# -*- coding: utf-8 -*-
"""
Tests for create_nodal_smart_voltage_dataframes and the VoltagesNodalSmart
property when accessed through dss_tools.
"""

import pandas as pd
import py_dss_interface

from py_dss_toolkit import dss_tools
from py_dss_toolkit.results.SnapShot.voltages_nodal_utils import create_nodal_ll_voltage_dataframes
from py_dss_toolkit.results.SnapShot.voltages_nodal_utils import create_nodal_smart_voltage_dataframes
from py_dss_toolkit.results.SnapShot.voltages_nodal_utils import create_nodal_voltage_dataframes

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_3PH_DD = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kv=13.8 kva=300 conn=delta
~ wdg=2 bus=B kv=0.22  kva=300 conn=delta
New Line.L1 bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=C kw=50 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_3PH_DY = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kV=13.8 kva=300 conn=delta
~ wdg=2 bus=B kV=0.22  kva=300 conn=wye
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""


def _run(script: str):
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())


# ---------------------------------------------------------------------------
# create_nodal_smart_voltage_dataframes
# ---------------------------------------------------------------------------


def test_smart_util_all_ln():
    """When connection_type_map maps every bus to 'ln', result matches LN util."""
    _run(SCRIPT_3PH_DY)
    dss = dss_tools.dss
    conn_map = {b.lower(): "ln" for b in dss.circuit.buses_names}

    smart_vmags, smart_vangs = create_nodal_smart_voltage_dataframes(dss, conn_map)
    ln_vmags, ln_vangs = create_nodal_voltage_dataframes(dss)

    pd.testing.assert_frame_equal(smart_vmags.drop(columns=["voltage_type"]), ln_vmags)
    pd.testing.assert_frame_equal(smart_vangs.drop(columns=["voltage_type"]), ln_vangs)
    assert (smart_vmags["voltage_type"] == "ln").all()


def test_smart_util_ll_buses_use_ll_voltages():
    """Buses mapped to 'll' should get LL voltages instead of LN."""
    _run(SCRIPT_3PH_DD)
    dss = dss_tools.dss
    conn_map = {"a": "ln", "b": "ll", "c": "ll"}

    smart_vmags, _ = create_nodal_smart_voltage_dataframes(dss, conn_map)
    ln_vmags, _ = create_nodal_voltage_dataframes(dss)
    ll_vmags, _ = create_nodal_ll_voltage_dataframes(dss)

    smart_vmags_numeric = smart_vmags.drop(columns=["voltage_type"])

    # Bus "a" (LN) should match the LN result
    pd.testing.assert_series_equal(smart_vmags_numeric.loc["a"].dropna(), ln_vmags.loc["a"].dropna(), check_names=False)

    # Bus "b" (LL) should match the LL result (if LL data exists)
    if "b" in ll_vmags.index and not ll_vmags.loc["b"].isna().all():
        pd.testing.assert_series_equal(
            smart_vmags_numeric.loc["b"].dropna(),
            ll_vmags.loc["b"].dropna(),
            check_names=False,
        )

    # voltage_type column reflects LN/LL per bus
    assert smart_vmags.loc["a", "voltage_type"] == "ln"
    assert smart_vmags.loc["b", "voltage_type"] == "ll"
    assert smart_vmags.loc["c", "voltage_type"] == "ll"


def test_smart_util_empty_map_defaults_to_ln():
    """Empty connection_type_map means all buses default to 'ln'."""
    _run(SCRIPT_3PH_DY)
    dss = dss_tools.dss
    smart_vmags, smart_vangs = create_nodal_smart_voltage_dataframes(dss, {})
    ln_vmags, ln_vangs = create_nodal_voltage_dataframes(dss)

    pd.testing.assert_frame_equal(smart_vmags.drop(columns=["voltage_type"]), ln_vmags)
    pd.testing.assert_frame_equal(smart_vangs.drop(columns=["voltage_type"]), ln_vangs)


def test_smart_util_returns_correct_shape():
    """Returned DataFrames have one row per bus."""
    _run(SCRIPT_3PH_DD)
    dss = dss_tools.dss
    conn_map = dss_tools.model.bus_connection_type_map
    vmags, vangs = create_nodal_smart_voltage_dataframes(dss, conn_map)

    num_buses = len(dss.circuit.buses_names)
    assert vmags.shape[0] == num_buses
    assert vangs.shape[0] == num_buses


# ---------------------------------------------------------------------------
# VoltagesNodalSmart via dss_tools (end-to-end)
# ---------------------------------------------------------------------------


def test_voltage_nodes_via_dss_tools():
    """dss_tools.results.voltage_nodes returns DataFrames with voltage_type column."""
    _run(SCRIPT_3PH_DD)
    dss_tools.simulation.solve_snapshot()
    vmags, vangs = dss_tools.results.voltage_nodes

    assert isinstance(vmags, pd.DataFrame)
    assert isinstance(vangs, pd.DataFrame)
    num_buses = len(dss_tools.dss.circuit.buses_names)
    assert vmags.shape[0] == num_buses
    assert vangs.shape[0] == num_buses
    assert "voltage_type" in vmags.columns
    assert "voltage_type" in vangs.columns
    assert set(vmags["voltage_type"]) <= {"ln", "ll"}
    assert set(vangs["voltage_type"]) <= {"ln", "ll"}
