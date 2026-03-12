# -*- coding: utf-8 -*-
"""
Unit tests for ModelQueries topology, feeding_voltage, and bus_connection_type.

Each test uses a minimal DSS script that exercises one specific branch of the
decision logic, making the expected values easy to reason about.
"""

import math

import pytest
import py_dss_interface

from py_dss_toolkit import dss_tools

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_NO_TRANSFORMER = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 phases=3 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l1 bus1=B kw=100 pf=1
Set voltagebases=[13.8]
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

SCRIPT_3PH_DD = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kv=13.8 kva=300 conn=delta
~ wdg=2 bus=B kv=0.22  kva=300 conn=delta
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_1PH_LL = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=1 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A.1.2 kv=13.8 kva=100
~ wdg=2 bus=B.1.2 kv=0.22  kva=100
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_1PH_LN = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=1 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A.2 kv=7.9674  kva=100
~ wdg=2 bus=B.2 kv=0.12702 kva=100
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

# Center-tap transformer (3 windings): secondary is always LN
SCRIPT_CENTER_TAP = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=1 windings=3 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A.2 kv=7.2 kva=25 conn=wye
~ wdg=2 bus=B.1.0 kv=0.24 kva=25 conn=wye
~ wdg=3 bus=B.0.2 kv=0.24 kva=25 conn=wye
Set voltagebases=[13.8 0.24]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def run_dss_script(script: str):
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())


# ---------------------------------------------------------------------------
# source_bus
# ---------------------------------------------------------------------------


def test_source_bus_returns_vsource_bus():
    """source_bus returns the bus where the Vsource is connected."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    assert dss_tools.model.source_bus == "a"


def test_source_bus_3ph_transformer_circuit():
    """source_bus in a circuit with transformer."""
    run_dss_script(SCRIPT_3PH_DY)
    assert dss_tools.model.source_bus == "a"


# ---------------------------------------------------------------------------
# upstream_transformer
# ---------------------------------------------------------------------------


def test_upstream_transformer_returns_nearest_transformer():
    """upstream_transformer returns the nearest transformer on path to source."""
    run_dss_script(SCRIPT_3PH_DY)
    tr = dss_tools.model.upstream_transformer("b")
    assert tr is not None
    assert tr.get("type") == "transformer"
    assert tr.get("name", "").lower() == "transformer.t1"
    assert tr.get("kv_secondary") == 0.22


def test_upstream_transformer_none_when_no_transformer():
    """upstream_transformer returns None when no transformer on path."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    assert dss_tools.model.upstream_transformer("b") is None


def test_upstream_transformer_source_bus_returns_none():
    """upstream_transformer at source bus returns None (no upstream)."""
    run_dss_script(SCRIPT_3PH_DY)
    assert dss_tools.model.upstream_transformer("a") is None


# ---------------------------------------------------------------------------
# is_bus_in_model
# ---------------------------------------------------------------------------


def test_is_bus_in_model_true():
    """Known bus returns True."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    assert dss_tools.model.is_bus_in_model("a") is True
    assert dss_tools.model.is_bus_in_model("b") is True


def test_is_bus_in_model_false():
    """Unknown bus returns False."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    assert dss_tools.model.is_bus_in_model("nonexistent") is False


def test_is_bus_in_model_case_insensitive():
    """Bus lookup is case-insensitive."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    assert dss_tools.model.is_bus_in_model("A") is True
    assert dss_tools.model.is_bus_in_model("B") is True


# ---------------------------------------------------------------------------
# feeding_voltage
# ---------------------------------------------------------------------------


def test_feeding_voltage_no_transformer_falls_back_to_vsource():
    """No transformer on path -> falls back to Vsource base kV (3-phase circuit)."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    vll, vln = dss_tools.model.feeding_voltage("b")
    assert vll == 13.8
    assert round(vln, 4) == round(13.8 / math.sqrt(3), 4)


def test_feeding_voltage_3ph_dy_secondary_wye():
    """3-phase transformer, wye secondary: kv_secondary is vll."""
    run_dss_script(SCRIPT_3PH_DY)
    vll, vln = dss_tools.model.feeding_voltage("b")
    assert vll == 0.22
    assert vln == round(0.22 / math.sqrt(3), 4)


def test_feeding_voltage_3ph_dd_secondary_delta():
    """3-phase transformer, delta secondary: kv_secondary is still vll (formula unchanged)."""
    run_dss_script(SCRIPT_3PH_DD)
    vll, vln = dss_tools.model.feeding_voltage("b")
    assert vll == 0.22
    assert vln == round(0.22 / math.sqrt(3), 4)


def test_feeding_voltage_1ph_ll_two_phase_nodes():
    """1-phase transformer, secondary bus=B.1.2 (two phase nodes): kv_secondary is vll."""
    run_dss_script(SCRIPT_1PH_LL)
    kv_secondary = 0.22
    vll, vln = dss_tools.model.feeding_voltage("b")
    assert vll == kv_secondary
    assert vln == round(kv_secondary / math.sqrt(3), 4)


def test_feeding_voltage_1ph_ln_one_phase_node():
    """1-phase transformer, secondary bus=B.2 (one phase node): kv_secondary is vln."""
    run_dss_script(SCRIPT_1PH_LN)
    kv_secondary = 0.127
    vll, vln = dss_tools.model.feeding_voltage("b")
    assert vln == kv_secondary
    assert vll == round(kv_secondary * math.sqrt(3), 4)


def test_feeding_voltage_raises_for_nonexistent_bus():
    """feeding_voltage raises ValueError when bus does not exist in circuit."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.feeding_voltage("nonexistent")


def test_feeding_voltage_source_bus():
    """Source bus (no upstream transformer) falls back to Vsource base kV."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    vll, vln = dss_tools.model.feeding_voltage("a")
    assert vll == 13.8
    assert round(vln, 4) == round(13.8 / math.sqrt(3), 4)


def test_feeding_voltage_center_tap_always_ln():
    """Center-tap transformer (3+ windings): vln = kv_secondary, vll = 2*vln."""
    run_dss_script(SCRIPT_CENTER_TAP)
    vll, vln = dss_tools.model.feeding_voltage("b")
    assert vln == 0.24
    assert vll == 0.48


# ---------------------------------------------------------------------------
# bus_connection_type
# ---------------------------------------------------------------------------


def test_bus_connection_type_no_transformer_is_ln():
    """No upstream transformer -> always 'ln'."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    assert dss_tools.model.bus_connection_type("b") == "ln"


def test_bus_connection_type_3ph_wye_secondary_is_ln():
    """3-phase transformer with wye secondary -> 'ln'."""
    run_dss_script(SCRIPT_3PH_DY)
    assert dss_tools.model.bus_connection_type("b") == "ln"


def test_bus_connection_type_3ph_delta_secondary_is_ll():
    """3-phase transformer with delta secondary -> 'll'."""
    run_dss_script(SCRIPT_3PH_DD)
    assert dss_tools.model.bus_connection_type("b") == "ll"


def test_bus_connection_type_1ph_two_phase_nodes_is_ll():
    """1-phase transformer, secondary bus=B.1.2 (two phase nodes) -> 'll'."""
    run_dss_script(SCRIPT_1PH_LL)
    assert dss_tools.model.bus_connection_type("b") == "ll"


def test_bus_connection_type_1ph_one_phase_node_is_ln():
    """1-phase transformer, secondary bus=B.2 (one phase node) -> 'ln'."""
    run_dss_script(SCRIPT_1PH_LN)
    assert dss_tools.model.bus_connection_type("b") == "ln"


def test_bus_connection_type_center_tap_always_ln():
    """Center-tap transformer (3+ windings) -> always 'ln'."""
    run_dss_script(SCRIPT_CENTER_TAP)
    assert dss_tools.model.bus_connection_type("b") == "ln"


def test_bus_connection_type_raises_for_nonexistent_bus():
    """bus_connection_type raises ValueError when bus does not exist in circuit."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.bus_connection_type("nonexistent")


def test_bus_connection_type_source_bus():
    """Source bus (no upstream transformer) -> 'ln'."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    assert dss_tools.model.bus_connection_type("a") == "ln"


# ---------------------------------------------------------------------------
# bus_connection_type_map
# ---------------------------------------------------------------------------

SCRIPT_DELTA_WITH_DOWNSTREAM = """
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

SCRIPT_CASCADED_TRANSFORMERS = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kv=13.8 kva=300 conn=delta
~ wdg=2 bus=B kv=4.16 kva=300 conn=delta
New Transformer.T2 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=B kv=4.16 kva=100 conn=delta
~ wdg=2 bus=C kv=0.22 kva=100 conn=wye
New load.l bus1=C kw=50 pf=1
Set voltagebases=[13.8 4.16 0.22]
Calcvoltagebases
Solve
"""


def test_bus_connection_type_map_no_transformer_all_ln():
    """No transformer -> every bus is 'ln'."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    m = dss_tools.model.bus_connection_type_map
    assert isinstance(m, dict)
    assert all(v == "ln" for v in m.values())
    assert "a" in m and "b" in m


def test_bus_connection_type_map_delta_secondary_propagates():
    """Delta secondary -> downstream buses inherit 'll'."""
    run_dss_script(SCRIPT_DELTA_WITH_DOWNSTREAM)
    m = dss_tools.model.bus_connection_type_map
    assert m["a"] == "ln"
    assert m["b"] == "ll"
    assert m["c"] == "ll"


def test_bus_connection_type_map_cascaded_transformers():
    """Delta->delta then delta->wye: B='ll', C='ln' (new transformer resets)."""
    run_dss_script(SCRIPT_CASCADED_TRANSFORMERS)
    m = dss_tools.model.bus_connection_type_map
    assert m["a"] == "ln"
    assert m["b"] == "ll"
    assert m["c"] == "ln"


def test_bus_connection_type_map_wye_secondary_is_ln():
    """3-phase delta-wye transformer: secondary bus is 'ln'."""
    run_dss_script(SCRIPT_3PH_DY)
    m = dss_tools.model.bus_connection_type_map
    assert m["a"] == "ln"
    assert m["b"] == "ln"


def test_bus_connection_type_map_center_tap_is_ln():
    """Center-tap transformer: secondary bus is 'ln'."""
    run_dss_script(SCRIPT_CENTER_TAP)
    m = dss_tools.model.bus_connection_type_map
    assert m["b"] == "ln"


def test_bus_connection_type_map_1ph_ll():
    """1-phase transformer with two phase conductors: secondary bus is 'll'."""
    run_dss_script(SCRIPT_1PH_LL)
    m = dss_tools.model.bus_connection_type_map
    assert m["b"] == "ll"


def test_bus_connection_type_map_consistent_with_per_bus():
    """bus_connection_type_map values match bus_connection_type for every bus."""
    run_dss_script(SCRIPT_DELTA_WITH_DOWNSTREAM)
    m = dss_tools.model.bus_connection_type_map
    for bus_name, expected in m.items():
        assert dss_tools.model.bus_connection_type(bus_name) == expected


# ---------------------------------------------------------------------------
# Topology queries: upstream/downstream segments and buses
# ---------------------------------------------------------------------------

SCRIPT_RADIAL_ABC = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Line.L2 bus1=B bus2=C phases=3 r1=0.1 x1=0.1 c1=0 length=1
New load.l bus1=C kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_SAME_BUSES_3XFMR = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoA phases=1 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800
~ wdg=1 bus=A.1.2 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.1 kv=0.127 kva=37.5 conn=wye
New Transformer.TrafoB phases=1 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800
~ wdg=1 bus=A.2.3 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.2 kv=0.127 kva=37.5 conn=wye
New Transformer.TrafoC phases=1 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800
~ wdg=1 bus=A.3.1 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.3 kv=0.127 kva=37.5 conn=wye
New load.l bus1=B kw=112.5 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""


# -- Upstream segments from bus --


def test_upstream_segments_from_bus_radial():
    """Radial A->B->C: upstream segments from B = [L1], level=1."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_segments_from_bus_df("b")
    assert len(df) == 1
    assert df.iloc[0]["segment"] == "line.l1"
    assert df.iloc[0]["level"] == 1


def test_upstream_segments_from_bus_source_empty():
    """Source bus has no upstream segments; empty DF has correct columns."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_segments_from_bus_df("a")
    assert len(df) == 0
    assert "segment" in df.columns and "level" in df.columns


def test_upstream_segments_from_bus_raises_for_nonexistent_bus():
    """Nonexistent bus raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.upstream_segments_from_bus_df("nonexistent")


# -- Downstream segments from bus --


def test_downstream_segments_from_bus_radial():
    """Radial A->B->C: downstream segments from B = [L2], level=1."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_segments_from_bus_df("b")
    assert len(df) == 1
    assert df.iloc[0]["segment"] == "line.l2"
    assert df.iloc[0]["level"] == 1


def test_downstream_segments_from_bus_leaf_empty():
    """Leaf bus has no downstream segments; empty DF has correct columns."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_segments_from_bus_df("c")
    assert len(df) == 0
    assert "segment" in df.columns and "level" in df.columns


def test_downstream_segments_from_bus_raises_for_nonexistent_bus():
    """Nonexistent bus raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.downstream_segments_from_bus_df("nonexistent")


# -- segments_at_bus_df --


def test_segments_at_bus_df_radial():
    """segments_at_bus_df returns all segments at bus with direction."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.segments_at_bus_df("b")
    assert len(df) == 2
    assert set(df["name"]) == {"line.l1", "line.l2"}
    assert "direction" in df.columns
    outgoing = df[df["direction"] == "outgoing"]
    incoming = df[df["direction"] == "incoming"]
    assert len(outgoing) == 1 and outgoing.iloc[0]["name"] == "line.l2"
    assert len(incoming) == 1 and incoming.iloc[0]["name"] == "line.l1"


def test_segments_at_bus_df_raises_for_nonexistent_bus():
    """segments_at_bus_df raises ValueError for nonexistent bus."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.segments_at_bus_df("nonexistent")


# -- upstream_transformers_df --


def test_upstream_transformers_df_single_transformer():
    """upstream_transformers_df returns transformer on path."""
    run_dss_script(SCRIPT_3PH_DY)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_transformers_df("b")
    assert len(df) == 1
    assert df.iloc[0]["segment"] == "transformer.t1"
    assert df.iloc[0]["level"] == 1
    assert df.iloc[0]["kv_secondary"] == 0.22


def test_upstream_transformers_df_empty_when_no_transformer():
    """upstream_transformers_df empty when no transformer on path."""
    run_dss_script(SCRIPT_NO_TRANSFORMER)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_transformers_df("b")
    assert len(df) == 0
    assert "segment" in df.columns and "level" in df.columns


def test_upstream_transformers_df_raises_for_nonexistent_bus():
    """upstream_transformers_df raises ValueError for nonexistent bus."""
    run_dss_script(SCRIPT_3PH_DY)
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.upstream_transformers_df("nonexistent")


# -- Upstream buses from bus --


def test_upstream_buses_from_bus_radial():
    """Radial A->B->C: upstream buses from B = [a] with level=1, and buses_df properties."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_buses_from_bus_df("b")
    assert "bus" in df.columns and "level" in df.columns
    assert len(df) == 1
    assert df.iloc[0]["bus"] == "a"
    assert df.iloc[0]["level"] == 1
    assert "kv_base" in df.columns or "distance" in df.columns


def test_upstream_buses_from_bus_source_empty():
    """Source bus has no upstream buses; empty DF has correct columns."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_buses_from_bus_df("a")
    assert len(df) == 0
    assert "bus" in df.columns and "level" in df.columns


def test_upstream_buses_from_bus_raises_for_nonexistent_bus():
    """Nonexistent bus raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.upstream_buses_from_bus_df("nonexistent")


# -- Downstream buses from bus --


def test_downstream_buses_from_bus_radial():
    """Radial A->B->C: downstream buses from B = [c] with level=1, and buses_df properties."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_buses_from_bus_df("b")
    assert "bus" in df.columns and "level" in df.columns
    assert len(df) == 1
    assert df.iloc[0]["bus"] == "c"
    assert df.iloc[0]["level"] == 1
    assert "kv_base" in df.columns or "distance" in df.columns


def test_downstream_buses_from_bus_leaf_empty():
    """Leaf bus has no downstream buses; empty DF has correct columns."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_buses_from_bus_df("c")
    assert len(df) == 0
    assert "bus" in df.columns and "level" in df.columns


def test_downstream_buses_from_bus_raises_for_nonexistent_bus():
    """Nonexistent bus raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.downstream_buses_from_bus_df("nonexistent")


# -- Upstream/downstream segments from segment --


def test_upstream_segments_from_segment():
    """Upstream of line.l2 = [line.l1]."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_segments_from_segment_df("line.l2")
    assert len(df) == 1
    assert df.iloc[0]["segment"] == "line.l1"


def test_downstream_segments_from_segment():
    """Downstream of line.l1 = [line.l2]."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_segments_from_segment_df("line.l1")
    assert len(df) == 1
    assert df.iloc[0]["segment"] == "line.l2"


def test_upstream_segments_from_segment_unknown_returns_error():
    """Unknown segment raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.upstream_segments_from_segment_df("line.nonexistent")


def test_downstream_segments_from_segment_unknown_returns_error():
    """Unknown segment raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.downstream_segments_from_segment_df("line.nonexistent")


# -- Upstream/downstream buses from segment --


def test_upstream_buses_from_segment():
    """Upstream buses of line.l2 = [a, b] with levels [1, 2]."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.upstream_buses_from_segment_df("line.l2")
    assert list(df["bus"].tolist()) == ["a", "b"]
    assert list(df["level"].tolist()) == [1, 2]


def test_downstream_buses_from_segment():
    """Downstream buses of line.l1 = [b, c] with levels [1, 2]."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.downstream_buses_from_segment_df("line.l1")
    assert list(df["bus"].tolist()) == ["b", "c"]
    assert list(df["level"].tolist()) == [1, 2]


def test_upstream_buses_from_segment_unknown_returns_error():
    """Unknown segment raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.upstream_buses_from_segment_df("line.nonexistent")


def test_downstream_buses_from_segment_unknown_returns_error():
    """Unknown segment raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.downstream_buses_from_segment_df("line.nonexistent")


# -- Path between buses: segments --


def test_segments_path_between_buses_same_buses():
    """3 transformers between A and B: segments_path_between_buses_df returns 3."""
    run_dss_script(SCRIPT_SAME_BUSES_3XFMR)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.segments_path_between_buses_df("a", "b")
    assert len(df) == 3
    names = set(df["segment"].tolist())
    assert names == {"transformer.trafoa", "transformer.trafob", "transformer.trafoc"}


def test_segments_path_between_buses_order_independent():
    """segments_path_between_buses_df(bus1, bus2) same as (bus2, bus1)."""
    run_dss_script(SCRIPT_SAME_BUSES_3XFMR)
    dss_tools.model.refresh_graph()
    df_ab = dss_tools.model.segments_path_between_buses_df("a", "b")
    df_ba = dss_tools.model.segments_path_between_buses_df("b", "a")
    assert len(df_ab) == len(df_ba) == 3


def test_segments_path_between_buses_non_neighbors():
    """Radial A->B->C: segments path between A and C returns L1 and L2."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.segments_path_between_buses_df("a", "c")
    assert len(df) == 2
    segments = set(df["segment"].str.lower())
    assert segments == {"line.l1", "line.l2"}
    assert list(df["level"]) == [1, 2]


def test_segments_path_between_buses_same_bus():
    """Path from bus to itself: no segments, empty DF with correct columns."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.segments_path_between_buses_df("b", "b")
    assert len(df) == 0
    assert "segment" in df.columns and "level" in df.columns


def test_segments_path_between_buses_raises_for_nonexistent_bus():
    """Nonexistent bus raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.segments_path_between_buses_df("nonexistent", "b")


def test_segments_path_between_buses_empty_columns_consistency():
    """Empty result has same column schema as non-empty result."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df_empty = dss_tools.model.segments_path_between_buses_df("b", "b")
    df_full = dss_tools.model.segments_path_between_buses_df("a", "c")
    assert "segment" in df_empty.columns
    assert "level" in df_empty.columns


# -- Path between buses: buses --


def test_buses_path_between_buses_df():
    """Radial A->B->C: buses path between A and C returns [a, b, c] with level 1, 2, 3."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.buses_path_between_buses_df("a", "c")
    assert "bus" in df.columns and "level" in df.columns
    assert list(df["bus"]) == ["a", "b", "c"]
    assert list(df["level"]) == [1, 2, 3]
    assert "kv_base" in df.columns or "distance" in df.columns


def test_buses_path_between_buses_same_bus():
    """Path from bus to itself: returns single row with level=1."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    df = dss_tools.model.buses_path_between_buses_df("b", "b")
    assert len(df) == 1
    assert df.iloc[0]["bus"] == "b"
    assert df.iloc[0]["level"] == 1


def test_buses_path_between_buses_raises_for_nonexistent_bus():
    """Nonexistent bus raises ValueError."""
    run_dss_script(SCRIPT_RADIAL_ABC)
    dss_tools.model.refresh_graph()
    with pytest.raises(ValueError, match="does not exist in the circuit"):
        dss_tools.model.buses_path_between_buses_df("nonexistent", "b")
