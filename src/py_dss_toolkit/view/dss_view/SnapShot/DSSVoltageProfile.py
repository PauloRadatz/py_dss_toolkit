# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_toolkit.view.view_base.VoltageProfileBase import VoltageProfileBase

class DSSVoltageProfile(VoltageProfileBase):

    def __init__(self, dss: DSS):
        self._dss = dss
        VoltageProfileBase.__init__(self, self._dss, None)

    def voltage_profile(self, phases: str = ""):
        self._check_energymeter()
        if phases == "":
            self._dss.text(f"plot profile")
        elif phases == 'all':
            self._dss.text(f"plot profile phases=all")
