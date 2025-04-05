# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewCircuitResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.Circuit import Circuit
from py_dss_toolkit.model.ModelBase import ModelBase


class ViewCircuitResults(Circuit):

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults, model: ModelBase):
        self._dss = dss
        self._results = results
        self._model = model
        Circuit.__init__(self, self._dss, self._results, self._model)
