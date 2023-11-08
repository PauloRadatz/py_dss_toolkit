# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Results.py
# @Software: PyCharm


from py_dss_tools.results.StaticResults import StaticResults
from py_dss_interface import DSS


class Results(StaticResults):

    def __init__(self, dss: DSS):
        self._dss = dss
        StaticResults.__init__(self, self._dss)
