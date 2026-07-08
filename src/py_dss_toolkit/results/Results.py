# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Callable
from typing import Dict
from typing import Union

from py_dss_interface import DSS

from py_dss_toolkit.results.ShortCircuit.FaultResults import FaultResults
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.results.TimeSeries.TimeSeriesPowerFlowResults import TimeSeriesPowerFlowResults


class Results(SnapShotPowerFlowResults, TimeSeriesPowerFlowResults, FaultResults):
    def __init__(self, dss: DSS, connection_type_map: Union[Dict[str, str], Callable[[], Dict[str, str]], None] = None):
        self._dss = dss
        SnapShotPowerFlowResults.__init__(self, self._dss, connection_type_map)
        TimeSeriesPowerFlowResults.__init__(self, self._dss, connection_type_map)
        FaultResults.__init__(self, self._dss)
