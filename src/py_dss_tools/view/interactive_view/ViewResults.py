# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.view.interactive_view.SnapShot.InteractiveViewSnapShotPowerFlowResults import InteractiveViewSnapShotPowerFlowResults
from py_dss_tools.view.interactive_view.TimeSeries.InteractiveViewTimeSeriesPowerFlowResults import InteractiveViewTimeSeriesPowerFlowResults
from py_dss_tools.view.interactive_view.SnapShot.Circuit import ViewCircuitResults
from py_dss_tools.results.Results import Results
from py_dss_tools.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_tools.results.TimeSeries.TimeSeriesPowerFlowResults import TimeSeriesPowerFlowResults
from py_dss_tools.model.ModelBase import ModelBase
from py_dss_interface import DSS
from typing import Union


class ViewResults(InteractiveViewSnapShotPowerFlowResults, InteractiveViewTimeSeriesPowerFlowResults):

    def __init__(self, dss: DSS, results: Union[Results, SnapShotPowerFlowResults, TimeSeriesPowerFlowResults], model: [ModelBase]):
        InteractiveViewSnapShotPowerFlowResults.__init__(self, dss, results, model)
        InteractiveViewTimeSeriesPowerFlowResults.__init__(self, dss, results)

