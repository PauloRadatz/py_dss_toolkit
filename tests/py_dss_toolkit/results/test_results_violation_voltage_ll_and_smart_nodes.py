# -*- coding: utf-8 -*-
"""Tests for violation_voltage_ll_nodes and violation_voltage_nodes."""

import pandas as pd
import pytest
import py_dss_interface

from py_dss_toolkit import dss_tools
from py_dss_toolkit.results.SnapShot.voltages_nodal_utils import (
    create_nodal_smart_voltage_dataframes,
)
from py_dss_toolkit.results.SnapShot.VoltagesNodalViolations import (
    VoltagesNodalViolations,
    _undervoltage_overvoltage_from_vmags,
)

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


def _run_dy():
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(SCRIPT_3PH_DY.strip())


def test_undervoltage_overvoltage_helper_ignores_voltage_type_column():
    df = pd.DataFrame(
        {
            "voltage_type": ["ln", "ll"],
            "node1": [0.90, 1.06],
        },
        index=["bus_a", "bus_b"],
    )
    under, over = _undervoltage_overvoltage_from_vmags(df, 0.95, 1.05)
    assert list(under.index) == ["bus_a"]
    assert list(over.index) == ["bus_b"]
    assert "voltage_type" in under.columns


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_violation_voltage_ll_nodes_shape(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    under, over = study.results.violation_voltage_ll_nodes
    assert under.shape[1] > 0
    assert over.shape[1] > 0


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_violation_voltage_nodes_has_expected_columns(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    under, over = study.results.violation_voltage_nodes
    assert "voltage_type" in under.columns
    assert "voltage_type" in over.columns
    assert under.shape[1] > 0
    assert over.shape[1] > 0


def test_violation_voltage_nodes_matches_helper_with_model_map():
    """results.violation_voltage_nodes matches manual check using the same connection map."""
    _run_dy()
    dss_tools.simulation.solve_snapshot()
    results = dss_tools.results
    conn_map = dss_tools.model.bus_connection_type_map

    vmags, _ = create_nodal_smart_voltage_dataframes(dss_tools.dss, conn_map)
    expected_under, expected_over = _undervoltage_overvoltage_from_vmags(
        vmags, results.v_min_pu, results.v_max_pu
    )

    under, over = results.violation_voltage_nodes
    pd.testing.assert_frame_equal(under, expected_under, check_index_type=False)
    pd.testing.assert_frame_equal(over, expected_over, check_index_type=False)


def test_violation_voltage_nodes_all_ln_map_matches_ln_nodes():
    """Explicit all-LN map: smart magnitudes match LN; violation sets match LN."""
    _run_dy()
    dss = dss_tools.dss
    conn_map = {b.lower(): "ln" for b in dss.circuit.buses_names}
    v = VoltagesNodalViolations(dss, conn_map)

    under_s, over_s = v.violation_voltage_nodes
    under_ln, over_ln = v.violation_voltage_ln_nodes

    pd.testing.assert_frame_equal(
        under_s.drop(columns=["voltage_type"]),
        under_ln,
        check_index_type=False,
    )
    pd.testing.assert_frame_equal(
        over_s.drop(columns=["voltage_type"]),
        over_ln,
        check_index_type=False,
    )
