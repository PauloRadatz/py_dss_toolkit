# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com


from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.model.PDElementsDF import PDElementsDF


class SegmentsDF(PDElementsDF):
    """Segments are PD elements that connect two different buses (bus1 != bus2).

    Shunt PD elements (e.g. wye/delta capacitors where bus1 == bus2) are
    excluded from segments but available in ``pd_elements_df``.
    """

    def __init__(self, dss: DSS):
        PDElementsDF.__init__(self, dss)

    @property
    def _segments_records(self) -> Dict[str, List]:
        return self._create_segments_records()

    @property
    def _enabled_segments_records(self) -> Dict[str, List]:
        return self._filter_segments_records(enabled=True)

    @property
    def _disabled_segments_records(self) -> Dict[str, List]:
        return self._filter_segments_records(enabled=False)

    @property
    def segments_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._segments_records)
        if df.empty:
            return None
        return df

    @property
    def enabled_segments_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._enabled_segments_records)
        if df.empty:
            return None
        return df.drop(columns=["enabled"]).reset_index(drop=True)

    @property
    def disabled_segments_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._disabled_segments_records)
        if df.empty:
            return None
        return df.drop(columns=["enabled"]).reset_index(drop=True)

    def _create_segments_records(self) -> Dict[str, List]:
        """PD element records filtered to bus1 != bus2 (series connections only).

        Elements with an empty bus2 (e.g. delta capacitors) are excluded.
        """
        records = self._create_pd_elements_records()
        indexes = [i for i, (b1, b2) in enumerate(zip(records["bus1"], records["bus2"])) if b2 and b1 != b2]
        return {key: [values[i] for i in indexes] for key, values in records.items()}

    def _filter_segments_records(self, enabled: bool) -> Dict[str, List]:
        records = self._create_segments_records()
        indexes = [i for i, value in enumerate(records["enabled"]) if value is enabled]
        return {key: [values[i] for i in indexes] for key, values in records.items()}

    def __create_dataframe(self, records: Dict[str, List]):
        return pd.DataFrame.from_dict(records)
