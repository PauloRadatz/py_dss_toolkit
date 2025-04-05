# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_toolkit.view.static_view.SnapShot.StaticViewSnapShotPowerFlowResults import StaticViewSnapShotPowerFlowResults
from py_dss_toolkit.view.static_view.TimeSeries.StaticViewTimeSeriesPowerFlowResults import StaticViewTimeSeriesPowerFlowResults
from py_dss_toolkit.view.static_view.ShortCircuit.ViewFaultStudy import ViewFaultResults
from py_dss_toolkit.results.Results import Results
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.results.TimeSeries.TimeSeriesPowerFlowResults import TimeSeriesPowerFlowResults
from py_dss_interface import DSS
from typing import Union


class ViewResults(StaticViewSnapShotPowerFlowResults, StaticViewTimeSeriesPowerFlowResults, ViewFaultResults):

    def __init__(self, dss: DSS, results: Union[Results, SnapShotPowerFlowResults, TimeSeriesPowerFlowResults]):
        StaticViewSnapShotPowerFlowResults.__init__(self, dss, results)
        StaticViewTimeSeriesPowerFlowResults.__init__(self, dss, results)
        ViewFaultResults.__init__(self, dss, results)

