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

        terminal1_cols = [c for c in loading_df.columns if "Terminal1" in c]
        is_transformer = loading_df.index.str.startswith("transformer.")
        mask = pd.Series(False, index=loading_df.index)
        if is_transformer.any():
            mask[is_transformer] = (loading_df.loc[is_transformer, terminal1_cols] > self.threshold_percent).any(axis=1)
        if (~is_transformer).any():
            mask[~is_transformer] = (loading_df[~is_transformer] > self.threshold_percent).any(axis=1)
        violating_elements = loading_df[mask]
        return violating_elements
