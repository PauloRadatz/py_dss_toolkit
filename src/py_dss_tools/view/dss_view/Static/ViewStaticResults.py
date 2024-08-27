# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewStaticResults.py
# @Software: PyCharm

from py_dss_tools.view.dss_view.Static.VoltageProfile import VoltageProfile
from py_dss_interface import DSS


class ViewStaticResults(VoltageProfile):

    def __init__(self, dss: DSS):
        VoltageProfile.__init__(self, dss)
