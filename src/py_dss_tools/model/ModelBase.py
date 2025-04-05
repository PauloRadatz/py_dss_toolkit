# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS

from py_dss_tools.model.BusesDataDF import BusesDataDF
from py_dss_tools.model.ElementData import ElementData
from py_dss_tools.model.ElementDataDFs import ElementDataDFs
from py_dss_tools.model.ModelUtils import ModelUtils
from py_dss_tools.model.SegmentsDF import SegmentsDF
from py_dss_tools.model.SummaryModelData import SummaryModelData


class ModelBase(ElementDataDFs, BusesDataDF, SummaryModelData, ElementData, SegmentsDF, ModelUtils):

    def __init__(self, dss: DSS):
        self._dss = dss
        ElementDataDFs.__init__(self, self._dss)
        BusesDataDF.__init__(self, self._dss)
        SummaryModelData.__init__(self, self._dss)
        ElementData.__init__(self, self._dss)
        SegmentsDF.__init__(self, self._dss)
        ModelUtils.__init__(self, self._dss)
