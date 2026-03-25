# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Callable, Dict, Union

from py_dss_interface import DSS

from py_dss_toolkit.results.SnapShot.AllLosses import AllLosses
from py_dss_toolkit.results.SnapShot.CircuitSnapShotPowerFlowResults import CircuitSnapShotPowerFlowResults
from py_dss_toolkit.results.SnapShot.Currents import Currents
from py_dss_toolkit.results.SnapShot.Losses import Losses
from py_dss_toolkit.results.SnapShot.Powers import Powers
from py_dss_toolkit.results.SnapShot.VoltagesElement import VoltagesElement
from py_dss_toolkit.results.SnapShot.VoltagesNodal import VoltagesNodal
from py_dss_toolkit.results.SnapShot.VoltagesNodalSmart import VoltagesNodalSmart
from py_dss_toolkit.results.SnapShot.VoltagesNodalViolations import VoltagesNodalViolations
from py_dss_toolkit.results.SnapShot.CurrentsViolations import CurrentsViolations
from py_dss_toolkit.results.SnapShot.CurrentsLoading import CurrentsLoading
from py_dss_toolkit.results.SnapShot.snapshot_utils import set_violation_current_limit_type as _set_violation_current_limit_type, get_violation_current_limit_type as _get_violation_current_limit_type

class SnapShotPowerFlowResults(VoltagesNodal,
                               VoltagesNodalSmart,
                               VoltagesElement,
                               Currents,
                               Powers,
                               Losses,
                               AllLosses,
                               CircuitSnapShotPowerFlowResults,
                               VoltagesNodalViolations,
                               CurrentsViolations,
                               CurrentsLoading):
    def __init__(self, dss: DSS, connection_type_map: Union[Dict[str, str], Callable[[], Dict[str, str]], None] = None):
        self._dss = dss
        VoltagesNodal.__init__(self, self._dss)
        VoltagesNodalSmart.__init__(self, self._dss, connection_type_map)
        VoltagesElement.__init__(self, self._dss)
        Currents.__init__(self, self._dss)
        Powers.__init__(self, self._dss)
        Losses.__init__(self, self._dss)
        AllLosses.__init__(self, self._dss)
        CircuitSnapShotPowerFlowResults.__init__(self, self._dss)
        VoltagesNodalViolations.__init__(self, self._dss, connection_type_map)
        CurrentsViolations.__init__(self, self._dss)
        CurrentsLoading.__init__(self, self._dss)

    def set_violation_current_limit_type(self, limit_type: str = "norm_amps"):
        _set_violation_current_limit_type(limit_type)

    def get_violation_current_limit_type(self):
        return _get_violation_current_limit_type()
