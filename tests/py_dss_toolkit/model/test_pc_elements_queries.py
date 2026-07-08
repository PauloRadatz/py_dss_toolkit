# -*- coding: utf-8 -*-
"""
Unit tests for PCElementsQueries: downstream load, load between buses, generation.
"""

import py_dss_interface
import pytest

from py_dss_toolkit import dss_tools


def run_dss_script(script: str):
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())


# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_RADIAL_ABC_LOADS = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.lb bus1=B kw=30 pf=1
New load.lc bus1=C kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_NO_LOADS = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_WITH_GENERATOR = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=C kw=50 pf=1
New Generator.G1 bus1=B kw=100 pf=1 model=3
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# downstream_load_kw
# ---------------------------------------------------------------------------


def test_downstream_load_kw_bus_feeds_all_downstream():
    """downstream_load_kw(a) = sum of loads at B and C."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    assert dss_tools.model.downstream_load_kw("a") == 80.0


def test_downstream_load_kw_includes_bus_itself():
    """downstream_load_kw(b) includes load at B."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    assert dss_tools.model.downstream_load_kw("b") == 80.0


def test_downstream_load_kw_leaf_bus():
    """downstream_load_kw(c) = load at C only."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    assert dss_tools.model.downstream_load_kw("c") == 50.0


def test_downstream_load_kw_no_loads_returns_zero():
    """Circuit with no loads returns 0."""
    run_dss_script(SCRIPT_NO_LOADS)
    dss_tools.model.refresh_graph()
    assert dss_tools.model.downstream_load_kw("a") == 0.0
    assert dss_tools.model.downstream_load_kw("b") == 0.0


def test_downstream_load_kw_raises_for_nonexistent_bus():
    """downstream_load_kw raises ValueError for nonexistent bus."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.downstream_load_kw("nonexistent")


# ---------------------------------------------------------------------------
# downstream_load_kvar
# ---------------------------------------------------------------------------


def test_downstream_load_kvar():
    """downstream_load_kvar returns sum of kvar."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    kvar = dss_tools.model.downstream_load_kvar("a")
    assert kvar >= 0.0


# ---------------------------------------------------------------------------
# load_between_buses
# ---------------------------------------------------------------------------


def test_load_between_buses_kw_inclusive():
    """load_between_buses_kw includes all buses on path (inclusive)."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    kw = dss_tools.model.load_between_buses_kw("a", "c")
    assert kw == 80.0


def test_load_between_buses_kw_same_bus():
    """load_between_buses_kw(a,a) = load at A only."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    kw = dss_tools.model.load_between_buses_kw("a", "a")
    assert kw == 0.0


def test_load_between_buses_kw_same_bus_with_load():
    """load_between_buses_kw(b,b) = load at B."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    kw = dss_tools.model.load_between_buses_kw("b", "b")
    assert kw == 30.0


def test_load_between_buses_kw_no_path_returns_zero():
    """No path between buses (isolated branch) returns 0."""
    script = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l1 bus1=B kw=50 pf=1
New Line.Floating bus1=C bus2=D phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l2 bus1=D kw=30 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""
    run_dss_script(script)
    dss_tools.model.refresh_graph()
    kw = dss_tools.model.load_between_buses_kw("a", "d")
    assert kw == 0.0


# ---------------------------------------------------------------------------
# downstream_generator_kw, downstream_pvsystem_kw, downstream_storage_kw
# ---------------------------------------------------------------------------


def test_downstream_generator_kw_includes_generator():
    """downstream_generator_kw(a) includes generator at B."""
    run_dss_script(SCRIPT_WITH_GENERATOR)
    dss_tools.model.refresh_graph()
    gen_kw = dss_tools.model.downstream_generator_kw("a")
    assert gen_kw == 100.0


def test_downstream_generator_kw_no_generation_returns_zero():
    """Circuit with no generators returns 0."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    assert dss_tools.model.downstream_generator_kw("a") == 0.0


def test_downstream_pvsystem_kw():
    """downstream_pvsystem_kw returns PV pmpp downstream."""
    script = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New PVSystem.PV1 bus1=B pmpp=50
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""
    run_dss_script(script)
    dss_tools.model.refresh_graph()
    assert dss_tools.model.downstream_pvsystem_kw("a") == 50.0


def test_downstream_storage_kw():
    """downstream_storage_kw returns storage kwrated downstream."""
    script = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Storage.S1 bus1=B kwrated=25
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""
    run_dss_script(script)
    dss_tools.model.refresh_graph()
    assert dss_tools.model.downstream_storage_kw("a") == 25.0


# ---------------------------------------------------------------------------
# generator_between_buses_kw, pvsystem_between_buses_kw, storage_between_buses_kw
# ---------------------------------------------------------------------------


def test_generator_between_buses_kw():
    """generator_between_buses_kw returns generator kW on path."""
    run_dss_script(SCRIPT_WITH_GENERATOR)
    dss_tools.model.refresh_graph()
    gen_kw = dss_tools.model.generator_between_buses_kw("a", "c")
    assert gen_kw == 100.0


def test_generator_between_buses_kw_same_bus():
    """generator_between_buses_kw(b,b) = generator at B."""
    run_dss_script(SCRIPT_WITH_GENERATOR)
    dss_tools.model.refresh_graph()
    gen_kw = dss_tools.model.generator_between_buses_kw("b", "b")
    assert gen_kw == 100.0


def test_pvsystem_between_buses_kw():
    """pvsystem_between_buses_kw returns PV pmpp on path."""
    script = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New PVSystem.PV1 bus1=B pmpp=50
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""
    run_dss_script(script)
    dss_tools.model.refresh_graph()
    pv_kw = dss_tools.model.pvsystem_between_buses_kw("a", "b")
    assert pv_kw == 50.0


def test_storage_between_buses_kw():
    """storage_between_buses_kw returns storage kwrated on path."""
    script = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Storage.S1 bus1=B kwrated=25
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""
    run_dss_script(script)
    dss_tools.model.refresh_graph()
    stor_kw = dss_tools.model.storage_between_buses_kw("a", "b")
    assert stor_kw == 25.0


# ---------------------------------------------------------------------------
# downstream_pc_elements_df
# ---------------------------------------------------------------------------


def test_downstream_pc_elements_df():
    """downstream_pc_elements_df returns per-bus breakdown."""
    run_dss_script(SCRIPT_RADIAL_ABC_LOADS)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_pc_elements_df("a")
    assert len(df) == 2
    assert set(df["element_type"]) == {"load"}
    assert set(df["bus"]) == {"b", "c"}
    assert df["kw"].sum() == 80.0


def test_downstream_pc_elements_df_empty_when_no_pc():
    """downstream_pc_elements_df returns empty DataFrame when no PC elements."""
    run_dss_script(SCRIPT_NO_LOADS)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_pc_elements_df("a")
    assert len(df) == 0
    assert "bus" in df.columns and "element_type" in df.columns
