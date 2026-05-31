# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.ModelBase import ModelBase

_PHASE_NODES = {"1", "2", "3"}
_NEUTRAL_NODES = {"0", "4"}


def _load_uses_vll(nodes: list) -> bool:
    """True if load kV is line-to-line based on connection.

    - 3ph (3 nodes in [1,2,3]): vll
    - 1ph with 2 nodes in [1,2,3] (e.g. B.1.2): vll
    - 1ph with 1 phase node and neutral (e.g. B.1.0, B.2.4): vln
    - 1ph with single phase node only (e.g. B.1): vln
    - Empty nodes (default 3ph): vll
    """
    phase_nodes = [n for n in nodes if n in _PHASE_NODES]
    neutral_nodes = [n for n in nodes if n in _NEUTRAL_NODES]
    phase_count = len(phase_nodes)

    if phase_count >= 2:
        return True  # 3ph or 1ph between two phases
    if phase_count == 1 and neutral_nodes:
        return False  # 1ph phase-to-neutral
    if phase_count == 1:
        return False  # 1ph single node (e.g. B.1) → ln
    return True  # empty nodes → default 3ph


class LoadsTransformerVoltageDF:
    """Verify that load kV declarations match the upstream transformer connection voltages."""

    def __init__(self, dss: DSS, model: ModelBase):
        self._dss = dss
        self._model = model

    @property
    def _loads_transformer_voltage_records(self) -> list:
        return self._create_loads_transformer_voltage_records()

    @property
    def loads_transformer_voltage_df(self) -> pd.DataFrame:
        """DataFrame of loads whose kV setting does not match the upstream transformer voltage.

        Columns: ``Load`` (element name), ``Transformer`` (segment name of the first
        upstream transformer that sets the bus voltage, or empty if none), ``kv_load``,
        ``kv_transformer``, ``voltage_type`` (``ll`` or ``ln``).
        """
        return pd.DataFrame(
            self._loads_transformer_voltage_records,
            columns=["Load", "Transformer", "kv_load", "kv_transformer", "voltage_type"],
        )

    def _create_loads_transformer_voltage_records(self) -> list:
        df = self._model.loads_df
        if df is None or df.empty:
            return []

        data = []
        for _, row in df.iterrows():
            bus_full = str(row["bus1"])
            bus = bus_full.split(".")[0].lower()
            nodes = bus_full.split(".")[1:]

            vll, vln = self._model.feeding_voltage(bus)
            uses_vll = _load_uses_vll(nodes)
            voltage_type = "ll" if uses_vll else "ln"
            kv_transformer = round(vll if uses_vll else vln, 4)

            kv_load = float(row["kv"])
            if round(kv_load, 4) != kv_transformer:
                tr_name = self._model.graph.nodes[bus].get("feeding_transformer", "")
                data.append([row["name"], tr_name, kv_load, kv_transformer, voltage_type])

        return data
