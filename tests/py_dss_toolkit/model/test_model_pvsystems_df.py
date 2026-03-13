from tests.py_dss_toolkit.model._dss_script_runner import run_dss_script
from py_dss_toolkit import dss_tools


SCRIPT_ENABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B kw=50 pf=1
New PVSystem.PV1 bus1=B phases=3 kv=13.8 kVA=100 pmpp=80 irrad=1 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_DISABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B kw=50 pf=1
New PVSystem.PV1 bus1=B phases=3 kv=13.8 kVA=100 pmpp=80 irrad=1 pf=1 enabled=no
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""

SCRIPT_NONE = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
New Load.L1 bus1=B kw=50 pf=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_pvsystems_df_enabled_returns_row():
    run_dss_script(SCRIPT_ENABLED)
    df = dss_tools.model.pvsystems_df
    assert df is not None
    assert set(df["name"].str.lower()) == {"pv1"}


def test_pvsystems_df_disabled_returns_none():
    run_dss_script(SCRIPT_DISABLED)
    df = dss_tools.model.pvsystems_df
    assert df is None


def test_pvsystems_df_none_when_no_pvsystems():
    run_dss_script(SCRIPT_NONE)
    df = dss_tools.model.pvsystems_df
    assert df is None

