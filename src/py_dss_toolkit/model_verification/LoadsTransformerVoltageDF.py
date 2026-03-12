# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.ModelBase import ModelBase

_PHASE_NODES = {"1", "2", "3"}


class LoadsTransformerVoltageDF:
    """Verify that load kV declarations match the upstream transformer connection voltages."""

    def __init__(self, dss: DSS, model: ModelBase):
        self._dss = dss
        self._model = model

    @property
    def loads_transformer_voltage_df(self) -> pd.DataFrame:
        """DataFrame of loads whose kV setting does not match the upstream transformer voltage."""
        return self._check_load_transformer()

    def _check_load_transformer(self) -> pd.DataFrame:
        data = []

        df = self._model.loads_df
        if df is None or df.empty:
            return pd.DataFrame(columns=["Load", "kV_set", "kV_use"])

        for _, row in df.iterrows():
            bus_full = str(row["bus1"])
            bus = bus_full.split(".")[0].lower()
            nodes = bus_full.split(".")[1:]
            phase_count = sum(1 for n in nodes if n in _PHASE_NODES)

            vll, vln = self._model.feeding_voltage(bus)
            expected = round(vll if phase_count >= 2 else vln, 2)

            kv_set = float(row["kv"])
            if round(kv_set, 2) != expected:
                data.append([row["name"], kv_set, expected])

        return pd.DataFrame(data, columns=["Load", "kV_set", "kV_use"])
