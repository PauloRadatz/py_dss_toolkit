# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS

from py_dss_toolkit.results.SnapShot.CircuitSnapShotPowerFlowResults import CircuitSnapShotPowerFlowResults
from py_dss_toolkit.results.SnapShot.Currents import Currents
from py_dss_toolkit.results.SnapShot.Powers import Powers
from py_dss_toolkit.results.SnapShot.VoltagesElement import VoltagesElement
from py_dss_toolkit.results.SnapShot.VoltagesNodal import VoltagesNodal
from py_dss_toolkit.results.SnapShot.VoltagesNodalViolations import VoltagesNodalViolations
from py_dss_toolkit.results.SnapShot.CurrentsViolations import CurrentsViolations
from py_dss_toolkit.results.SnapShot.CurrentsLoading import CurrentsLoading
from py_dss_toolkit.results.SnapShot.currents_utils import set_violation_current_limit_type as _set_violation_current_limit_type, get_violation_current_limit_type as _get_violation_current_limit_type

class SnapShotPowerFlowResults(VoltagesNodal,
                               VoltagesElement,
                               Currents,
                               Powers,
                               CircuitSnapShotPowerFlowResults,
                               VoltagesNodalViolations,
                               CurrentsViolations,
                               CurrentsLoading):
    def __init__(self, dss: DSS):
        self._dss = dss
        VoltagesNodal.__init__(self, self._dss)
        VoltagesElement.__init__(self, self._dss)
        Currents.__init__(self, self._dss)
        Powers.__init__(self, self._dss)
        CircuitSnapShotPowerFlowResults.__init__(self, self._dss)
        VoltagesNodalViolations.__init__(self, self._dss)
        CurrentsViolations.__init__(self, self._dss)
        CurrentsLoading.__init__(self, self._dss)

    def set_violation_current_limit_type(self, limit_type: str = "norm_amps"):
        _set_violation_current_limit_type(limit_type)

    def get_violation_current_limit_type(self):
        return _get_violation_current_limit_type()
