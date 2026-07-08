from _dss_script_runner import run_dss_script

from py_dss_toolkit import dss_tools

SCRIPT_ENABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
"""

# Disable the only Vsource (created by the circuit statement)
SCRIPT_DISABLED = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
Edit Vsource.Source enabled=no
"""

# No circuit at all -> vsources.count should be 0 -> df should be None
SCRIPT_NONE = """
ClearAll
"""


def test_vsources_df_enabled_has_at_least_one_row():
    run_dss_script(SCRIPT_ENABLED)
    df = dss_tools.model.vsources_df
    assert df is not None
    assert len(df) >= 1


def test_vsources_df_disabled_returns_none():
    run_dss_script(SCRIPT_DISABLED)
    df = dss_tools.model.vsources_df
    assert df is None


def test_vsources_df_none_when_no_circuit():
    run_dss_script(SCRIPT_NONE)
    df = dss_tools.model.vsources_df
    assert df is None
