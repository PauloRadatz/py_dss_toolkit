# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : AnalysisFeederResults.py
# @Software: PyCharm

import os

from py_dss_interface import DSS
from py_dss_toolkit.results.ModelVerification.Summary import Summary
from py_dss_toolkit.results.ModelVerification.SameBus import SameBus
from py_dss_toolkit.results.ModelVerification.Isolated import Isolated
from py_dss_toolkit.results.ModelVerification.LoadsTransformerVoltage import LoadsTransformerVoltage
from py_dss_toolkit.results.ModelVerification.PhasesConnections import PhasesConnections
from py_dss_toolkit.results.ModelVerification.TransformerData import TransformerData
from py_dss_toolkit.results.ModelVerification.PDBusOder import PDBusOder
from py_dss_toolkit.results.ModelVerification.CapacitorControlVoltage import CapacitorControlVoltage
from py_dss_toolkit.results.ModelVerification.RegulatorkVA import RegulatorkVA

from py_dss_toolkit.results.ModelVerification.RegulatorControlVoltage import RegulatorControlVoltage
class ModelVerificationResults(Summary,
                               Isolated,
                               SameBus,
                               LoadsTransformerVoltage,
                               PhasesConnections,
                               TransformerData,
                               PDBusOder,
                               RegulatorkVA):
    def __init__(self, dss: DSS):
        self._dss = dss
        Summary.__init__(self, self._dss)
        SameBus.__init__(self, self._dss)
        Isolated.__init__(self, self._dss)
        LoadsTransformerVoltage.__init__(self, self._dss)
        PhasesConnections.__init__(self, self._dss)
        TransformerData.__init__(self, self._dss)
        PDBusOder.__init__(self, self._dss)
        RegulatorkVA.__init__(self, self._dss)

class  AllModelVerificationResults:
    def __init__(self, dss: DSS):
        self.summary = Summary(dss).summary
        self.sameBus = SameBus(dss).same_bus
        self.isolated = Isolated(dss).isolated
        self.loads_transformer_voltage_mismatch = LoadsTransformerVoltage(dss).loads_transformer_voltage_mismatch
        self.busInversion = PDBusOder(dss).pd_bus_order  # To get results.
        self.capacitorControlVoltage = CapacitorControlVoltage(dss).capacitorControlVoltage  # To get results.
        self.regulatorControlVoltage = RegulatorControlVoltage(dss).regulatorControlVoltage  # To get results.

if __name__ == '__main__':
    import os
    import pathlib

    dss = DSS()
    script_path = os.path.dirname(os.path.abspath(__file__))
    dss_file = pathlib.Path(script_path).joinpath("..", "..","..", "..", "examples", "feeders", "123Bus", "IEEE123Master.dss")
    dss.text(f"compile [{dss_file}]")

    AllModelVerification = AllModelVerificationResults(dss)
    print(f'verification summary ==================================================')
    print(AllModelVerification.summary)
    print(f'verification sameBus ==================================================')
    print(AllModelVerification.sameBus)
    print(f'verification Isolated =================================================')
    print(AllModelVerification.isolated)
    print(f'verification LoadsTransformerVoltage ==================================')
    print(AllModelVerification.loads_transformer_voltage_mismatch)
    print(f'verification busInversion =============================================')
    print(AllModelVerification.busInversion)
    print(f'verification CapacitorControlVoltage ==================================')
    print(AllModelVerification.capacitorControlVoltage)
    print(f'verification regulatorControlVoltage ==================================')
    print(AllModelVerification.regulatorControlVoltage)
