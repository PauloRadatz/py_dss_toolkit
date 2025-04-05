# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS

from py_dss_toolkit.results.SnapShot.CircuitSnapShotPowerFlowResults import CircuitSnapShotPowerFlowResults
from py_dss_toolkit.results.SnapShot.Currents import Currents
from py_dss_toolkit.results.SnapShot.Powers import Powers
from py_dss_toolkit.results.SnapShot.VoltagesElement import VoltagesElement
from py_dss_toolkit.results.SnapShot.VoltagesNodal import VoltagesNodal
from py_dss_toolkit.results.TimeSeries.Energymeters import Energymeters
from py_dss_toolkit.results.TimeSeries.Monitor import Monitor


class TimeSeriesPowerFlowResults(Energymeters, Monitor, VoltagesNodal, VoltagesElement, Currents, Powers,
                                 CircuitSnapShotPowerFlowResults):

    def __init__(self, dss: DSS):
        self._dss = dss
        Energymeters.__init__(self, self._dss)
        Monitor.__init__(self, self._dss)
        VoltagesNodal.__init__(self, self._dss)
        VoltagesElement.__init__(self, self._dss)
        Currents.__init__(self, self._dss)
        Powers.__init__(self, self._dss)
        CircuitSnapShotPowerFlowResults.__init__(self, self._dss)
