# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewTemporalResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.view.dss_view.Temporal.Monitor import Monitor


class ViewTemporalResults(Monitor):

    def __init__(self, dss: DSS):
        self._dss = dss
        Monitor.__init__(self, self._dss)
