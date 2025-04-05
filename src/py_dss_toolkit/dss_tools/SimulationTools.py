# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS


class SimulationTools:

    def __init__(self, dss: DSS):
        self._dss = dss

    def solve_snapshot(self, control_mode="SnapShot", max_iterations=15, max_control_iter=10):
        self._dss.text(f"Set maxiterations={max_iterations}")
        self._dss.text(f"Set maxcontroliter={max_control_iter}")
        self._dss.text(f"set ControlMode={control_mode}")
        self._dss.text("Set Mode=SnapShot")
        self._dss.text("solve")

    def solve_daily(self, stepsize="1h", number=24, control_mode="SnapShot", max_iterations=15, max_control_iter=10):
        self._dss.text(f"Set maxiterations={max_iterations}")
        self._dss.text(f"Set maxcontroliter={max_control_iter}")
        self._dss.text(f"set ControlMode={control_mode}")
        self._dss.text("Set Mode=daily")
        self._dss.text(f"Set Stepsize={stepsize}")
        self._dss.text(f"Set number={number}")
        self._dss.text("solve")
