# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com


from typing import Optional, Dict, List

from py_dss_interface import DSS
import pandas as pd


class ElementDataDFs:
    """Tabular exports of major OpenDSS element classes (one row per element).

    Mixed into :class:`~py_dss_toolkit.model.ModelBase.ModelBase`. Each ``*_df``
    returns ``None`` if that class has no **enabled** elements; otherwise a
    DataFrame with a lowercase ``name`` column and one column per DSS property
    from ``cktelement.property_names`` for that class.

    Access via ``dss_tools.model.lines_df`` (or ``study.model.…``), etc.
    """

    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _lines_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.lines)

    @property
    def _transformers_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.transformers)

    @property
    def _meters_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.meters)

    @property
    def _monitors_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.monitors)

    @property
    def _generators_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.generators)

    @property
    def _vsources_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.vsources)

    @property
    def _regcontrols_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.regcontrols)

    @property
    def _loads_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.loads)

    @property
    def _pvsystems_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.pvsystems)

    @property
    def _storage_records(self) -> Optional[Dict[str, List]]:
        return self._create_element_data_records(self._dss.storages)

    @property
    def lines_df(self) -> Optional[pd.DataFrame]:
        """All ``Line`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._lines_records)

    @property
    def transformers_df(self) -> Optional[pd.DataFrame]:
        """All ``Transformer`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._transformers_records)

    @property
    def meters_df(self) -> Optional[pd.DataFrame]:
        """All ``EnergyMeter`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._meters_records)

    @property
    def monitors_df(self) -> Optional[pd.DataFrame]:
        """All ``Monitor`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._monitors_records)

    @property
    def generators_df(self) -> Optional[pd.DataFrame]:
        """All ``Generator`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._generators_records)

    @property
    def vsources_df(self) -> Optional[pd.DataFrame]:
        """All ``Vsource`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._vsources_records)

    @property
    def regcontrols_df(self) -> Optional[pd.DataFrame]:
        """All ``RegControl`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._regcontrols_records)

    @property
    def loads_df(self) -> Optional[pd.DataFrame]:
        """All ``Load`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._loads_records)

    @property
    def pvsystems_df(self) -> Optional[pd.DataFrame]:
        """All ``PVSystem`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._pvsystems_records)

    @property
    def storage_df(self) -> Optional[pd.DataFrame]:
        """All ``Storage`` elements; ``None`` if none enabled."""
        return self.__create_dataframe_from_records(self._storage_records)

    def _create_element_data_records(self, element) -> Optional[Dict[str, List]]:
        if element.count == 0:
            return None

        element.first()
        element_properties = self._dss.cktelement.property_names
        prop_keys = [p.lower() for p in element_properties]
        num_props = len(element_properties)

        rows = []
        for element_name in element.names:
            element.name = element_name
            if self._dss.cktelement.is_enabled:
                row = [element.name.lower()]
                for idx in range(num_props):
                    row.append(self._dss.dssproperties.value_read(str(idx + 1)))
                rows.append(row)

        if not rows:
            return None

        columns = ["name"] + prop_keys
        records = {col: [r[i] for r in rows] for i, col in enumerate(columns)}
        return records

    @staticmethod
    def __create_dataframe_from_records(records: Optional[Dict[str, List]]) -> Optional[pd.DataFrame]:
        if records is None:
            return None
        return pd.DataFrame.from_dict(records)
