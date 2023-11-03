# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ModelData.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from py_dss_tools.model.ElementDataDFs import ModelDataDFs
from py_dss_tools.model.BusesDataDF import BusesDataDF


class ModelData(ModelDataDFs, BusesDataDF):

    def __init__(self, dss: DSS):
        self._dss = dss
        ModelDataDFs.__init__(self, self._dss)
        BusesDataDF.__init__(self, self._dss)
