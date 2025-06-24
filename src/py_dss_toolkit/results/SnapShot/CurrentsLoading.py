import pandas as pd
import numpy as np
from py_dss_interface import DSS
from .currents_utils import create_currents_elements_dataframes, get_violation_current_limit_type

class CurrentsLoading:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def current_loading_percent(self) -> pd.DataFrame:
        imags_df, _ = create_currents_elements_dataframes(self._dss)
        loading_df = imags_df.copy()
        limit_type = get_violation_current_limit_type()
        pd_element = list()
        for element in imags_df.index:
            self._dss.circuit.set_active_element(element)
            if len(self._dss.cktelement.bus_names) > 1:  # It is a PD Element
                pd_element.append(element)
                amps = getattr(self._dss.cktelement, limit_type)
                if amps > 0:
                    loading_df.loc[element] = (imags_df.loc[element] / amps) * 100
                else:
                    loading_df.loc[element] = np.nan
        return loading_df.loc[pd_element]

