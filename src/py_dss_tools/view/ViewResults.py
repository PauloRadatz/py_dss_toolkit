# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.view.ViewStaticResults import ViewStaticResults
from py_dss_tools.results.Results import Results
from py_dss_interface import DSS


class ViewResults(ViewStaticResults):

    def __init__(self, dss: DSS, results: Results):
        ViewStaticResults.__init__(self, dss, results)
