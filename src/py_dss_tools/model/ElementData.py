# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ElementData.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from typing import Dict
from py_dss_tools.dss_tools import DSSTools


class ElementData:
    def __init__(self, dss: DSS):
        self._dss = dss

    def element_data(self, element_class: str, element_name: str) -> pd.DataFrame:
        return DSSTools(self._dss).model.element_data(element_class, element_name)

    def edit_element(self, element_class: str, element_name: str, properties: Dict[str, str]) -> None:
        DSSTools(self._dss).model.edit_element(element_class, element_name, properties)

    def add_element(self, element_class: str, element_name: str, properties: Dict[str, str]) -> None:
        DSSTools(self._dss).model.add_element(element_class, element_name, properties)


