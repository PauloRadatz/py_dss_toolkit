# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.static_view.ViewStaticResults import ViewStaticResults
from py_dss_tools.static_view.ViewTemporalResults import ViewTemporalResults
from py_dss_tools.static_view.ViewFaultStudy import ViewFaultResults
from py_dss_tools.results.Results import Results
from py_dss_interface import DSS


class ViewResults(ViewStaticResults, ViewTemporalResults, ViewFaultResults):

    def __init__(self, dss: DSS, results: Results):
        ViewStaticResults.__init__(self, dss, results)
        ViewTemporalResults.__init__(self, dss, results)
        ViewFaultResults.__init__(self, dss, results)

