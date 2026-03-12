# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd

from py_dss_toolkit.model.ModelBase import ModelBase


class SameBusesSegmentsDF:
    """Segments that share the same bus pair, derived from the model's graph topology."""

    def __init__(self, model: ModelBase):
        self._model = model

    @property
    def same_buses_segments_df(self) -> pd.DataFrame:
        """Segments that share the same bus pair (multiple elements between the same two buses)."""
        edges = self._model.graph_df
        if edges.empty:
            return pd.DataFrame()

        def bus_pair(row):
            b1, b2 = str(row["bus1"]).lower(), str(row["bus2"]).lower()
            if b1 == b2:
                return None
            return tuple(sorted([b1, b2]))

        edges = edges.copy()
        edges["_bus_pair"] = edges.apply(bus_pair, axis=1)
        edges = edges[edges["_bus_pair"].notna()]

        pair_counts = edges.groupby("_bus_pair").size()
        duplicate_pairs = pair_counts[pair_counts > 1].index.tolist()

        result = edges[edges["_bus_pair"].isin(duplicate_pairs)].copy()
        result["segments_in_pair"] = result["_bus_pair"].map(pair_counts)
        result = result.drop(columns=["_bus_pair"])
        return result.reset_index(drop=True)
