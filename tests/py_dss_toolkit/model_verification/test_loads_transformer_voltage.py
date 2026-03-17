# -*- coding: utf-8 -*-
"""Tests for loads_transformer_voltage_df."""

from py_dss_toolkit import dss_tools

from .helpers import run_dss_script

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_3PH_LOAD_CORRECT_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=3 windings=2 xhl=3
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=delta
~ wdg=2 bus=B kv=0.22 kva=112.5 conn=wye
New load.l3ok bus1=B.1.2.3 kv=0.22 phases=3 kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_3PH_LOAD_WRONG_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=3 windings=2 xhl=3
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=delta
~ wdg=2 bus=B kv=0.22 kva=112.5 conn=wye
New load.l3bad bus1=B.1.2.3 kv=0.13 phases=3 kw=100 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_1PH_LN_LOAD_CORRECT_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=1 windings=2 xhl=3
~ wdg=1 bus=A.1.2 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.1 kv=0.127 kva=37.5 conn=wye
New load.l1ok bus1=B.1 kv=0.127 phases=1 kw=37.5 pf=1
Set voltagebases=[13.8 0.127]
Calcvoltagebases
Solve
"""

SCRIPT_1PH_LN_LOAD_WRONG_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=1 windings=2 xhl=3
~ wdg=1 bus=A.1.2 kv=13.8 kva=37.5 conn=delta
~ wdg=2 bus=B.1 kv=0.127 kva=37.5 conn=wye
New load.l1bad bus1=B.1 kv=0.22 phases=1 kw=37.5 pf=1
Set voltagebases=[13.8 0.127]
Calcvoltagebases
Solve
"""

SCRIPT_1PH_LL_LOAD_CORRECT_KV = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.Tr phases=3 windings=2 xhl=3
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=delta
~ wdg=2 bus=B kv=0.22 kva=112.5 conn=wye
New load.l1ll bus1=B.1.2 kv=0.22 phases=1 kw=50 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_NO_LOADS = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.T1 phases=3 windings=2 xhl=5 %loadloss=0.15 %noloadloss=0.015 %imag=2
~ wdg=1 bus=A kV=13.8 kva=300 conn=delta
~ wdg=2 bus=B kV=0.22  kva=300 conn=wye
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""


def test_loads_transformer_voltage_df_columns():
    """Property always returns a DataFrame with the expected columns."""
    run_dss_script(SCRIPT_3PH_LOAD_CORRECT_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert list(df.columns) == ["Load", "kv_load", "kv_transformer", "voltage_type"]


def test_loads_transformer_voltage_df_empty_when_3ph_kv_correct():
    """3-phase load whose kv matches the transformer vll produces an empty result."""
    run_dss_script(SCRIPT_3PH_LOAD_CORRECT_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 0


def test_loads_transformer_voltage_df_detects_3ph_kv_mismatch():
    """3-phase load with kv set to vln instead of vll is flagged."""
    run_dss_script(SCRIPT_3PH_LOAD_WRONG_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 1
    assert df.iloc[0]["Load"] == "l3bad"
    assert round(df.iloc[0]["kv_load"], 2) == 0.13
    assert round(df.iloc[0]["kv_transformer"], 2) == 0.22
    assert df.iloc[0]["voltage_type"] == "ll"


def test_loads_transformer_voltage_df_empty_when_1ph_ln_kv_correct():
    """1-phase LN load whose kv matches the transformer vln produces an empty result."""
    run_dss_script(SCRIPT_1PH_LN_LOAD_CORRECT_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 0


def test_loads_transformer_voltage_df_detects_1ph_ln_kv_mismatch():
    """1-phase LN load with kv set to vll instead of vln is flagged."""
    run_dss_script(SCRIPT_1PH_LN_LOAD_WRONG_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 1
    assert df.iloc[0]["Load"] == "l1bad"
    assert round(df.iloc[0]["kv_load"], 2) == 0.22
    assert round(df.iloc[0]["kv_transformer"], 2) == 0.13
    assert df.iloc[0]["voltage_type"] == "ln"


def test_loads_transformer_voltage_df_empty_when_1ph_ll_kv_correct():
    """1-phase LL load (B.1.2) whose kv matches transformer vll produces an empty result."""
    run_dss_script(SCRIPT_1PH_LL_LOAD_CORRECT_KV)
    dss_tools.model.refresh_graph()
    df = dss_tools.model_verification.loads_transformer_voltage_df
    assert len(df) == 0


def test_loads_transformer_voltage_df_no_loads_returns_empty():
    """Circuit with transformer but no loads: loads_transformer_voltage_df is empty."""
    run_dss_script(SCRIPT_NO_LOADS)
    dss_tools.model.refresh_graph()
    mv = dss_tools.model_verification
    df = mv.loads_transformer_voltage_df
    assert len(df) == 0
