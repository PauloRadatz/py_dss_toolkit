# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd
from py_dss_interface import DSS


class Monitor:
    def __init__(self, dss: DSS):
        self._dss = dss

    def monitor(self, name: str):  # -> Optional[Dict[(str, str), pd.DataFrame]]:
        name = name.lower()
        if name not in [m.lower() for m in self._dss.monitors.names]:
            return None

        return self.__create_dataframe(name)

    def __create_dataframe(self, name: str):
        self._dss.monitors.name = name
        num_channels = self._dss.monitors.num_channels
        headers = self._dss.monitors.header
        dbl_hour = self._dss.monitors.dbl_hour
        dbl_freq = self._dss.monitors.dbl_freq

        dict_to_df = dict()
        dict_to_df["Hour"] = dbl_hour

        if len(dbl_freq) == 1:
            dict_to_df["sec"] = 0.0
        else:
            dict_to_df["sec"] = dbl_freq
        for index, header in enumerate(headers):
            dict_to_df[header] = self._dss.monitors.channel(index + 1)

        return pd.DataFrame().from_dict(dict_to_df)
