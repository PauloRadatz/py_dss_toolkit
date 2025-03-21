# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.view.static_view.SnapShot.StaticViewSnapShotPowerFlowResults import StaticViewSnapShotPowerFlowResults
from py_dss_tools.view.static_view.Temporal.ViewTemporalResults import ViewTemporalResults
from py_dss_tools.view.static_view.ShortCircuit.ViewFaultStudy import ViewFaultResults
from py_dss_tools.results.Results import Results
from py_dss_tools.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_tools.results.Temporal.TemporalResults import TemporalResults
from py_dss_interface import DSS
from typing import Union


class ViewResults(StaticViewSnapShotPowerFlowResults, ViewTemporalResults, ViewFaultResults):

    def __init__(self, dss: DSS, results: Union[Results, SnapShotPowerFlowResults, TemporalResults]):
        StaticViewSnapShotPowerFlowResults.__init__(self, dss, results)
        ViewTemporalResults.__init__(self, dss, results)
        ViewFaultResults.__init__(self, dss, results)

