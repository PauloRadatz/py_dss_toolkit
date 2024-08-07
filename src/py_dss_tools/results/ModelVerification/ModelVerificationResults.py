# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : AnalysisFeederResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.ModelVerification.Summary import Summary
from py_dss_tools.results.ModelVerification.SameBus import SameBus
from py_dss_tools.results.ModelVerification.Isolated import Isolated
from py_dss_tools.results.ModelVerification.LoadsTransformerVoltage import LoadsTransformerVoltage
from py_dss_tools.results.ModelVerification.PhasesConnections import PhasesConnections
from py_dss_tools.results.ModelVerification.TransformerData import TransformerData


class ModelVerificationResults(Summary, Isolated, SameBus, LoadsTransformerVoltage, PhasesConnections, TransformerData):
    def __init__(self, dss: DSS):
        self._dss = dss
        Summary.__init__(self, self._dss)
        SameBus.__init__(self, self._dss)
        Isolated.__init__(self, self._dss)
        LoadsTransformerVoltage.__init__(self, self._dss)
        PhasesConnections.__init__(self, self._dss)
        TransformerData.__init__(self, self._dss)
