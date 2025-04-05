# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS


class DSSViewTools:

    def __init__(self, dss: DSS):
        self._dss = dss

    def voltage_profile(self, option="all"):
        if self._dss.meters.count == 0:
            raise ValueError(f'At least one enerymeter should exist to plot the voltage profile.')
        self._dss.text(f"plot profile phases={option}")
