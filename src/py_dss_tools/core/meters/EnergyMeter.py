# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:10:55
 Project: py_dss_tools [set, 2021]
"""


class EnergyMeter:
    name = "EnergyMeter"
    name_plural = "EnergyMeters"
    columns = ['3phaselosses', 'action', 'basefreq', 'caidi', 'custinterrupts', 'element', 'enabled', 'int_duration',
               'int_rate', 'kvaemerg', 'kvanormal', 'like', 'linelosses', 'localonly', 'losses', 'mask', 'option',
               'peakcurrent', 'phasevoltagereport', 'saidi', 'saifi', 'saifikw', 'seqlosses', 'terminal', 'vbaselosses',
               'xfmrlosses', 'zonelist']

    def __init__(self):
        pass
