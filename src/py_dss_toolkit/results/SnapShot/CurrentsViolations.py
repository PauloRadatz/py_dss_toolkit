import pandas as pd
from py_dss_interface import DSS
from .CurrentsLoading import CurrentsLoading

class CurrentsViolations:
    def __init__(self, dss: DSS):
        self._dss = dss
        self.set_currents_loading_threshold_percent()

    def set_currents_loading_threshold_percent(self, threshold_percent: float = 100.0):
        self.threshold_percent = threshold_percent

    @property
    def violation_currents_elements(self) -> pd.DataFrame:
        loading = CurrentsLoading(self._dss)
        loading_df = loading.current_loading_percent

        mask = []
        for idx, row in loading_df.iterrows():
            if idx.startswith("transformer."):
                relevant = row[[col for col in row.index if "Terminal1" in col]]
                mask.append((relevant > self.threshold_percent).any())
            else:
                mask.append((row > self.threshold_percent).any())
        violating_elements = loading_df[mask]
        return violating_elements
