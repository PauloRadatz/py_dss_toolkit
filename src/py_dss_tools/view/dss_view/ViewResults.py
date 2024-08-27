# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.view.dss_view.Static.ViewStaticResults import ViewStaticResults
from py_dss_tools.view.dss_view.Temporal.ViewTemporalResults import ViewTemporalResults
from py_dss_interface import DSS


class ViewResults(ViewStaticResults, ViewTemporalResults):

    def __init__(self, dss: DSS):
        ViewStaticResults.__init__(self, dss)
        ViewTemporalResults.__init__(self, dss)
