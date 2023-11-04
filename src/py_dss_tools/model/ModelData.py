# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ModelData.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from py_dss_tools.model.ElementDataDFs import ElementDataDFs
from py_dss_tools.model.BusesDataDF import BusesDataDF
from py_dss_tools.model.SummaryModelData import SummaryModelData
from py_dss_tools.model.ElementData import ElementData


class ModelData(ElementDataDFs, BusesDataDF, SummaryModelData, ElementData):

    def __init__(self, dss: DSS):
        self._dss = dss
        ElementDataDFs.__init__(self, self._dss)
        BusesDataDF.__init__(self, self._dss)
        SummaryModelData.__init__(self, self._dss)
        ElementData.__init__(self, self._dss)
