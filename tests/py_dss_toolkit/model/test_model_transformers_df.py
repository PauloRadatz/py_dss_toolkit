from tests.py_dss_toolkit.model._dss_script_runner import run_dss_script
from py_dss_toolkit import dss_tools


SCRIPT_ENABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kV=13.8 kva=300 conn=delta
~ wdg=2 bus=B kV=0.22  kva=300 conn=wye
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_DISABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2 enabled=no
~ wdg=1 bus=A kV=13.8 kva=300 conn=delta
~ wdg=2 bus=B kV=0.22  kva=300 conn=wye
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_NONE = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Line.L1 bus1=A bus2=B phases=3 r1=0.1 x1=0.1 c1=0 length=1
Set voltagebases=[13.8]
Calcvoltagebases
Solve
"""


def test_transformers_df_enabled_returns_row():
    run_dss_script(SCRIPT_ENABLED)
    df = dss_tools.model.transformers_df
    assert df is not None
    assert set(df["name"].str.lower()) == {"t1"}


def test_transformers_df_disabled_returns_none():
    run_dss_script(SCRIPT_DISABLED)
    df = dss_tools.model.transformers_df
    assert df is None


def test_transformers_df_none_when_no_transformers():
    run_dss_script(SCRIPT_NONE)
    df = dss_tools.model.transformers_df
    assert df is None

