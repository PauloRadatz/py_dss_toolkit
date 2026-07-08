from _dss_script_runner import run_dss_script

from py_dss_toolkit import dss_tools

SCRIPT_WITH_CAPACITOR = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Capacitor.C1 bus1=B phases=3 kvar=50
New Load.L1 bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_DELTA_CAPACITOR = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Capacitor.Cdelta bus1=B phases=3 kvar=50 conn=delta
New Load.L1 bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_SERIES_CAPACITOR = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Capacitor.CSeries bus1=B bus2=C phases=3 kvar=50
New Load.L1 bus1=C kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_MIXED_PD = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=B kV=13.8 kva=300 conn=delta
~ wdg=2 bus=C kV=0.22 kva=300 conn=wye
New Capacitor.C1 bus1=C phases=3 kvar=50
New Load.L1 bus1=C kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_NO_PD = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Load.L1 bus1=A kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


# ---------------------------------------------------------------------------
# pd_elements_df (includes all PD elements: lines, transformers, reactors, capacitors)
# ---------------------------------------------------------------------------


def test_pd_elements_df_columns():
    run_dss_script(SCRIPT_WITH_CAPACITOR)
    df = dss_tools.model.pd_elements_df
    assert list(df.columns) == [
        "name",
        "bus1",
        "nodes1",
        "bus2",
        "nodes2",
        "type",
        "x1",
        "y1",
        "x2",
        "y2",
        "enabled",
    ]


def test_pd_elements_df_includes_capacitor():
    """Shunt capacitor appears in pd_elements_df."""
    run_dss_script(SCRIPT_WITH_CAPACITOR)
    df = dss_tools.model.pd_elements_df
    assert df is not None
    types = set(df["type"])
    assert "capacitor" in types
    assert "line" in types


def test_pd_elements_df_includes_all_pd_types():
    """pd_elements_df includes lines, transformers, and capacitors."""
    run_dss_script(SCRIPT_MIXED_PD)
    df = dss_tools.model.pd_elements_df
    assert df is not None
    types = set(df["type"])
    assert types == {"line", "transformer", "capacitor"}


def test_pd_elements_df_none_when_no_pd_elements():
    run_dss_script(SCRIPT_NO_PD)
    df = dss_tools.model.pd_elements_df
    assert df is None


def test_pd_elements_df_wye_capacitor_has_same_bus():
    """Wye capacitor: OpenDSS returns bus2=bus.0.0.0 so bus1 == bus2."""
    run_dss_script(SCRIPT_WITH_CAPACITOR)
    df = dss_tools.model.pd_elements_df
    cap_rows = df[df["type"] == "capacitor"]
    assert len(cap_rows) == 1
    assert cap_rows.iloc[0]["bus1"] == cap_rows.iloc[0]["bus2"]


def test_pd_elements_df_delta_capacitor_has_empty_bus2():
    """Delta capacitor: OpenDSS returns no bus2, so bus2 is empty string."""
    run_dss_script(SCRIPT_DELTA_CAPACITOR)
    df = dss_tools.model.pd_elements_df
    cap_rows = df[df["type"] == "capacitor"]
    assert len(cap_rows) == 1
    assert cap_rows.iloc[0]["bus2"] == ""


def test_segments_df_excludes_delta_capacitor():
    """Delta capacitor (empty bus2) must not appear in segments_df."""
    run_dss_script(SCRIPT_DELTA_CAPACITOR)
    seg_df = dss_tools.model.segments_df
    assert seg_df is not None
    assert "capacitor" not in set(seg_df["type"])


def test_pd_elements_df_series_capacitor_has_different_buses():
    """Series capacitor has bus1 != bus2."""
    run_dss_script(SCRIPT_SERIES_CAPACITOR)
    df = dss_tools.model.pd_elements_df
    cap_rows = df[df["type"] == "capacitor"]
    assert len(cap_rows) == 1
    assert cap_rows.iloc[0]["bus1"] != cap_rows.iloc[0]["bus2"]


# ---------------------------------------------------------------------------
# segments_df vs pd_elements_df: shunt capacitors excluded from segments
# ---------------------------------------------------------------------------


def test_segments_df_excludes_shunt_capacitor():
    """Shunt capacitor (bus1 == bus2) must not appear in segments_df."""
    run_dss_script(SCRIPT_WITH_CAPACITOR)
    seg_df = dss_tools.model.segments_df
    assert seg_df is not None
    assert "capacitor" not in set(seg_df["type"])


def test_segments_df_includes_series_capacitor():
    """Series capacitor (bus1 != bus2) appears in segments_df."""
    run_dss_script(SCRIPT_SERIES_CAPACITOR)
    seg_df = dss_tools.model.segments_df
    assert seg_df is not None
    assert "capacitor.cseries" in set(seg_df["name"])


def test_pd_elements_df_is_superset_of_segments_df():
    """pd_elements_df includes everything in segments_df plus shunt elements."""
    run_dss_script(SCRIPT_WITH_CAPACITOR)
    pd_df = dss_tools.model.pd_elements_df
    seg_df = dss_tools.model.segments_df
    assert pd_df is not None
    assert seg_df is not None
    assert len(pd_df) > len(seg_df)
    seg_names = set(seg_df["name"])
    pd_names = set(pd_df["name"])
    assert seg_names.issubset(pd_names)


# ---------------------------------------------------------------------------
# enabled/disabled pd_elements_df
# ---------------------------------------------------------------------------


SCRIPT_DISABLED_CAP = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Capacitor.C1 bus1=B phases=3 kvar=50 enabled=no
New Load.L1 bus1=B kw=100 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_enabled_pd_elements_df_excludes_disabled():
    run_dss_script(SCRIPT_DISABLED_CAP)
    df = dss_tools.model.enabled_pd_elements_df
    assert df is not None
    assert "capacitor.c1" not in set(df["name"])
    assert "enabled" not in df.columns


def test_disabled_pd_elements_df_returns_only_disabled():
    run_dss_script(SCRIPT_DISABLED_CAP)
    df = dss_tools.model.disabled_pd_elements_df
    assert df is not None
    assert "capacitor.c1" in set(df["name"])
    assert "enabled" not in df.columns


def test_disabled_pd_elements_df_none_when_all_enabled():
    run_dss_script(SCRIPT_WITH_CAPACITOR)
    df = dss_tools.model.disabled_pd_elements_df
    assert df is None
