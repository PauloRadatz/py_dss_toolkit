from _dss_script_runner import run_dss_script
from py_dss_toolkit import dss_tools


SCRIPT_ENABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=1 windings=2 xhl=0.01 kVAs=[100 100]
~ wdg=1 bus=A.1 kv=13.8 kva=100 conn=delta
~ wdg=2 bus=B.1 kv=0.22  kva=100 conn=wye
New Regcontrol.R1 transformer=T1 winding=2 vreg=120 band=2 ptratio=60 ctprim=300 R=3 X=9
New Load.L1 bus1=B.1 kw=10 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_DISABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=1 windings=2 xhl=0.01 kVAs=[100 100]
~ wdg=1 bus=A.1 kv=13.8 kva=100 conn=delta
~ wdg=2 bus=B.1 kv=0.22  kva=100 conn=wye
New Regcontrol.R1 transformer=T1 winding=2 vreg=120 band=2 ptratio=60 ctprim=300 R=3 X=9 enabled=no
New Load.L1 bus1=B.1 kw=10 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_NONE = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=1 windings=2 xhl=0.01 kVAs=[100 100]
~ wdg=1 bus=A.1 kv=13.8 kva=100 conn=delta
~ wdg=2 bus=B.1 kv=0.22  kva=100 conn=wye
New Load.L1 bus1=B.1 kw=10 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""


def test_regcontrols_df_enabled_returns_row():
    run_dss_script(SCRIPT_ENABLED)
    df = dss_tools.model.regcontrols_df
    assert df is not None
    assert set(df["name"].str.lower()) == {"r1"}


def test_regcontrols_df_disabled_returns_none():
    run_dss_script(SCRIPT_DISABLED)
    df = dss_tools.model.regcontrols_df
    assert df is None


def test_regcontrols_df_none_when_no_regcontrols():
    run_dss_script(SCRIPT_NONE)
    df = dss_tools.model.regcontrols_df
    assert df is None

