# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_toolkit.view.dss_view.SnapShot.DSSViewSnapShotPowerFlowResults import DSSViewSnapShotPowerFlowResults
from py_dss_toolkit.view.dss_view.TimeSeries.DSSViewTimeSeriesPowerFlowResults import DSSViewTimeSeriesPowerFlowResults
from py_dss_interface import DSS


class ViewResults(DSSViewSnapShotPowerFlowResults, DSSViewTimeSeriesPowerFlowResults):

    def __init__(self, dss: DSS):
        DSSViewSnapShotPowerFlowResults.__init__(self, dss)
        DSSViewTimeSeriesPowerFlowResults.__init__(self, dss)
