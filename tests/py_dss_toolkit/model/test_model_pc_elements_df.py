from _dss_script_runner import run_dss_script
from py_dss_toolkit import dss_tools


SCRIPT_MIXED_PC = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B.1.2.3 kw=100 pf=1
New Generator.G1 bus1=B.1.2.3 phases=3 kw=50 pf=1 model=3
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_DISABLED_PC = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B kw=100 pf=1 enabled=no
New Generator.G1 bus1=B phases=3 kw=50 pf=1 model=3
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_NO_PC = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_SINGLE_LOAD = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# pc_elements_df (loads, generators, pvsystems, storage — no capacitors)
# ---------------------------------------------------------------------------


def test_pc_elements_df_columns():
    run_dss_script(SCRIPT_MIXED_PC)
    df = dss_tools.model.pc_elements_df
    assert list(df.columns) == ["name", "bus1", "nodes1", "type", "enabled"]


def test_pc_elements_df_returns_all_pc_types():
    run_dss_script(SCRIPT_MIXED_PC)
    df = dss_tools.model.pc_elements_df
    assert df is not None
    types = set(df["type"])
    assert types == {"load", "generator"}


def test_pc_elements_df_does_not_include_capacitors():
    """Capacitors are PD elements; they must not appear in pc_elements_df."""
    script = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B kw=100 pf=1
New Capacitor.C1 bus1=B phases=3 kvar=50
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""
    run_dss_script(script)
    df = dss_tools.model.pc_elements_df
    assert df is not None
    assert "capacitor" not in set(df["type"])


def test_pc_elements_df_includes_disabled():
    run_dss_script(SCRIPT_DISABLED_PC)
    df = dss_tools.model.pc_elements_df
    assert df is not None
    assert len(df) == 2
    names = set(df["name"])
    assert "load.l1" in names
    assert "generator.g1" in names


def test_pc_elements_df_none_when_no_pc_elements():
    run_dss_script(SCRIPT_NO_PC)
    df = dss_tools.model.pc_elements_df
    assert df is None


def test_pc_elements_df_bus_and_nodes():
    run_dss_script(SCRIPT_SINGLE_LOAD)
    df = dss_tools.model.pc_elements_df
    assert df is not None
    row = df.iloc[0]
    assert row["name"] == "load.l1"
    assert row["bus1"] == "b"
    assert row["nodes1"] == ["1", "2", "3"]
    assert row["type"] == "load"


# ---------------------------------------------------------------------------
# enabled_pc_elements_df
# ---------------------------------------------------------------------------


def test_enabled_pc_elements_df_excludes_disabled():
    run_dss_script(SCRIPT_DISABLED_PC)
    df = dss_tools.model.enabled_pc_elements_df
    assert df is not None
    assert len(df) == 1
    assert df.iloc[0]["name"] == "generator.g1"
    assert "enabled" not in df.columns


def test_enabled_pc_elements_df_none_when_all_disabled():
    run_dss_script(SCRIPT_DISABLED_PC)
    df = dss_tools.model.pc_elements_df
    disabled_names = set(df[~df["enabled"]]["name"])
    assert "load.l1" in disabled_names

    enabled_script = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B kw=100 pf=1 enabled=no
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""
    run_dss_script(enabled_script)
    df = dss_tools.model.enabled_pc_elements_df
    assert df is None


def test_enabled_pc_elements_df_none_when_no_pc_elements():
    run_dss_script(SCRIPT_NO_PC)
    df = dss_tools.model.enabled_pc_elements_df
    assert df is None


# ---------------------------------------------------------------------------
# disabled_pc_elements_df
# ---------------------------------------------------------------------------


def test_disabled_pc_elements_df_returns_only_disabled():
    run_dss_script(SCRIPT_DISABLED_PC)
    df = dss_tools.model.disabled_pc_elements_df
    assert df is not None
    assert len(df) == 1
    assert df.iloc[0]["name"] == "load.l1"
    assert "enabled" not in df.columns


def test_disabled_pc_elements_df_none_when_all_enabled():
    run_dss_script(SCRIPT_MIXED_PC)
    df = dss_tools.model.disabled_pc_elements_df
    assert df is None


def test_disabled_pc_elements_df_none_when_no_pc_elements():
    run_dss_script(SCRIPT_NO_PC)
    df = dss_tools.model.disabled_pc_elements_df
    assert df is None
