import pandas as pd
import numpy as np
from py_dss_interface import DSS
from py_dss_toolkit.model.ElementDataDFs import ElementDataDFs
from .snapshot_utils import create_currents_elements_records, get_violation_current_limit_type


def _parse_dss_list(value: str) -> list:
    cleaned = str(value).replace("[", "").replace("]", "").strip()
    if not cleaned:
        return []
    if "," in cleaned:
        return [v.strip() for v in cleaned.split(",") if v.strip()]
    return [v.strip() for v in cleaned.split() if v.strip()]


def _terminal_number(col: str) -> int:
    return int(col.split("Terminal")[1].split(".")[0])


def _build_transformer_kvs_lookup(dss: DSS) -> dict:
    transformers_df = ElementDataDFs(dss).transformers_df
    if transformers_df is None:
        return {}
    lookup = {}
    for _, row in transformers_df.iterrows():
        kvs = [float(v) for v in _parse_dss_list(row.get("kvs", ""))]
        if kvs:
            lookup[row["name"]] = kvs
    return lookup


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

        transformer_kvs = _build_transformer_kvs_lookup(self._dss)

        loading_df = imags_df.loc[pd_elements].copy()
        for element in pd_elements:
            amps = amps_dict[element]
            if amps <= 0:
                loading_df.loc[element] = np.nan
                continue

            if element.startswith("transformer."):
                tr_name = element.split(".", 1)[1]
                kvs = transformer_kvs.get(tr_name)
                if kvs and len(kvs) >= 2:
                    kv1 = kvs[0]
                    for col in loading_df.columns:
                        t = _terminal_number(col)
                        if t == 1:
                            divisor = amps
                        elif t <= len(kvs):
                            divisor = amps * kv1 / kvs[t - 1]
                        else:
                            divisor = amps
                        loading_df.loc[element, col] = (imags_df.loc[element, col] / divisor) * 100
                else:
                    loading_df.loc[element] = (imags_df.loc[element] / amps) * 100
            else:
                loading_df.loc[element] = (imags_df.loc[element] / amps) * 100
        return loading_df

