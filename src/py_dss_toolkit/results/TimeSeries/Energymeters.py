# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com


from typing import Optional

import pandas as pd
from py_dss_interface import DSS


class Energymeters:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _energymeter_records(self):
        return self._create_energymeter_records()

    @property
    def energymeters(self) -> Optional[pd.DataFrame]:
        return self.__create_dataframe()

    def _create_energymeter_records(self):
        rows = []
        register_names = [name.lower() for name in self._dss.meters.register_names]
        self._dss.meters.first()
        for _ in range(self._dss.meters.count):
            if self._dss.cktelement.is_enabled:
                row = {"name": self._dss.meters.name.lower()}
                register_values = self._dss.meters.register_values
                row.update(
                    {
                        register_name: register_values[index]
                        for index, register_name in enumerate(register_names)
                    }
                )
                rows.append(row)
            self._dss.meters.next()
        return rows

    def __create_dataframe(self):
        if self._dss.meters.count == 0:
            return None

        return pd.DataFrame(self._create_energymeter_records())
