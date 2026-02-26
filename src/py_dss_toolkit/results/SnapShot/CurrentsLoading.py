import pandas as pd
import numpy as np
from py_dss_interface import DSS
from .snapshot_utils import create_currents_elements_records, get_violation_current_limit_type

class CurrentsLoading:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def current_loading_percent(self) -> pd.DataFrame:
        imags_records, _, elements, element_norm_amps, element_emerg_amps = create_currents_elements_records(self._dss)

        imags_df = pd.DataFrame.from_dict(imags_records, orient='index').reindex(elements)
        limit_type = get_violation_current_limit_type()
        amps_dict = element_norm_amps if limit_type == "norm_amps" else element_emerg_amps
        pd_elements = [e for e in elements if e in amps_dict]

        loading_df = imags_df.loc[pd_elements].copy()
        for element in pd_elements:
            amps = amps_dict[element]
            if amps > 0:
                loading_df.loc[element] = (imags_df.loc[element] / amps) * 100
            else:
                loading_df.loc[element] = np.nan
        return loading_df

