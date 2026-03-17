# -*- coding: utf-8 -*-
"""Tests for same_buses_segments_df."""

from py_dss_toolkit import dss_tools

from .helpers import run_dss_script

# ---------------------------------------------------------------------------
# DSS Scripts
# ---------------------------------------------------------------------------

SCRIPT_ONE_TRANSFORMER = """
ClearAll
New Circuit.Thevenin bus1=A pu=1.0 basekv=13.8 model=ideal
New Transformer.TrafoTri phases=3 windings=2 xhl=3.2879 %loadloss=1.2 %noloadloss=0.3156 %imag=2.4800 leadlag=lead
~ wdg=1 bus=A kv=13.8 kva=112.5 conn=delta
~ wdg=2 bus=B kv=0.22 kva=112.5 conn=wye
New load.l bus1=B kw=112.5 pf=1
Set voltagebases=[13.8 0.22]
Calcvoltagebases
Solve
"""

SCRIPT_THREE_PARALLEL_TRANSFORMERS = """
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


def test_same_buses_segments_df_has_duplicates():
    """Three transformers between A and B; all should appear in same_buses_segments_df."""
    run_dss_script(SCRIPT_THREE_PARALLEL_TRANSFORMERS)
    mv = dss_tools.model_verification
    same_buses = mv.same_buses_segments_df
    assert len(same_buses) == 3
    assert set(same_buses["name"]) == {"transformer.trafoa", "transformer.trafob", "transformer.trafoc"}
    assert (same_buses["segments_in_pair"] == 3).all()


def test_same_buses_segments_df_empty_when_no_duplicates():
    """One element between A and B; same_buses_segments_df should be empty."""
    run_dss_script(SCRIPT_ONE_TRANSFORMER)
    mv = dss_tools.model_verification
    same_buses = mv.same_buses_segments_df
    assert len(same_buses) == 0
