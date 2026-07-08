# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from py_dss_toolkit.model.ModelBase import ModelBase


class ReversedSegmentsDF:
    def __init__(self, model: ModelBase) -> None:
        self._model = model

    @property
    def reversed_segments_df(self) -> pd.DataFrame:
        """Segments whose DSS terminal order was flipped by the BFS."""
        df = self._model.graph_df
        return df[df["reversed"]].reset_index(drop=True)
